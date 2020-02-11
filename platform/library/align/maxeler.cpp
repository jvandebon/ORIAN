/* maxeler.cpp ----- James Arram 2017 */

#include "maxeler.hpp"

// run alignment command
void runDFE(kin_t **in, kout_t **out, uint32_t *part_size, ival_t *ival,
	    max_engine_t **engine, uint32_t n_dfes)
{
  uint64_t n_bytes_in[n_dfes*6];
  uint64_t n_bytes_out[n_dfes*6];
  for (uint32_t i = 0; i < n_dfes*6; i++) {
    n_bytes_in[i] = (part_size[i]+BATCH)*sizeof(kin_t);
    n_bytes_out[i] = part_size[i]*sizeof(kout_t);
  }
  
  ExactMatch_Align_actions_t *em_align[n_dfes];
  for (uint32_t i = 0; i < n_dfes; i++) {
    em_align[i] = new ExactMatch_Align_actions_t;
    em_align[i]->param_loopOffset = BATCH*2;
    em_align[i]->param_ivals = (uint64_t*)ival;
    em_align[i]->param_nBytesIn = &n_bytes_in[i*6];
    em_align[i]->param_nBytesOut = &n_bytes_out[i*6];
    
    // kernel 1 I/O
    em_align[i]->instream_seqIn0 = (uint64_t*)in[i*6];
    em_align[i]->outstream_alignOut0 = (uint64_t*)out[i*6];

    // kernel 2 I/O
    em_align[i]->instream_seqIn1 = (uint64_t*)in[(i*6)+1];
    em_align[i]->outstream_alignOut1 = (uint64_t*)out[(i*6)+1];

    // kernel 3 I/O
    em_align[i]->instream_seqIn2 = (uint64_t*)in[(i*6)+2];
    em_align[i]->outstream_alignOut2 = (uint64_t*)out[(i*6)+2];

    // kernel 4 I/O
    em_align[i]->instream_seqIn3 = (uint64_t*)in[(i*6)+3];
    em_align[i]->outstream_alignOut3 = (uint64_t*)out[(i*6)+3];
    
    // kernel 5 I/O
    em_align[i]->instream_seqIn4 = (uint64_t*)in[(i*6)+4];
    em_align[i]->outstream_alignOut4 = (uint64_t*)out[(i*6)+4];

    // kernel 6 I/O
    em_align[i]->instream_seqIn5 = (uint64_t*)in[(i*6)+5];
    em_align[i]->outstream_alignOut5 = (uint64_t*)out[(i*6)+5];
  }
#pragma omp parallel for num_threads(n_dfes)
  for (uint32_t i = 0; i < n_dfes; i++) {
    ExactMatch_Align_run(engine[i], em_align[i]);
    delete em_align[i];
  }
}

// write FM-index to LMem
void writeIndex(idxopt_t *idx, uint64_t index_bytes,  max_engine_t **engine, uint32_t n_dfes)
{
  ExactMatch_Write_actions_t *em_write[n_dfes];
  for (uint32_t i = 0; i < n_dfes; i++) {
    em_write[i] = new ExactMatch_Write_actions_t;
    em_write[i]->param_nBytes = index_bytes;
    em_write[i]->param_offset = 0;
    em_write[i]->instream_indexToMger = (uint64_t*)idx;
  }
#pragma omp parallel for num_threads(n_dfes)
  for (uint32_t i = 0; i < n_dfes; i++) {
    ExactMatch_Write_run(engine[i], em_write[i]);
    delete em_write[i];
  }
}

