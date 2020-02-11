#include <boost/python.hpp>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <vector>
#include <sys/time.h>
#include "index.hpp"
#include "seq.hpp"
#include "match.hpp"
#include "sa.hpp"
#include "file.hpp"
#include <string.h>

max_group_t *global_group;
max_file_t *global_maxfile;

template <class T>
uint64_t input(char *filename, T **a)
{
  FILE *fp = NULL;

  openFile(&fp, filename, "rb"); // open file
  uint64_t f_size = fileSizeBytes(fp); // get file size

  // allocate buffer memory
  *a = new(std::nothrow) T [f_size/sizeof(T)];
  if (*a == NULL) {
    printf("error: unable to allocate memory!\n");
    exit(1);
  }

  readFile(fp, *a, f_size); // read file to buffer
  fclose(fp); // close file

  return f_size; // return file size
}

struct CPUComputeContext{
  idxbase_t *base_idx;
  idxopt_t *opt_idx;
  ssa_t *ssa;
  char *ref;
  uint32_t *lut;
  ival_t **ival;
  std::vector<seq_t> seqs;
  char *buffer;
  uint32_t n_threads;
  uint32_t ssa_len;
  uint32_t lut_end;
  exactout_t *exact_out;
  int volume;
};



idxopt_t *global_opt_idx;
ssa_t *global_ssa;
uint32_t global_ssa_len;

//void read_files(){
//  printf("Reading opt idx and ssa...");
//  input("../../apps/exact_align/data/hg38.fa.fmb", &global_opt_idx);
//  global_ssa_len = input("../../apps/exact_align/data/hg38.fa.ssa", &global_ssa);
//  printf(" done\n");
//}

uint64_t cpu_compute_construct(int volume, uint32_t n_threads, char *file){

  // allocate memeory and initialize compute context struct
  struct CPUComputeContext *context = new CPUComputeContext();

  char fasta[50];
  const char *fasta_ext = ".fa";
  strcpy(fasta, file);
  strcat(fasta, fasta_ext);

  char fastq[50];
  char fastq_ext[20];
  sprintf(fastq_ext, "_%d.fastq", volume);
  strcpy(fastq, file);
  strcat(fastq, fastq_ext);

  context->base_idx = NULL; // base FM-index
  context->opt_idx = NULL; // optimised FM-index
  context->ssa = NULL; // sampled suffix array
  context->ref = NULL; // reference sequence
  context->buffer = NULL; // buffer for FASTQ file

  context->n_threads = n_threads;
  context->volume = volume;

  struct timeval tv1, tv2;

  char filename[128];
  printf("reading FM-index files ... "); fflush(stdout);
  gettimeofday(&tv1, NULL);
/* 
  sprintf(filename, "%s.fma", fasta);
  input(filename, &(context->base_idx));
*/
  sprintf(filename, "%s.fmb", fasta);
  input(filename, &(context->opt_idx));
//  context->opt_idx = global_opt_idx;

  sprintf(filename, "%s.ssa", fasta);
  context->ssa_len = input(filename, &(context->ssa));
//  context->ssa = global_ssa;
//  context->ssa_len = global_ssa_len;
  context->ssa_len /= sizeof(ssa_t);

  sprintf(filename, "%s.ref", fasta);
  input(filename, &(context->ref));

  if (STEP_SIZE > 1) {
    context->ival = new ival_t* [STEP_SIZE-1];
    for (int i = 0; i < STEP_SIZE-1; i++) {
      sprintf(filename, "%s.ival%d", fasta, i+1);
      input(filename, &(context->ival[i]));
    }
  }

  context->lut = new(std::nothrow) uint32_t [(1<<LUT_BITS)+1];
  if (context->lut == NULL) {
    printf("error: unable to allocate memory!\n");
    exit(1);
  }
  context->lut_end = 0;
  buildLUT(context->lut, &(context->lut_end), context->ssa, context->ssa_len);

  gettimeofday(&tv2, NULL);
  printf("done (%.2f s)\n", (double) (tv2.tv_usec - tv1.tv_usec) / 1000000 +
         (double) (tv2.tv_sec - tv1.tv_sec));

  printf("reading sequences from FASTQ file ... "); fflush(stdout);
  gettimeofday(&tv1, NULL);
  uint64_t len = input(fastq, &(context->buffer));
  readSequences(context->seqs, context->buffer, len);

  gettimeofday(&tv2, NULL);
  printf("done (%.2f s)\n", (double) (tv2.tv_usec - tv1.tv_usec) / 1000000 +
         (double) (tv2.tv_sec - tv1.tv_sec));

  context->exact_out = new(std::nothrow) exactout_t [context->seqs.size()];
  if (context->exact_out == NULL) {
    printf("error: unable to allocate memory!\n");
    exit(1);
  }

  return (uint64_t)context;
}


void cpu_compute_destruct(uint64_t c){

  struct CPUComputeContext *context = (struct CPUComputeContext *)c;

  if (STEP_SIZE > 1) {
    for (int i = 0; i < STEP_SIZE-1; i++) {
      delete[] context->ival[i];
    }
    delete[] context->ival;
  }
  delete[] context->base_idx;
  delete[] context->opt_idx;
  delete[] context->ref;
  delete[] context->ssa;
  delete[] context->lut;
  delete[] context->buffer;
  delete[] context->exact_out;
  delete context;

}

void cpu_compute(uint64_t c){

  struct CPUComputeContext *context = (struct CPUComputeContext *)c;

  struct timeval tv1, tv2;

  printf("exact match sequences (%u threads) ... ", context->n_threads); fflush(stdout);
  gettimeofday(&tv1, NULL);
  exactMatch(context->seqs, context->buffer, context->opt_idx, context->ival, context->exact_out, context->n_threads);
  gettimeofday(&tv2, NULL);
  printf("done (%.2f s)\n", (double) (tv2.tv_usec - tv1.tv_usec) / 1000000 +
        (double) (tv2.tv_sec - tv1.tv_sec));

}

void cpu_testbench(uint64_t c){
  
  struct CPUComputeContext *context = (struct CPUComputeContext *)c;
  
  printf("running test bench ... "); fflush(stdout);
  for (uint32_t i = 0; i < context->seqs.size(); i++) {

    // sequence does not match
    if (context->exact_out[i].low > context->exact_out[i].high) {
      printf("failed (1): sequence %u failed to match!\n", i);
      exit(1);
    }

    // test positions
    else {
      uint32_t n_pos = context->exact_out[i].high - context->exact_out[i].low + 1;
      for (uint32_t j = 0; j < n_pos; j++) {
        // convert position in suffix array to text
        uint32_t pos = convertPos(context->exact_out[i].low+j, context->base_idx, context->ssa, context->ssa_len, context->lut, context->lut_end);

        // compare sequence to reference
        if (strncmp(&(context->ref)[pos], &(context->buffer)[context->seqs[i].pos], context->seqs[i].len) != 0) {
          printf("failed (2): sequence %u position incorrect!\n", i);
          exit(1);
        }
      }
    }
  }
  printf("passed\n");

}

void load_dfes(int nproc){
  std::cout << "Loading DFEs: " << nproc << std::endl;
  global_maxfile = ExactMatch_init();
  global_group = max_load_group(global_maxfile, MAXOS_EXCLUSIVE, "*", nproc);
  std::cout << "finished." << std::endl;
}

struct DFEComputeContext{

  idxbase_t *base_idx;
  idxopt_t *opt_idx;
  ssa_t *ssa;
  char *ref;
  uint32_t *lut;
  ival_t *ival;
  std::vector<seq_t> seqs;
  char *buffer;
  uint32_t n_dfes;
  uint32_t ssa_len;
  uint32_t lut_end;
  exactout_t *exact_out;
  uint64_t index_bytes;

  max_file_t *maxfile;
  max_group_t *group;
  max_engine_t **engine;

  int volume;

};

uint64_t dfe_compute_construct(int volume, uint32_t n_dfes, char *file){

  struct DFEComputeContext *context = new DFEComputeContext();

  context->base_idx = NULL; // base FM-index
  context->opt_idx = NULL; // optimised FM-index
  context->ssa = NULL; // sampled suffix array
  context->ref = NULL; // reference sequence
  context->buffer = NULL; // buffer for FASTQ file

  context->maxfile = NULL;
  context->group = NULL;
  context->engine = new max_engine_t *[n_dfes];

  context->n_dfes = n_dfes;
  context->volume = volume;

  char fasta[50];
  const char *fasta_ext = ".fa";
  strcpy(fasta, file);
  strcat(fasta, fasta_ext);

  char fastq[50];
  char fastq_ext[20];
  sprintf(fastq_ext, "_%d.fastq", volume);
  strcpy(fastq, file);
  strcat(fastq, fastq_ext);

  struct timeval tv1, tv2;
  char filename[128];

  printf("reading FM-index files ... "); fflush(stdout);
  gettimeofday(&tv1, NULL);
//  sprintf(filename, "%s.fma", fasta);
//  input(filename, &(context->base_idx));

  sprintf(filename, "%s.fmb", fasta);
  context->index_bytes = input(filename, &(context->opt_idx));

  sprintf(filename, "%s.ssa", fasta);
  context->ssa_len = input(filename, &(context->ssa));
  context->ssa_len /= sizeof(ssa_t);

  sprintf(filename, "%s.ref", fasta);
  input(filename, &(context->ref));

  sprintf(filename, "%s.ival1", fasta);
  input(filename, &(context->ival));  

  context->lut = new(std::nothrow) uint32_t [(1<<LUT_BITS)+1];
  if (context->lut == NULL) {
    printf("error: unable to allocate memory!\n");
    exit(1);
  }
  context->lut_end = 0;
  buildLUT(context->lut, &(context->lut_end), context->ssa, context->ssa_len);

  gettimeofday(&tv2, NULL);
  printf("done (%.2f s)\n", (double) (tv2.tv_usec - tv1.tv_usec) / 1000000 +
         (double) (tv2.tv_sec - tv1.tv_sec));

  printf("initialising maxeler platform ... "); fflush(stdout);
  gettimeofday(&tv1, NULL);
//  context->maxfile = global_maxfile; 
  context->maxfile = ExactMatch_init();
//  context->group = global_group; 
  context->group = max_load_group(context->maxfile, MAXOS_EXCLUSIVE, "*", context->n_dfes);
  for (uint8_t i = 0; i < context->n_dfes; i++) {
    context->engine[i] = max_lock_any(context->group);
  }
  writeIndex(context->opt_idx, context->index_bytes, context->engine, context->n_dfes);
  gettimeofday(&tv2, NULL);
  printf("done (%.2f s)\n", (double) (tv2.tv_usec - tv1.tv_usec) / 1000000 +
         (double) (tv2.tv_sec - tv1.tv_sec));


  printf("reading sequences from FASTQ file ... "); fflush(stdout);
  gettimeofday(&tv1, NULL);
  uint64_t len = input(fastq, &(context->buffer));
  readSequences(context->seqs, context->buffer, len);

  gettimeofday(&tv2, NULL);
  printf("done (%.2f s)\n", (double) (tv2.tv_usec - tv1.tv_usec) / 1000000 +
         (double) (tv2.tv_sec - tv1.tv_sec));

  context->exact_out = new(std::nothrow) exactout_t [context->seqs.size()];
  if (context->exact_out == NULL) {
    printf("error: unable to allocate memory!\n");
    exit(1);
  }

  return (uint64_t)context;
}

void dfe_compute(uint64_t c){

  struct DFEComputeContext *context = (struct DFEComputeContext *)c;

  printf("exact match sequences (%d DFEs) ... ", context->n_dfes); fflush(stdout);
  double time = exactMatchDFE(context->seqs, context->buffer, context->ival, context->exact_out, context->engine, context->n_dfes);
  printf("done (%.2f s)\n", time);

}


void dfe_compute_destruct(uint64_t c){

  struct DFEComputeContext *context = (struct DFEComputeContext *)c;


  // release DFE
  for (uint8_t i = 0; i < context->n_dfes; i++) {
    max_unlock(context->engine[i]);
  }
//  max_unload_group(context->group);
//  max_file_free(context->maxfile);

// cleanup
  delete[] context->base_idx;
  delete[] context->opt_idx;
  delete[] context->ref;
  delete[] context->ssa;
  delete[] context->lut;
  delete[] context->ival;
  delete[] context->buffer;
  delete[] context->exact_out;
  delete context;
}	

void dfe_testbench(uint64_t c){

  struct DFEComputeContext *context = (struct DFEComputeContext *)c;

  printf("running test bench ... "); fflush(stdout);
  for (uint32_t i = 0; i < context->seqs.size(); i++) {

    // sequence does not match
    if (context->exact_out[i].low > context->exact_out[i].high) {
      printf("failed (1): sequence %u failed to match!\n", i);
      exit(1);
    }

    // test positions
    else {
      uint32_t n_pos = context->exact_out[i].high - context->exact_out[i].low + 1;
      for (uint32_t j = 0; j < n_pos; j++) {
        // convert position in suffix array to text
        uint32_t pos = convertPos(context->exact_out[i].low+j, context->base_idx, context->ssa, context->ssa_len, context->lut, context->lut_end);

        // compare sequence to reference
        if (strncmp(&(context->ref)[pos], &(context->buffer)[context->seqs[i].pos], context->seqs[i].len) != 0) {
          printf("failed (2): sequence %u position incorrect!\n", i);
          exit(1);
        }
      }
    }
  }
  printf("passed\n");

}

BOOST_PYTHON_MODULE(align)
{
  using namespace boost::python;
  def("cpu_compute", cpu_compute); 
  def("cpu_compute_construct", cpu_compute_construct); 
  def("cpu_compute_destruct", cpu_compute_destruct);
  def("cpu_testbench", cpu_testbench);
  def("dfe_compute", dfe_compute);
  def("dfe_compute_construct", dfe_compute_construct);
  def("dfe_compute_destruct", dfe_compute_destruct);
  def("dfe_testbench", dfe_testbench);
  def("load_dfes", load_dfes);
//  def("read_files", read_files);
}

