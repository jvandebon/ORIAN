/* sa.hpp ----- James Arram 2017 */

/*
 * functions to query sampled suffix array
 */

#ifndef SA_HPP
#define SA_HPP

#include <stdint.h>
#include "index.hpp"
#include "utils.hpp"

#define LUT_BITS 24

// sampled suffix array structure
struct ssa_t {
  uint32_t sa_pos; // index in suffix array 
  uint32_t t_pos; // position in text
};

/*
 * Function: buildLUT
 * ---------------------
 *
 * build look-up table for sampled suffix array
 * 
 * [input]
 * lut - look-up table
 * lut_end - last populated entry in look-up table
 * ssa - sampled suffix array
 * ssa_len - length of suffix array
 *
 */
void buildLUT(uint32_t *lut, uint32_t *lut_end, ssa_t *ssa, uint32_t ssa_len);

/*
 * Function: convertPos
 * ---------------------
 *
 * convert position in suffix array to text
 * 
 * [input]
 * pos - position in suffix array 
 * idx - base FM-index
 * ssa - sampled suffix array
 * ssa_len - length of suffix array
 * lut - look-up table
 * lut_end - last populated entry in look-up table
 * 
 * [return]
 * position in text
 *
 */
uint32_t convertPos(uint32_t pos, idxbase_t *idx, ssa_t *ssa, uint32_t ssa_len, 
		    uint32_t *lut, uint32_t lut_end);

#endif