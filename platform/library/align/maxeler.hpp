/* maxeler.hpp ----- James Arram 2017 */

/*
 * utilities to run slic commands
 */

#ifndef MAXELER_HPP
#define MAXELER_HPP

#include <stdint.h>
#include <omp.h>
#include "index.hpp"
#include <MaxSLiCInterface.h>
#include "ExactMatch.h"


//#ifndef N_DFE
//#define N_DFE 1
//#endif
#define BATCH 200

// kernel input
struct kin_t {
  uint32_t id;
  uint8_t pck_sym[58];
  uint8_t len;
  uint8_t is_pad;
};

// kernel output
struct kout_t {
  uint32_t id;
  uint32_t low;
  uint32_t high;
  uint32_t pad;
};

/*
 * Function: runDFE
 * ---------------------
 *
 * run alignment interface
 * 
 * [input]
 * kin - kernel input
 * kout - kernel output
 * part_size - data partition sizes
 * ival - precomputed intervals
 * engine - maxeler engine loaded with bitstream
 * 
 */
void runDFE(kin_t **in, kout_t **out, uint32_t *part_size, ival_t *ival,
	    max_engine_t **engine, uint32_t n_dfes);


/*
 * Function: writeIndex
 * ---------------------
 *
 * write FM-index to LMem
 * 
 * [input]
 * idx - FM-index
 * index_bytes - size of index in bytes
 * engine - maxeler engine loaded with bitstream
 *
 */
void writeIndex(idxopt_t *idx, uint64_t index_bytes,  max_engine_t **engine, uint32_t n_dfes);

#endif
