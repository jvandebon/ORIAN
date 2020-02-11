/* seq.hpp ----- James Arram 2017 */

#ifndef SEQ_HPP
#define SEQ_HPP

#include <stdint.h>
#include <vector>
#include "index.hpp"
#include "sa.hpp"

// sequence structure
struct seq_t {
  uint64_t pos; // sequence start position
  uint8_t len; // sequence length
 
  // constructors
  seq_t(){};
  seq_t(uint64_t _pos, uint8_t _len)
  {
    pos = _pos;
    len = _len;
  }
};

/*
 * Function: readSequences
 * -----------------------
 *
 * read sequences from FASTQ file
 * 
 * [input]
 * seq - container for sequences
 * buffer - buffer containing FASTQ file
 * len - buffer length
 *
 */
void readSequences(std::vector<seq_t> &seqs, char *buffer, uint64_t len);

#endif