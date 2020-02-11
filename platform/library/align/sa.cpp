/* sa.cpp ----- James Arram 2017 */

#include "sa.hpp"

/*
 * Function: search
 * -----------------
 *
 * search for pos in sampled suffix array using binary search
 * 
 * [input]
 * pos - position to find
 * ssa - sampled suffix array
 * ssa_len - length of suffix array
 * l - lower bound positon
 * r - upper bound position
 *
 * [return]
 * position if occurs, else -1
 *
 */ 
int64_t search(uint32_t pos, ssa_t *ssa, uint32_t l, uint32_t r)
{
  while (l <= r) {
    
    uint32_t m = l + ((r-l)/2);
      
    if (pos < ssa[m].sa_pos) {
      if (m > 0)
	r = m - 1;
      else
	return -1;
    }
    
    else if (pos > ssa[m].sa_pos)
      l = m + 1;
    
    else 
      return m;
  }
  
  return -1;
}

// build look-up table for sampled suffix array
void buildLUT(uint32_t *lut, uint32_t *lut_end, ssa_t *ssa, uint32_t ssa_len)
{
  uint32_t lut_len = (1<<LUT_BITS)+1;
  uint32_t thresh = 0;
  uint32_t last = 0;

  for (uint32_t i = 0; i < ssa_len-1; i++) {
    uint32_t next_thresh = ssa[i+1].sa_pos>>(32-LUT_BITS);
    lut[thresh] = last;

      if (next_thresh > thresh) {
	  last = i+1;
	  for (uint32_t j = thresh+1; j <= next_thresh; j++)
	    lut[j] = last;
      }	  
      thresh = next_thresh;
    }

  for (uint32_t i = thresh; i < lut_len-1; i++) {
    lut[i] = last;
  }

  *lut_end = thresh;
}

// convert position in suffix array to text
uint32_t convertPos(uint32_t pos, idxbase_t *idx, ssa_t *ssa, uint32_t ssa_len, 
		    uint32_t *lut, uint32_t lut_end)
{
  uint32_t step = 0;

  while (1) {
    uint32_t lut_idx = pos>>(32-LUT_BITS);
    uint32_t l = lut[lut_idx];
    uint32_t r = lut_idx+1 >= lut_end ? ssa_len-1 : lut[lut_idx+1]-1;
    int64_t i = search(pos, ssa, l, r);
    
    // position not stored in sampled suffix array
    if (i == -1) {
      
      // get bwt character @ position     
      uint8_t sym = getVal(idx[pos/SDIST_BASE].bwt, pos%SDIST_BASE, BIT_BASE);
      
      // LF-Mapping
      uint32_t pos_tmp = pos == 0 ? 0 : pos - 1;
      uint32_t counter = idx[pos_tmp/SDIST_BASE].counters[sym];
      uint32_t count = getOcc(sym, idx[pos_tmp/SDIST_BASE].bwt, 0, pos_tmp%SDIST_BASE, BIT_BASE);
      pos = pos == 0 ? counter : counter + count;
      step += 1;
    }
    
    // position exists in sampled suffix array
    else {
      return ssa[i].t_pos + step;
    }
  }
}