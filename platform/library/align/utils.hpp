/* utils.hpp ----- James Arram 2017 */

/*
 * utility functions
 */

#ifndef UTILS_HPP
#define UTILS_HPP

#include <stdint.h>

// ceiling macro
#define CEIL(a, b) (((a) + (b) - 1) / (b))

/*
 * Function: reverse
 * ---------------------
 *
 * reverse string
 * 
 * [input]
 * str - string
 * len - string length
 */
void reverse(char *str, uint32_t len);

/*
 * Function: sum
 * ---------------
 *
 * sum array
 * 
 * [input]
 * a - array
 * n - array size
 */
uint32_t sum(uint32_t *a, int n);

/*
 * Function: setVal
 * ----------------
 *
 * set value in packed bwt
 * 
 * [input]
 * bwt - bwt buffer
 * idx - position of character in bwt
 * val - character value
 * bit_width - number of bits per character [<8]
 */
void setVal(uint8_t *bwt, uint32_t idx, uint8_t val, uint8_t bit_width);

/*
 * Function: getVal
 * ----------------
 *
 * get value in packed bwt
 * 
 * [input]
 * bwt - bwt buffer
 * idx - position of character in bwt
 * bit_width - number of bits per character [<8]
 * 
 * [return]
 * bwt character
 */
uint8_t getVal(uint8_t *bwt, uint32_t idx, uint8_t bit_width);

/*
 * Function: getOcc
 * ----------------
 *
 * count occurrence of character in bwt
 * 
 * [input]
 * sym - character to count occurrence of
 * bwt - bwt buffer
 * s_pos - start position
 * e_pos - end position
 * bit_width - number of bits per character [<8]
 *
 * [return]
 * occurrence of character
 */
uint32_t getOcc(uint8_t sym, uint8_t *bwt, uint32_t s_pos, uint32_t e_pos, 
		uint8_t bit_width);

#endif