#include "RandomVariable.h"
#include "Adp.h"
#include <omp.h>
#include <stdio.h>
#include <unistd.h>
#include <iostream>
#include <fstream>
#include <stdlib.h>
#include <sys/wait.h>
#include <boost/python.hpp>

#define NUM_FEATURES 12
#define BETA 0.001

extern "C" {
void maxrt_direct_stream_write() { 
   printf("Should not be invoking me...\n");
}
}

using namespace std;

float *global_pm;
float *global_pv;
float *global_y;

max_group_t *global_group;
max_file_t *global_maxfile;

struct CPUComputeContext{
  float *y;
  float *prior_m;
  float *prior_v;
  int nproc;
  int volume;
  float *post_m;
  float *post_s;
};

struct DFEComputeContext {
  float *y;
  float *prior_m;
  float *prior_v;
  int nproc;
  int volume;
  int allocSize;
  float *post_m;
  float *post_s;
  max_file_t *maxfile;
  max_group_t *group;
  uint64_t dfeActions;
  uint64_t batchSize;
};
	
static float V (float t) {
   float cdf = RandomVariable::CDF(t, 0, 1);
   if (cdf == 0.0) {
      return 0.0;
   }
   
   return RandomVariable::PDF(t, 0, 1) / cdf;
}
  
static float W (float t) {
	float v = V(t);
	return v * (v + t);
}

static float frand(int min, int max) {
   return min + (float)rand()/((float)RAND_MAX/(max-min));        
}

 float rand_y() {
    return (rand() % 2)? 1.0 : -1.0;
 }
 
 float rand_m() {
    return frand(-6, 6); 
 }
   
float rand_v() {
   return frand(0, 100); 
}

// GLOBALS
float g_y = rand_y(); 
float g_m = rand_m();
float g_v = rand_v();

void create_python_impressions(int volume, boost::python::list& prior_m, boost::python::list& prior_v, boost::python::list& y) {

   for (int i = 0; i < volume; i++) {
      y[i] = rand_y();
      uint64_t base = i*NUM_FEATURES;
      for (int j = 0; j < NUM_FEATURES; j++) {     
          prior_m[base+j] = rand_m();
          prior_v[base+j] = rand_v();
      }                      
   } 
}

uint64_t cpu_compute_construct(int volume, int nproc, string pm_file, string pv_file, string y_file){

  std::cout << "AdPredictor " << volume << " " << nproc << " threads." << std::endl;

  // allocate memeory and initialize compute context struct
  struct CPUComputeContext *context = new CPUComputeContext();
  
  int total_size = volume * NUM_FEATURES;
  float *prior_m = new float[total_size];
  float *prior_v = new float[total_size];     
  float *post_m = new float[total_size];           
  float *post_s = new float[total_size];  
  float *y = new float[volume];

  context->prior_m = prior_m;
  context->prior_v = prior_v;
  context->y = y;
  context->volume = volume;
  context->nproc = nproc;
  context->post_m = post_m;
  context->post_s = post_s;

  // read files and populate values for priors and y
/*  ifstream pmfile (pm_file.c_str());
  ifstream pvfile (pv_file.c_str());
  ifstream yfile (y_file.c_str());

  for (int i = 0; i < volume; i++) {
    yfile >> y[i];
    uint64_t base = i*NUM_FEATURES;
    for (int j = 0; j < NUM_FEATURES; j++) {
        pmfile >> prior_m[base+j];
        pvfile >> prior_v[base+j];
    }                      
  } 

  pvfile.close();
  pmfile.close();
  yfile.close();

  for (int i = 0; i < volume; i++) {
    y[i] = global_y[i];
    uint64_t base = i*NUM_FEATURES;
    for (int j = 0; j < NUM_FEATURES; j++) {
      prior_m[base+j] = global_pm[base+j];
      prior_v[base+j] = global_pv[base+j];
    }
  }
*/

  for (int i = 0; i < volume; i++) {
    y[i] = g_y;
    uint64_t base = i*NUM_FEATURES;
    for (int j = 0; j < NUM_FEATURES; j++) {
      prior_m[base+j] = g_m;
      prior_v[base+j] = g_v;
    }
  } 
  // return pointer to struct
  return (uint64_t)context;

}

void cpu_compute_destruct(uint64_t c, string postm_file, string posts_file){
  
  struct CPUComputeContext *context = (struct CPUComputeContext *)c;
  
  // write posts to files
/*  int total_size = context->volume * NUM_FEATURES;

  ofstream pmfile, psfile;
  pmfile.open (postm_file.c_str());
  psfile.open (posts_file.c_str());

  for (int i = 0; i < total_size; i++) {
    pmfile << context->post_m[i] << "\n";
    psfile << context->post_s[i] << "\n";
  }

  pmfile.close();
  psfile.close();
*/
  // clear all memory 
  delete context->prior_m;
  delete context->prior_v;
  delete context->y;
  delete context->post_m;
  delete context->post_s;
  delete context;

  std::cout << "...finished." << std::endl;

}

void _cpu_compute(int volume, int nproc, float *prior_m, float *prior_v, float *post_m, float *post_s, float *y){

  omp_set_num_threads(nproc);

  #pragma omp parallel for schedule(dynamic) 
  for (int st = 0; st < volume; st++) {
    float s = 0.0;
    float m = 0.0;
    for (int i = 0; i < NUM_FEATURES; i++) {
      int idx = st*NUM_FEATURES+i;
      m += prior_m[idx];
      s += prior_v[idx];
    }
    float beta = BETA;
    float S = sqrt(beta*beta + s);
    float t = (y[st] * m) / S;
    for (int i = 0; i < NUM_FEATURES; i++) {
      post_m[st*NUM_FEATURES+i] = prior_m[st*NUM_FEATURES+i] + y[st] * (prior_v[st*NUM_FEATURES+i] / S) * V(t);
      post_s[st*NUM_FEATURES+i] = sqrt(fabs(prior_v[st*NUM_FEATURES+i] * (1 - (prior_v[st*NUM_FEATURES+i] / (S*S)) * W(t))));     
    }          
  }
}

void cpu_compute(uint64_t c) {
  struct CPUComputeContext *context = (struct CPUComputeContext *)c;
  _cpu_compute(context->volume, context->nproc, context->prior_m, context->prior_v, context->post_m, context->post_s, context->y); 
}


void load_impressions(int volume, string pm_file, string pv_file, string y_file){

  global_pm = new float[volume * NUM_FEATURES];
  global_pv = new float[volume * NUM_FEATURES];
  global_y = new float[volume];

  // read files and populate values for priors and y
  ifstream pmfile (pm_file.c_str());
  ifstream pvfile (pv_file.c_str());
  ifstream yfile (y_file.c_str());

  for (int i = 0; i < volume; i++) {
    yfile >> global_y[i];
    uint64_t base = i*NUM_FEATURES;
    for (int j = 0; j < NUM_FEATURES; j++) {
        pmfile >> global_pm[base+j];
        pvfile >> global_pv[base+j];
    }

    if (i % 5000000 == 0) {
       cout << i << endl;
    }
  }

  pvfile.close();
  pmfile.close();
  yfile.close();

}

void load_dfes(int nproc){
  std::cout << "Loading DFEs: " << nproc << std::endl;
  global_maxfile = Adp_init();
  global_group = max_load_group(global_maxfile, MAXOS_EXCLUSIVE, "adp", nproc);
  std::cout << "finished." << global_group << std::endl;
}

uint64_t dfe_compute_construct(int volume, int nproc, string pm_file, string pv_file, string y_file){

  std::cout << "AdPredictor " << volume << " " << nproc << " DFEs." << std::endl;

  // allocate memeory and initialize compute context struct
  struct DFEComputeContext *context = new DFEComputeContext();
  
  int alignBy = nproc * 16;

  if (alignBy != 0) {
    uint64_t m = volume % alignBy;
    context->allocSize = m ? volume + alignBy - m : volume;
  } else {
    context->allocSize = volume;
  }

  int total_size = context->allocSize * NUM_FEATURES;

  float *prior_m = new float[total_size];
  float *prior_v = new float[total_size];     
  float *post_m = new float[total_size];           
  float *post_s = new float[total_size];  
  float *y = new float[context->allocSize];
  
  context->prior_m = prior_m;
  context->prior_v = prior_v;
  context->y = y;
  context->volume = volume;
  context->nproc = nproc;
  context->post_m = post_m;
  context->post_s = post_s;
  
  // read files and populate values for priors and y
/*
  ifstream pmfile (pm_file.c_str());
  ifstream pvfile (pv_file.c_str());
  ifstream yfile (y_file.c_str());

  for (int i = 0; i < volume; i++) {
    yfile >> y[i];
    uint64_t base = i*NUM_FEATURES;
    for (int j = 0; j < NUM_FEATURES; j++) {
        pmfile >> prior_m[base+j];
        pvfile >> prior_v[base+j];
    }                      
  } 

  pvfile.close();
  pmfile.close();
  yfile.close();

  for (int i = 0; i < volume; i++) {
    y[i] = global_y[i];
    uint64_t base = i*NUM_FEATURES;
    for (int j = 0; j < NUM_FEATURES; j++) {
      prior_m[base+j] = global_pm[base+j];
      prior_v[base+j] = global_pv[base+j];
    }
  }
*/
 
  for (int i = 0; i < volume; i++) {
    y[i] = g_y;
    uint64_t base = i*NUM_FEATURES;
    for (int j = 0; j < NUM_FEATURES; j++) {
      prior_m[base+j] = g_m;
      prior_v[base+j] = g_v;
    }
  } 

  context->maxfile = global_maxfile; // Adp_init();
  context->group = global_group; // max_load_group(context->maxfile, MAXOS_EXCLUSIVE, "adp", nproc);

  if ((uint64_t) (context->allocSize / 16) < (uint64_t) nproc) {
    context->dfeActions = context->allocSize / 16;
  } else {
    context->dfeActions = nproc;
  }
  context->batchSize = context->allocSize / context->dfeActions;   
	
  // return pointer to struct
  return (uint64_t)context;

}

void dfe_compute_destruct(uint64_t c, string postm_file, string posts_file){
  
  struct DFEComputeContext *context = (struct DFEComputeContext *)c;
  
  // write posts to files
  int total_size = context->volume * NUM_FEATURES;
/*
  ofstream pmfile, psfile;
  pmfile.open (postm_file.c_str());
  psfile.open (posts_file.c_str());

  for (int i = 0; i < total_size; i++) {
    pmfile << context->post_m[i] << "\n";
    psfile << context->post_s[i] << "\n";
  }

  pmfile.close();
  psfile.close();
*/
  // clear all memory
//  max_unload_group(context->group);
//  max_file_free(context->maxfile);

  delete context->prior_m;
  delete context->prior_v;
  delete context->y;
  delete context->post_m;
  delete context->post_s;
  delete context;

  std::cout << "...finished." << std::endl;
}



void _dfe_compute(int volume, int nproc, uint64_t dfeActions, uint64_t batchSize, max_group_t *group, float *prior_m, float *prior_v, float *post_m, float *post_s, float *y) {


  max_run_t* actionCompletion[dfeActions]; 
  Adp_actions_t action[dfeActions];
  float* tmp_prior_m = prior_m;
  float* tmp_prior_v = prior_v;
  float* tmp_y = y;
  float* tmp_post_m = post_m;
  float* tmp_post_s = post_s;
  for (uint64_t i = 0; i < dfeActions ; ++i){
    action[i] = (Adp_actions_t) {
            batchSize, 
            BETA, 
            tmp_prior_m,
            tmp_prior_v,
            tmp_y,
            tmp_post_m,
            tmp_post_s
          };
    actionCompletion[i] = Adp_run_group_nonblock(group, &action[i]);
    // Advance the pointers for the next action
    tmp_prior_m += (batchSize * NUM_FEATURES);
    tmp_prior_v += (batchSize * NUM_FEATURES);
    tmp_y += batchSize;
    tmp_post_m += (batchSize * NUM_FEATURES);
    tmp_post_s += (batchSize * NUM_FEATURES);
  }	

  for (uint64_t i = 0 ; i < dfeActions ; ++i){
    max_wait(actionCompletion[i]);
  }
}


void dfe_compute(uint64_t c) {
  struct DFEComputeContext *context = (struct DFEComputeContext *)c;
  _dfe_compute(context->volume, context->nproc, context->dfeActions, context->batchSize, context->group, context->prior_m, context->prior_v, context->post_m, context->post_s, context->y);

}

BOOST_PYTHON_MODULE(adp)
{
    using namespace boost::python;
    def("cpu_compute_construct", cpu_compute_construct);
    def("cpu_compute_destruct", cpu_compute_destruct);
    def("cpu_compute", cpu_compute);
    def("dfe_compute_construct", dfe_compute_construct);
    def("dfe_compute_destruct", dfe_compute_destruct);
    def("dfe_compute", dfe_compute);
    def("create_python_impressions", create_python_impressions);
    def("load_impressions", load_impressions);
    def("load_dfes", load_dfes);
}
