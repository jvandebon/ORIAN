#include <boost/python.hpp>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <sys/time.h>
#include <unistd.h>
#include "NBody.h"
#include <MaxSLiCInterface.h>
#include "Maxfiles.h"
#include "main.h"

#define EPS 100
#define NT 1

struct CPUComputeContext{

   uint32_t n_threads;
   int volume;
   particle_t *particles;
   float *m;
   particle_t *cpu_particles;
   coord3d_t *a;

};

uint64_t cpu_compute_construct(int volume, uint32_t n_threads){

  struct CPUComputeContext *context = new CPUComputeContext();

  context->n_threads = n_threads;
  context->volume = volume;;

  context->particles = (particle_t *) malloc(volume * sizeof(particle_t));
  context->m = (float *) malloc(volume * sizeof(float));

  srand(100);
  for (int i = 0; i < volume; i++)
  {
     context->m[i] = (float)rand()/100000;
     context->particles[i].p.x = (float)rand()/100000;
     context->particles[i].p.y = (float)rand()/100000;
     context->particles[i].p.z = (float)rand()/100000;
     context->particles[i].v.x = (float)rand()/100000;
     context->particles[i].v.y = (float)rand()/100000;
     context->particles[i].v.z = (float)rand()/100000;
   }

   context->cpu_particles = (particle_t *) malloc(volume * sizeof(particle_t));
   memcpy(context->cpu_particles, context->particles, volume * sizeof(particle_t));
   context->a = (coord3d_t *) malloc(volume * sizeof(coord3d_t));

   return (uint64_t)context;
}


void run_cpu(int N, const float *m, particle_t *p, coord3d_t *a, uint32_t n_threads)
{

    double wall_time;
    timer_init(&wall_time);
    timer_start(&wall_time);
    double cpuTime = 0;

    puts("Running on CPU...\n");

    for (int t = 0; t < NT; t++) {

        memset(a, 0, N * sizeof(coord3d_t));
	
	#pragma omp parallel for num_threads(n_threads)
        for (int q = 0; q < N; q++) {
            for (int j = 0; j < N; j++) {
                //if (j != q) {
                    float rx = p[j].p.x - p[q].p.x;
                    float ry = p[j].p.y - p[q].p.y;
                    float rz = p[j].p.z - p[q].p.z;
                    float dd = rx*rx + ry*ry + rz*rz + EPS;
                    float d = 1/ (dd*sqrtf(dd));
                    float s = m[j] * d;
                    a[q].x += rx * s;
                    a[q].y += ry * s;
                    a[q].z += rz * s;
                //}
            }
        }

	#pragma omp parallel for num_threads(n_threads)
        for (int i = 0; i < N; i++) {
            p[i].p.x += p[i].v.x;
            p[i].p.y += p[i].v.y;
            p[i].p.z += p[i].v.z;
            p[i].v.x += a[i].x;
            p[i].v.y += a[i].y;
            p[i].v.z += a[i].z;
        }
    }

    timer_stop(&wall_time);

    cpuTime = wall_time;
    printf("CPU execution time: %.3gs\n", cpuTime);

}


void cpu_compute(uint64_t c) {
  
  struct CPUComputeContext *context = (struct CPUComputeContext *)c;
  run_cpu(context->volume, context->m, context->particles, context->a, context->n_threads);

}


void cpu_compute_destruct(uint64_t c) {

  struct CPUComputeContext *context = (struct CPUComputeContext *)c;
  
  free(context->a);
  free(context->particles);
  free(context->m);
  free(context->cpu_particles);
  free(context);
}


struct DFEComputeContext{
   int volume;
   particle_t *particles;
   float *m;
   dfe_in_t *dfe_particles;
   dfe_out_t *acc;
   particle_t *cur_particles;
   int newN;
   max_file_t *maxfile;
};

uint64_t dfe_compute_construct(int volume){

  struct DFEComputeContext *context = new DFEComputeContext();

  context->volume = volume;;

  context->particles = (particle_t *) malloc(volume * sizeof(particle_t));
  context->m = (float *) malloc(volume * sizeof(float));

  srand(100);
  for (int i = 0; i < volume; i++)
  {
     context->m[i] = (float)rand()/100000;
     context->particles[i].p.x = (float)rand()/100000;
     context->particles[i].p.y = (float)rand()/100000;
     context->particles[i].p.z = (float)rand()/100000;
     context->particles[i].v.x = (float)rand()/100000;
     context->particles[i].v.y = (float)rand()/100000;
     context->particles[i].v.z = (float)rand()/100000;
   }

   context->maxfile = NBody_init();

   const int latency = max_get_constant_uint64t(context->maxfile, "loopLatency");
   const int max_particles = max_get_constant_uint64t(context->maxfile, "maxParticles");
   const int num_particles_divisor = max_get_constant_uint64t(context->maxfile, "numParticlesDivisor");

   if (volume < latency) {
     context->newN = next_multiple(latency, num_particles_divisor);
     fprintf(stderr, "info: The number of particles on the DFE has been padded to %d\n", context->newN);
   } else if (volume > max_particles) {
     fprintf(stderr, "error: the number of particles must be less than or equal to %d\n", max_particles);
     exit(EXIT_FAILURE);
   } else if (volume % num_particles_divisor != 0) {
     context->newN = next_multiple(volume, num_particles_divisor);
     fprintf(stderr, "info: The number of particles on the DFE has been padded to %d\n", context->newN);
   } else {
     context->newN = volume;
   }

    /* Copy initial state of particles */
    context->dfe_particles = (dfe_in_t *) malloc(context->newN * sizeof(dfe_in_t));
    for (int i = 0; i < volume; i++) {
        context->dfe_particles[i].x = context->particles[i].p.x;
        context->dfe_particles[i].y = context->particles[i].p.y;
        context->dfe_particles[i].z = context->particles[i].p.z;
        context->dfe_particles[i].m = context->m[i];
    }

    for (int i = volume; i < context->newN; i++) {
        context->dfe_particles[i].x = 0;
        context->dfe_particles[i].y = 0;
        context->dfe_particles[i].z = 0;
        /* Setting a null mass on the padded particles ensures they have no effect */
        context->dfe_particles[i].m = 0;
    }

   context->acc = (dfe_out_t *) malloc(context->newN * sizeof(dfe_out_t));
   context->cur_particles = (particle_t *) malloc(volume * sizeof(particle_t));
   memcpy(context->cur_particles, context->particles, volume * sizeof(particle_t));

   return (uint64_t)context;
}

static void run_dfe(int newN, particle_t *cur_particles, dfe_in_t *dfe_particles, dfe_out_t *acc, int volume)
{

    puts("Running on DFE...\n");
    
    double wall_time, run_time, update_time, dfeTime;
    timer_init(&wall_time);
    timer_init(&run_time);
    timer_init(&update_time);
    timer_start(&wall_time);

    for (int t = 0; t < NT; t++) {

        timer_start(&run_time);
        NBody(newN, EPS, (float *) dfe_particles, (float *) acc);
        timer_stop(&run_time);

        timer_start(&update_time);

        /* Update the state of particles */
        for (int i = 0; i < volume; i++) {
            cur_particles[i].p.x += cur_particles[i].v.x;
            cur_particles[i].p.y += cur_particles[i].v.y;
            cur_particles[i].p.z += cur_particles[i].v.z;
            cur_particles[i].v.x += acc[i].x;
            cur_particles[i].v.y += acc[i].y;
            cur_particles[i].v.z += acc[i].z;
        }

        for (int i = 0; i < volume; i++) {
            dfe_particles[i].x = cur_particles[i].p.x;
            dfe_particles[i].y = cur_particles[i].p.y;
            dfe_particles[i].z = cur_particles[i].p.z;
        }
        timer_stop(&update_time);
    }

    timer_stop(&wall_time);

    printf("Wall clock time:   %-12gs\n", wall_time);
    printf("Run time:          %-12gs (%.1f%%)\n", run_time, run_time/wall_time*100);
    printf("Update time:       %-12gs (%.1f%%)\n", update_time, update_time/wall_time*100);

    dfeTime = wall_time;
    printf("DFE execution time: %.3gs\n", dfeTime);
}

void dfe_compute(uint64_t c){

  struct DFEComputeContext *context = (struct DFEComputeContext *)c;
  run_dfe(context->newN, context->cur_particles, context->dfe_particles, context->acc, context->volume);
}


void dfe_compute_destruct(uint64_t c){

    struct DFEComputeContext *context = (struct DFEComputeContext *)c;  

    max_file_free(context->maxfile);

    free(context->acc);
    free(context->cur_particles);
    free(context->particles);
    free(context->dfe_particles);
    free(context);
}



BOOST_PYTHON_MODULE(nbody)
{
  using namespace boost::python;
  def("cpu_compute", cpu_compute);
  def("cpu_compute_construct", cpu_compute_construct);
  def("cpu_compute_destruct", cpu_compute_destruct);
  def("dfe_compute", dfe_compute);
  def("dfe_compute_construct", dfe_compute_construct);
  def("dfe_compute_destruct", dfe_compute_destruct);
}
