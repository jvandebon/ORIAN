/* utils.cpp ----- James Arram 2017 */

#include "utils.hpp"

// reverse string
void rev(char *str, uint32_t len)
{
  char *p1 = str;
  char *p2 = &str[len-1];
  char tmp;

  while (p2 > p1) {
    tmp = *p1;
    *p1++ = *p2;
    *p2-- = tmp;
  }
}

// sum array
uint32_t sum(uint32_t *a, int n)
{
  uint32_t cnt = 0;
  
  for (int i = 0; i < n; i++)
    cnt += a[i];
  
  return cnt;
}

// set value in packed bwt
void setVal(uint8_t *bwt, uint32_t idx, uint8_t val, uint8_t bit_width)
{
  uint16_t tmp = val << ((idx*bit_width)%8);
  bwt[(idx*bit_width)/8] |= (uint8_t) tmp;
  bwt[((idx*bit_width)/8)+1] |= (uint8_t) (tmp>>8);
}

// get value from packed bwt
uint8_t getVal(uint8_t *bwt, uint32_t idx, uint8_t bit_width)
{
  uint16_t tmp = (((uint16_t)bwt[((idx*bit_width)/8)+1]) << 8) | bwt[(idx*bit_width)/8];
  tmp = (tmp >> ((idx*bit_width)%8)) & ((1 << bit_width) - 1);

  return tmp;
}

// count occurrence from bwt
uint32_t getOcc(uint8_t sym, uint8_t *bwt, uint32_t s_pos, uint32_t e_pos, 
		uint8_t bit_width)
{
  uint32_t count = 0;
  
  for (uint32_t i = s_pos; i <= e_pos; i++) {
    uint8_t bwt_sym = getVal(bwt, i, bit_width);
    if (sym == bwt_sym) {
      count += 1;
    }
  }
  return count;
}
