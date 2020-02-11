/**\file */
#ifndef SLIC_DECLARATIONS_ExactMatch_H
#define SLIC_DECLARATIONS_ExactMatch_H
#include "MaxSLiCInterface.h"
#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */



/*----------------------------------------------------------------------------*/
/*----------------------------- Interface Align ------------------------------*/
/*----------------------------------------------------------------------------*/




/**
 * \brief Basic static function for the interface 'Align'.
 * 
 * \param [in] param_loopOffset Interface Parameter "loopOffset".
 * \param [in] param_ivals Interface Parameter array ivals[] should be of size 4.
 * \param [in] param_nBytesIn Interface Parameter array nBytesIn[] should be of size 6.
 * \param [in] param_nBytesOut Interface Parameter array nBytesOut[] should be of size 6.
 * \param [in] instream_seqIn0 The stream should be of size param_nBytesIn[0] bytes.
 * \param [in] instream_seqIn1 The stream should be of size param_nBytesIn[1] bytes.
 * \param [in] instream_seqIn2 The stream should be of size param_nBytesIn[2] bytes.
 * \param [in] instream_seqIn3 The stream should be of size param_nBytesIn[3] bytes.
 * \param [in] instream_seqIn4 The stream should be of size param_nBytesIn[4] bytes.
 * \param [in] instream_seqIn5 The stream should be of size param_nBytesIn[5] bytes.
 * \param [out] outstream_alignOut0 The stream should be of size param_nBytesOut[0] bytes.
 * \param [out] outstream_alignOut1 The stream should be of size param_nBytesOut[1] bytes.
 * \param [out] outstream_alignOut2 The stream should be of size param_nBytesOut[2] bytes.
 * \param [out] outstream_alignOut3 The stream should be of size param_nBytesOut[3] bytes.
 * \param [out] outstream_alignOut4 The stream should be of size param_nBytesOut[4] bytes.
 * \param [out] outstream_alignOut5 The stream should be of size param_nBytesOut[5] bytes.
 */
void ExactMatch_Align(
	uint32_t param_loopOffset,
	const uint64_t *param_ivals,
	const uint64_t *param_nBytesIn,
	const uint64_t *param_nBytesOut,
	const uint64_t *instream_seqIn0,
	const uint64_t *instream_seqIn1,
	const uint64_t *instream_seqIn2,
	const uint64_t *instream_seqIn3,
	const uint64_t *instream_seqIn4,
	const uint64_t *instream_seqIn5,
	uint64_t *outstream_alignOut0,
	uint64_t *outstream_alignOut1,
	uint64_t *outstream_alignOut2,
	uint64_t *outstream_alignOut3,
	uint64_t *outstream_alignOut4,
	uint64_t *outstream_alignOut5);

/**
 * \brief Basic static non-blocking function for the interface 'Align'.
 * 
 * Schedule to run on an engine and return immediately.
 * The status of the run can be checked either by ::max_wait or ::max_nowait;
 * note that one of these *must* be called, so that associated memory can be released.
 * 
 * 
 * \param [in] param_loopOffset Interface Parameter "loopOffset".
 * \param [in] param_ivals Interface Parameter array ivals[] should be of size 4.
 * \param [in] param_nBytesIn Interface Parameter array nBytesIn[] should be of size 6.
 * \param [in] param_nBytesOut Interface Parameter array nBytesOut[] should be of size 6.
 * \param [in] instream_seqIn0 The stream should be of size param_nBytesIn[0] bytes.
 * \param [in] instream_seqIn1 The stream should be of size param_nBytesIn[1] bytes.
 * \param [in] instream_seqIn2 The stream should be of size param_nBytesIn[2] bytes.
 * \param [in] instream_seqIn3 The stream should be of size param_nBytesIn[3] bytes.
 * \param [in] instream_seqIn4 The stream should be of size param_nBytesIn[4] bytes.
 * \param [in] instream_seqIn5 The stream should be of size param_nBytesIn[5] bytes.
 * \param [out] outstream_alignOut0 The stream should be of size param_nBytesOut[0] bytes.
 * \param [out] outstream_alignOut1 The stream should be of size param_nBytesOut[1] bytes.
 * \param [out] outstream_alignOut2 The stream should be of size param_nBytesOut[2] bytes.
 * \param [out] outstream_alignOut3 The stream should be of size param_nBytesOut[3] bytes.
 * \param [out] outstream_alignOut4 The stream should be of size param_nBytesOut[4] bytes.
 * \param [out] outstream_alignOut5 The stream should be of size param_nBytesOut[5] bytes.
 * \return A handle on the execution status, or NULL in case of error.
 */
max_run_t *ExactMatch_Align_nonblock(
	uint32_t param_loopOffset,
	const uint64_t *param_ivals,
	const uint64_t *param_nBytesIn,
	const uint64_t *param_nBytesOut,
	const uint64_t *instream_seqIn0,
	const uint64_t *instream_seqIn1,
	const uint64_t *instream_seqIn2,
	const uint64_t *instream_seqIn3,
	const uint64_t *instream_seqIn4,
	const uint64_t *instream_seqIn5,
	uint64_t *outstream_alignOut0,
	uint64_t *outstream_alignOut1,
	uint64_t *outstream_alignOut2,
	uint64_t *outstream_alignOut3,
	uint64_t *outstream_alignOut4,
	uint64_t *outstream_alignOut5);

/**
 * \brief Advanced static interface, structure for the engine interface 'Align'
 * 
 */
typedef struct { 
	uint32_t param_loopOffset; /**<  [in] Interface Parameter "loopOffset". */
	const uint64_t *param_ivals; /**<  [in] Interface Parameter array ivals[] should be of size 4. */
	const uint64_t *param_nBytesIn; /**<  [in] Interface Parameter array nBytesIn[] should be of size 6. */
	const uint64_t *param_nBytesOut; /**<  [in] Interface Parameter array nBytesOut[] should be of size 6. */
	const uint64_t *instream_seqIn0; /**<  [in] The stream should be of size param_nBytesIn[0] bytes. */
	const uint64_t *instream_seqIn1; /**<  [in] The stream should be of size param_nBytesIn[1] bytes. */
	const uint64_t *instream_seqIn2; /**<  [in] The stream should be of size param_nBytesIn[2] bytes. */
	const uint64_t *instream_seqIn3; /**<  [in] The stream should be of size param_nBytesIn[3] bytes. */
	const uint64_t *instream_seqIn4; /**<  [in] The stream should be of size param_nBytesIn[4] bytes. */
	const uint64_t *instream_seqIn5; /**<  [in] The stream should be of size param_nBytesIn[5] bytes. */
	uint64_t *outstream_alignOut0; /**<  [out] The stream should be of size param_nBytesOut[0] bytes. */
	uint64_t *outstream_alignOut1; /**<  [out] The stream should be of size param_nBytesOut[1] bytes. */
	uint64_t *outstream_alignOut2; /**<  [out] The stream should be of size param_nBytesOut[2] bytes. */
	uint64_t *outstream_alignOut3; /**<  [out] The stream should be of size param_nBytesOut[3] bytes. */
	uint64_t *outstream_alignOut4; /**<  [out] The stream should be of size param_nBytesOut[4] bytes. */
	uint64_t *outstream_alignOut5; /**<  [out] The stream should be of size param_nBytesOut[5] bytes. */
} ExactMatch_Align_actions_t;

/**
 * \brief Advanced static function for the interface 'Align'.
 * 
 * \param [in] engine The engine on which the actions will be executed.
 * \param [in,out] interface_actions Actions to be executed.
 */
void ExactMatch_Align_run(
	max_engine_t *engine,
	ExactMatch_Align_actions_t *interface_actions);

/**
 * \brief Advanced static non-blocking function for the interface 'Align'.
 *
 * Schedule the actions to run on the engine and return immediately.
 * The status of the run can be checked either by ::max_wait or ::max_nowait;
 * note that one of these *must* be called, so that associated memory can be released.
 *
 * 
 * \param [in] engine The engine on which the actions will be executed.
 * \param [in] interface_actions Actions to be executed.
 * \return A handle on the execution status of the actions, or NULL in case of error.
 */
max_run_t *ExactMatch_Align_run_nonblock(
	max_engine_t *engine,
	ExactMatch_Align_actions_t *interface_actions);

/**
 * \brief Group run advanced static function for the interface 'Align'.
 * 
 * \param [in] group Group to use.
 * \param [in,out] interface_actions Actions to run.
 *
 * Run the actions on the first device available in the group.
 */
void ExactMatch_Align_run_group(max_group_t *group, ExactMatch_Align_actions_t *interface_actions);

/**
 * \brief Group run advanced static non-blocking function for the interface 'Align'.
 * 
 *
 * Schedule the actions to run on the first device available in the group and return immediately.
 * The status of the run must be checked with ::max_wait. 
 * Note that use of ::max_nowait is prohibited with non-blocking running on groups:
 * see the ::max_run_group_nonblock documentation for more explanation.
 *
 * \param [in] group Group to use.
 * \param [in] interface_actions Actions to run.
 * \return A handle on the execution status of the actions, or NULL in case of error.
 */
max_run_t *ExactMatch_Align_run_group_nonblock(max_group_t *group, ExactMatch_Align_actions_t *interface_actions);

/**
 * \brief Array run advanced static function for the interface 'Align'.
 * 
 * \param [in] engarray The array of devices to use.
 * \param [in,out] interface_actions The array of actions to run.
 *
 * Run the array of actions on the array of engines.  The length of interface_actions
 * must match the size of engarray.
 */
void ExactMatch_Align_run_array(max_engarray_t *engarray, ExactMatch_Align_actions_t *interface_actions[]);

/**
 * \brief Array run advanced static non-blocking function for the interface 'Align'.
 * 
 *
 * Schedule to run the array of actions on the array of engines, and return immediately.
 * The length of interface_actions must match the size of engarray.
 * The status of the run can be checked either by ::max_wait or ::max_nowait;
 * note that one of these *must* be called, so that associated memory can be released.
 *
 * \param [in] engarray The array of devices to use.
 * \param [in] interface_actions The array of actions to run.
 * \return A handle on the execution status of the actions, or NULL in case of error.
 */
max_run_t *ExactMatch_Align_run_array_nonblock(max_engarray_t *engarray, ExactMatch_Align_actions_t *interface_actions[]);

/**
 * \brief Converts a static-interface action struct into a dynamic-interface max_actions_t struct.
 *
 * Note that this is an internal utility function used by other functions in the static interface.
 *
 * \param [in] maxfile The maxfile to use.
 * \param [in] interface_actions The interface-specific actions to run.
 * \return The dynamic-interface actions to run, or NULL in case of error.
 */
max_actions_t* ExactMatch_Align_convert(max_file_t *maxfile, ExactMatch_Align_actions_t *interface_actions);



/*----------------------------------------------------------------------------*/
/*----------------------------- Interface Write ------------------------------*/
/*----------------------------------------------------------------------------*/




/**
 * \brief Basic static function for the interface 'Write'.
 * 
 * \param [in] param_nBytes Interface Parameter "nBytes".
 * \param [in] param_offset Interface Parameter "offset".
 * \param [in] instream_indexToMger The stream should be of size param_nBytes bytes.
 */
void ExactMatch_Write(
	uint64_t param_nBytes,
	uint64_t param_offset,
	const uint64_t *instream_indexToMger);

/**
 * \brief Basic static non-blocking function for the interface 'Write'.
 * 
 * Schedule to run on an engine and return immediately.
 * The status of the run can be checked either by ::max_wait or ::max_nowait;
 * note that one of these *must* be called, so that associated memory can be released.
 * 
 * 
 * \param [in] param_nBytes Interface Parameter "nBytes".
 * \param [in] param_offset Interface Parameter "offset".
 * \param [in] instream_indexToMger The stream should be of size param_nBytes bytes.
 * \return A handle on the execution status, or NULL in case of error.
 */
max_run_t *ExactMatch_Write_nonblock(
	uint64_t param_nBytes,
	uint64_t param_offset,
	const uint64_t *instream_indexToMger);

/**
 * \brief Advanced static interface, structure for the engine interface 'Write'
 * 
 */
typedef struct { 
	uint64_t param_nBytes; /**<  [in] Interface Parameter "nBytes". */
	uint64_t param_offset; /**<  [in] Interface Parameter "offset". */
	const uint64_t *instream_indexToMger; /**<  [in] The stream should be of size param_nBytes bytes. */
} ExactMatch_Write_actions_t;

/**
 * \brief Advanced static function for the interface 'Write'.
 * 
 * \param [in] engine The engine on which the actions will be executed.
 * \param [in,out] interface_actions Actions to be executed.
 */
void ExactMatch_Write_run(
	max_engine_t *engine,
	ExactMatch_Write_actions_t *interface_actions);

/**
 * \brief Advanced static non-blocking function for the interface 'Write'.
 *
 * Schedule the actions to run on the engine and return immediately.
 * The status of the run can be checked either by ::max_wait or ::max_nowait;
 * note that one of these *must* be called, so that associated memory can be released.
 *
 * 
 * \param [in] engine The engine on which the actions will be executed.
 * \param [in] interface_actions Actions to be executed.
 * \return A handle on the execution status of the actions, or NULL in case of error.
 */
max_run_t *ExactMatch_Write_run_nonblock(
	max_engine_t *engine,
	ExactMatch_Write_actions_t *interface_actions);

/**
 * \brief Group run advanced static function for the interface 'Write'.
 * 
 * \param [in] group Group to use.
 * \param [in,out] interface_actions Actions to run.
 *
 * Run the actions on the first device available in the group.
 */
void ExactMatch_Write_run_group(max_group_t *group, ExactMatch_Write_actions_t *interface_actions);

/**
 * \brief Group run advanced static non-blocking function for the interface 'Write'.
 * 
 *
 * Schedule the actions to run on the first device available in the group and return immediately.
 * The status of the run must be checked with ::max_wait. 
 * Note that use of ::max_nowait is prohibited with non-blocking running on groups:
 * see the ::max_run_group_nonblock documentation for more explanation.
 *
 * \param [in] group Group to use.
 * \param [in] interface_actions Actions to run.
 * \return A handle on the execution status of the actions, or NULL in case of error.
 */
max_run_t *ExactMatch_Write_run_group_nonblock(max_group_t *group, ExactMatch_Write_actions_t *interface_actions);

/**
 * \brief Array run advanced static function for the interface 'Write'.
 * 
 * \param [in] engarray The array of devices to use.
 * \param [in,out] interface_actions The array of actions to run.
 *
 * Run the array of actions on the array of engines.  The length of interface_actions
 * must match the size of engarray.
 */
void ExactMatch_Write_run_array(max_engarray_t *engarray, ExactMatch_Write_actions_t *interface_actions[]);

/**
 * \brief Array run advanced static non-blocking function for the interface 'Write'.
 * 
 *
 * Schedule to run the array of actions on the array of engines, and return immediately.
 * The length of interface_actions must match the size of engarray.
 * The status of the run can be checked either by ::max_wait or ::max_nowait;
 * note that one of these *must* be called, so that associated memory can be released.
 *
 * \param [in] engarray The array of devices to use.
 * \param [in] interface_actions The array of actions to run.
 * \return A handle on the execution status of the actions, or NULL in case of error.
 */
max_run_t *ExactMatch_Write_run_array_nonblock(max_engarray_t *engarray, ExactMatch_Write_actions_t *interface_actions[]);

/**
 * \brief Converts a static-interface action struct into a dynamic-interface max_actions_t struct.
 *
 * Note that this is an internal utility function used by other functions in the static interface.
 *
 * \param [in] maxfile The maxfile to use.
 * \param [in] interface_actions The interface-specific actions to run.
 * \return The dynamic-interface actions to run, or NULL in case of error.
 */
max_actions_t* ExactMatch_Write_convert(max_file_t *maxfile, ExactMatch_Write_actions_t *interface_actions);

/**
 * \brief Initialise a maxfile.
 */
max_file_t* ExactMatch_init(void);

/* Error handling functions */
int ExactMatch_has_errors(void);
const char* ExactMatch_get_errors(void);
void ExactMatch_clear_errors(void);
/* Free statically allocated maxfile data */
void ExactMatch_free(void);
/* These are dummy functions for hardware builds. */
int ExactMatch_simulator_start(void);
int ExactMatch_simulator_stop(void);

#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* SLIC_DECLARATIONS_ExactMatch_H */

