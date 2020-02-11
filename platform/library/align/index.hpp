/* idx.hpp ----- James Arram 2016 */

#ifndef IDX_HPP
#define IDX_HPP

#include <stdint.h>
#include "utils.hpp"

/* constant values -- do not change */
#define ALPHA 4 // size of text alphabet (excl. $)
#define SDIST_BASE 64 // sample distance for base FM-index
#define BIT_BASE 3 // bit width for base FM-index BWT
#define SA_SDIST 12  // suffix array sample distance

/* optimised FM-index structure */
#define SDIST_OPT 64 // sample distance for optimised FM-index
#define STEP_SIZE 2 // step size for k-step FM-index
#define BIT_OPT 5 // bit width for optimised FM-index BWT
#define OSAMPLE 1 // oversample factor

// base FM-index structure
struct idxbase_t {
  uint32_t counters[ALPHA];
  uint8_t bwt[CEIL(SDIST_BASE*BIT_BASE,8)];
  uint8_t pad[24];
};

// optimised FM-index structure
struct idxopt_t {
  uint32_t counters[16]; // occurrence counters
  uint8_t bwt[CEIL(SDIST_OPT*BIT_OPT,8)]; // segment of BWT
  uint8_t pad[24]; //optional padding
};

// interval structure
struct ival_t {
  uint32_t low;
  uint32_t high;
};

#endif