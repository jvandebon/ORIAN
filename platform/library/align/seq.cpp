/* seq.cpp ----- James Arram 2016 */

#include "seq.hpp"

// read sequences from FASTQ file
void readSequences(std::vector<seq_t> &seqs, char *buffer, uint64_t len)
{
  uint64_t i = 0; // current position in buffer
  uint64_t start = 0; // start position of line 
  uint64_t line_count = 0; // line counter
  while (i < len) {
    if (buffer[i] == '\n') {
      if (line_count%4 == 1) // sequences are stored on second line in FASTQ entry
	seqs.emplace_back(start, i-start);
      start = i+1;
      line_count++;
    }
    i++;
  }
}