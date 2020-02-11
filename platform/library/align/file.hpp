/* file.hpp ----- James Arram 2015 */

/*
 * file utilities
 */

#ifndef FILE_HPP
#define FILE_HPP

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>

/*
 * Function: openFile
 * ---------------------
 *
 * open file 
 * 
 * [input]
 * fp - file pointer
 * f_name - file name
 * mode - file open mode
 */
void openFile(FILE **fp, char *f_name, const char *mode);

/*
 * Function: fileSizeBytes
 * ---------------------
 *
 * get file size in bytes
 * 
 * [input]
 * fp - file pointer
 */
uint64_t fileSizeBytes(FILE *fp);

/*
 * Function: readFile
 * ---------------------
 *
 * read bytes from file
 * 
 * [input]
 * fp - file pointer
 * a - buffer to read into
 * size - number of bytes to read
 */
void readFile(FILE *fp, void  *a, uint64_t size);

/*
 * Function: writeFile
 * ---------------------
 *
 * write bytes to file
 * 
 * [input]
 * fp - file pointer
 * a - buffer to write from
 * size - number of bytes to write
 */
void writeFile(FILE *fp, void *a, uint64_t size);

#endif