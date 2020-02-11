/* match.hpp ----- James Arram 2017 */

/*
 * string matching functions
 */

#ifndef MATCH_HPP
#define MATCH_HPP

#include <stdint.h>
#include <omp.h>
#include <vector>
#include "seq.hpp"
#include "index.hpp"
#include "utils.hpp"
#include "maxeler.hpp"
#include <string.h>
#include <cmath>

// exact match output structure
struct exactout_t {
  uint32_t low;
  uint32_t high;  
};

/*
 * Function: exactMatch
 * ---------------------
 *
 * exact match sequences
 * 
 * [input]
 * seqs - sequences to match
 * buffer - buffer containing FASTQ file
 * idx1step - FM-index
 * ival - precomputed intervals
 * exact_out - final interval of match
 *
 */
void exactMatch(std::vector<seq_t> &seqs, char *buffer, idxopt_t *idx, 
		ival_t **ival, exactout_t *exact_out, uint32_t n_threads);

/*
 * Function: exactMatchDFE
 * ---------------------
 *
 * exact match sequences
 *
 * [input]
 * seqs - sequences to match
 * buffer - buffer containing FASTQ file
 * ival - precomputed intervals
 * exact_out - final interval of match
 * engine - maxeler engine loaded with bitstream
 * n_dfe - number of DFEs targeted
 *
 */
double exactMatchDFE(std::vector<seq_t> &seqs, char *buffer, ival_t *ival,
                  exactout_t *exact_out, max_engine_t **engine, uint32_t n_dfes);

#endif
