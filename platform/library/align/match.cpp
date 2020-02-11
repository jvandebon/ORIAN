/* match.cpp ----- James Arram 2017 */

#include "match.hpp"
#include <stdio.h>
#include<sys/time.h>

/*
 * Function: exactMatchUtil
 * ------------------------
 *
 * exact match utility function
 * 
 * [input]
 * sym - sequence characters
 * len - sequence length
 * idx - FM-index
 * ival - precomputed intervals
 *
 */
void exactMatchUtil(char *sym, uint8_t len, idxopt_t *idx, ival_t **ival,
		    exactout_t *exact_out)
{
  
  // initialise interval for remainder characters
  uint32_t offset = len%STEP_SIZE;
  uint8_t val_init = 0;
  for (uint32_t i = 0; i < offset; i++) {
    int mult = 1<<(i*2);
    switch (sym[len-i-1]) {
    case 'A' : val_init += 0*mult; break;
    case 'C' : val_init += 1*mult; break;
    case 'G' : val_init += 2*mult; break;
    case 'T' : val_init += 3*mult; break;
    default : val_init += 0*mult; // default to 'A'
    }
  }

  uint32_t low = offset == 0 ? 0 : ival[offset-1][val_init].low;
  uint32_t high = offset == 0 ? ival[0][3].high : ival[offset-1][val_init].high;
 
  for (uint32_t i = offset; i < len; i+=STEP_SIZE) {
    
    // get sequence character
    uint8_t val = 0;
    for (int j = 0; j < STEP_SIZE; j++) {
      int mult = 1<<(j*2);
      switch (sym[len-i-j-1]) {
      case 'A' : val += 0*mult; break;
      case 'C' : val += 1*mult; break;
      case 'G' : val += 2*mult; break;
      case 'T' : val += 3*mult; break;
      default : val += 0*mult; // default to 'A'
      }
    }
    
    uint32_t low_tmp = low == 0 ? 0 : low - 1;
    uint32_t low_addr = low_tmp/SDIST_OPT;
    uint32_t high_addr = high/SDIST_OPT;
    
    // update low
    uint32_t low_idx = low_tmp%SDIST_OPT;
    uint32_t low_counter = idx[low_addr].counters[val];
    uint32_t low_count = getOcc(val, idx[low_addr].bwt, 0, low_idx, BIT_OPT);
    low = low == 0 ? low_counter : low_counter + low_count;
    
    // update high
    uint32_t high_idx = high%SDIST_OPT;
    if (low_addr == high_addr) {
      high = low_counter + low_count + 
	getOcc(val, idx[low_addr].bwt, low_idx+1, high_idx, BIT_OPT) - 1;
    }   
    else {
      high = idx[high_addr].counters[val] + 
	getOcc(val, idx[high_addr].bwt, 0, high_idx, BIT_OPT) - 1;
    }

    if (low > high)
      break;
  }

  // store final interval
  (*exact_out).low = low;
  (*exact_out).high = high;  
}

// exact match sequences
void exactMatch(std::vector<seq_t> &seqs, char *buffer, idxopt_t *idx, 
		ival_t **ival, exactout_t *exact_out, uint32_t n_threads)
{
 
#pragma omp parallel for num_threads(n_threads)
  for (uint32_t i = 0; i < seqs.size(); i++) {
    exactMatchUtil(&buffer[seqs[i].pos], seqs[i].len, idx, ival, &exact_out[i]);
  }
}

/*
 * Function: set2bit
 * ------------------
 *
 * set 2-bit value
 *
 * [input]
 * pck - buffer for packed values
 * idx - value index
 * val - 2-bit value
 *
 */
inline void set2bit(uint8_t *pck, uint32_t idx, uint8_t val);

/*
 * Function: packSymbols
 * ------------------
 *
 * pack sequence symbols
 *
 * [input]
 * pck - buffer for packed values
 * sym - sequence symbols
 * len - sequence length
 *
 */
void packSymbols(uint8_t *pck, char *sym, uint8_t len);

/*
 * Function: getPartitionSizes
 * ------------------
 *
 *
 * get partition sizes
 *
 * [input]
 * part_size - partition sizes
 * items - number of data items
 * parts - number of paritions
 *
 */
void getPartitionSizes(uint32_t *part_size, uint32_t items, uint32_t parts);

// exact match sequences
double exactMatchDFE(std::vector<seq_t> &seqs, char *buffer, ival_t *ival,
                  exactout_t *exact_out, max_engine_t **engine, uint32_t n_dfes)
{
  kin_t *in[n_dfes*6];
  kout_t *out[n_dfes*6];
  uint32_t part_size[n_dfes*6];
  uint32_t n_threads = omp_get_max_threads();

  // generate kernel input
  getPartitionSizes(part_size, seqs.size(), n_dfes*6);
  uint32_t offset = 0;
  for (uint32_t i = 0; i < n_dfes*6; i++) {
    in[i] = new(std::nothrow) kin_t [part_size[i] + BATCH];
    if (in[i] == NULL) {
      printf("error: unable to allocate memory for kernel input!\n");
      exit(1);
    }
    memset(in[i], 0, (part_size[i]+BATCH)*sizeof(kin_t));
#pragma omp parallel for num_threads(n_threads)
    for (uint32_t j = 0; j < part_size[i]; j++) {
      uint32_t k = j+offset;
      in[i][j].id = k;
      in[i][j].len = seqs[k].len;
      packSymbols(in[i][j].pck_sym, &buffer[seqs[k].pos], seqs[k].len);
      in[i][j].is_pad = 0;
    }
    for (uint32_t j = 0; j < BATCH; j++)
      in[i][part_size[i]+j].is_pad = 1;
    offset += part_size[i];
  }

  // run alignment
  for (uint32_t i = 0; i < n_dfes*6; i++) {
    out[i] = new(std::nothrow) kout_t [part_size[i]];
    if (out[i] == NULL) {
      printf("error: unable to allocate memory for kernel output!\n");
      exit(1);
    }
  }
  struct timeval  tv1, tv2;
  gettimeofday(&tv1, NULL);
  runDFE(in, out, part_size, ival, engine, n_dfes);
  gettimeofday(&tv2, NULL);
  double time = (double) (tv2.tv_usec - tv1.tv_usec) / 1000000 +
    (double) (tv2.tv_sec - tv1.tv_sec);

  // parse output
#pragma omp parallel for num_threads(n_threads)
  for (uint32_t i = 0; i < n_dfes*6; i++) {
    for (uint32_t j = 0; j < part_size[i]; j++) {
      uint32_t id = out[i][j].id;
      exact_out[id].low = out[i][j].low;
      exact_out[id].high = out[i][j].high;
    }
  }

  // cleanup
  for (uint32_t i = 0; i < n_dfes*6; i++) {
    delete[] in[i];
    delete[] out[i];
  }

  return time;
}

// get partition sizes
void getPartitionSizes(uint32_t *part_size, uint32_t items, uint32_t parts)
{
  for (uint32_t i = 0; i < parts; i++) {
    if (items % parts != 0) {
      part_size[i] = CEIL(items, parts);
      items-=1;
    }
    else
      part_size[i] = items/parts;
  }
}

// pack sequence symbols
void packSymbols(uint8_t *pck, char *sym, uint8_t len)
{
  for (uint8_t i = 0; i < len; i++) {
    switch(sym[len-1-i]) {
    case 'A': set2bit(pck, i, 0); break;
    case 'C': set2bit(pck, i, 1); break;
    case 'G': set2bit(pck, i, 2); break;
    case 'T': set2bit(pck, i, 3); break;
    default : set2bit(pck, i, 0);
    }
  }
}

// set 2 bit value
inline void set2bit(uint8_t *pck, uint32_t idx, uint8_t val)
{
  uint8_t tmp = val << ((idx << 1) & 0x7);
  pck[idx >> 2] |= tmp;
}
