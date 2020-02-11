/**\file */
#ifndef SLIC_DECLARATIONS_NBody_H
#define SLIC_DECLARATIONS_NBody_H
#include "MaxSLiCInterface.h"
#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#define NBody_maxParticles (65535)
#define NBody_numParticlesDivisor (420)
#define NBody_loopLatency (14)
#define NBody_numPipes (30)


/*----------------------------------------------------------------------------*/
/*---------------------------- Interface advanced ----------------------------*/
/*----------------------------------------------------------------------------*/




/**
 * \brief Basic static function for the interface 'advanced'.
 * 
 * \param [in] param_N Interface Parameter "N".: Number of particles in system
 * \param [in] param_P Interface Parameter "P".: Number of particles to compute acceleration for
 * \param [in] inscalar_NBodyKernel_EPS Input scalar parameter "NBodyKernel.EPS".
 * \param [in] instream_fromhost The stream should be of size ((param_N * 4) * 4) bytes.
 * \param [out] outstream_acc The stream should be of size ((param_P * 4) * 4) bytes.
 */
void NBody_advanced(
	int32_t param_N,
	int32_t param_P,
	double inscalar_NBodyKernel_EPS,
	const float *instream_fromhost,
	float *outstream_acc);

/**
 * \brief Basic static non-blocking function for the interface 'advanced'.
 * 
 * Schedule to run on an engine and return immediately.
 * The status of the run can be checked either by ::max_wait or ::max_nowait;
 * note that one of these *must* be called, so that associated memory can be released.
 * 
 * 
 * \param [in] param_N Interface Parameter "N".: Number of particles in system
 * \param [in] param_P Interface Parameter "P".: Number of particles to compute acceleration for
 * \param [in] inscalar_NBodyKernel_EPS Input scalar parameter "NBodyKernel.EPS".
 * \param [in] instream_fromhost The stream should be of size ((param_N * 4) * 4) bytes.
 * \param [out] outstream_acc The stream should be of size ((param_P * 4) * 4) bytes.
 * \return A handle on the execution status, or NULL in case of error.
 */
max_run_t *NBody_advanced_nonblock(
	int32_t param_N,
	int32_t param_P,
	double inscalar_NBodyKernel_EPS,
	const float *instream_fromhost,
	float *outstream_acc);

/**
 * \brief Advanced static interface, structure for the engine interface 'advanced'
 * 
 */
typedef struct { 
	int32_t param_N; /**<  [in] Interface Parameter "N".: Number of particles in system */
	int32_t param_P; /**<  [in] Interface Parameter "P".: Number of particles to compute acceleration for */
	double inscalar_NBodyKernel_EPS; /**<  [in] Input scalar parameter "NBodyKernel.EPS". */
	const float *instream_fromhost; /**<  [in] The stream should be of size ((param_N * 4) * 4) bytes. */
	float *outstream_acc; /**<  [out] The stream should be of size ((param_P * 4) * 4) bytes. */
} NBody_advanced_actions_t;

/**
 * \brief Advanced static function for the interface 'advanced'.
 * 
 * \param [in] engine The engine on which the actions will be executed.
 * \param [in,out] interface_actions Actions to be executed.
 */
void NBody_advanced_run(
	max_engine_t *engine,
	NBody_advanced_actions_t *interface_actions);

/**
 * \brief Advanced static non-blocking function for the interface 'advanced'.
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
max_run_t *NBody_advanced_run_nonblock(
	max_engine_t *engine,
	NBody_advanced_actions_t *interface_actions);

/**
 * \brief Group run advanced static function for the interface 'advanced'.
 * 
 * \param [in] group Group to use.
 * \param [in,out] interface_actions Actions to run.
 *
 * Run the actions on the first device available in the group.
 */
void NBody_advanced_run_group(max_group_t *group, NBody_advanced_actions_t *interface_actions);

/**
 * \brief Group run advanced static non-blocking function for the interface 'advanced'.
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
max_run_t *NBody_advanced_run_group_nonblock(max_group_t *group, NBody_advanced_actions_t *interface_actions);

/**
 * \brief Array run advanced static function for the interface 'advanced'.
 * 
 * \param [in] engarray The array of devices to use.
 * \param [in,out] interface_actions The array of actions to run.
 *
 * Run the array of actions on the array of engines.  The length of interface_actions
 * must match the size of engarray.
 */
void NBody_advanced_run_array(max_engarray_t *engarray, NBody_advanced_actions_t *interface_actions[]);

/**
 * \brief Array run advanced static non-blocking function for the interface 'advanced'.
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
max_run_t *NBody_advanced_run_array_nonblock(max_engarray_t *engarray, NBody_advanced_actions_t *interface_actions[]);

/**
 * \brief Converts a static-interface action struct into a dynamic-interface max_actions_t struct.
 *
 * Note that this is an internal utility function used by other functions in the static interface.
 *
 * \param [in] maxfile The maxfile to use.
 * \param [in] interface_actions The interface-specific actions to run.
 * \return The dynamic-interface actions to run, or NULL in case of error.
 */
max_actions_t* NBody_advanced_convert(max_file_t *maxfile, NBody_advanced_actions_t *interface_actions);



/*----------------------------------------------------------------------------*/
/*---------------------------- Interface default -----------------------------*/
/*----------------------------------------------------------------------------*/




/**
 * \brief Basic static function for the interface 'default'.
 * 
 * \param [in] param_N Interface Parameter "N".: Number of particles
 * \param [in] inscalar_NBodyKernel_EPS Input scalar parameter "NBodyKernel.EPS".
 * \param [in] instream_fromhost The stream should be of size ((param_N * 4) * 4) bytes.
 * \param [out] outstream_acc The stream should be of size ((param_N * 4) * 4) bytes.
 */
void NBody(
	int32_t param_N,
	double inscalar_NBodyKernel_EPS,
	const float *instream_fromhost,
	float *outstream_acc);

/**
 * \brief Basic static non-blocking function for the interface 'default'.
 * 
 * Schedule to run on an engine and return immediately.
 * The status of the run can be checked either by ::max_wait or ::max_nowait;
 * note that one of these *must* be called, so that associated memory can be released.
 * 
 * 
 * \param [in] param_N Interface Parameter "N".: Number of particles
 * \param [in] inscalar_NBodyKernel_EPS Input scalar parameter "NBodyKernel.EPS".
 * \param [in] instream_fromhost The stream should be of size ((param_N * 4) * 4) bytes.
 * \param [out] outstream_acc The stream should be of size ((param_N * 4) * 4) bytes.
 * \return A handle on the execution status, or NULL in case of error.
 */
max_run_t *NBody_nonblock(
	int32_t param_N,
	double inscalar_NBodyKernel_EPS,
	const float *instream_fromhost,
	float *outstream_acc);

/**
 * \brief Advanced static interface, structure for the engine interface 'default'
 * 
 */
typedef struct { 
	int32_t param_N; /**<  [in] Interface Parameter "N".: Number of particles */
	double inscalar_NBodyKernel_EPS; /**<  [in] Input scalar parameter "NBodyKernel.EPS". */
	const float *instream_fromhost; /**<  [in] The stream should be of size ((param_N * 4) * 4) bytes. */
	float *outstream_acc; /**<  [out] The stream should be of size ((param_N * 4) * 4) bytes. */
} NBody_actions_t;

/**
 * \brief Advanced static function for the interface 'default'.
 * 
 * \param [in] engine The engine on which the actions will be executed.
 * \param [in,out] interface_actions Actions to be executed.
 */
void NBody_run(
	max_engine_t *engine,
	NBody_actions_t *interface_actions);

/**
 * \brief Advanced static non-blocking function for the interface 'default'.
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
max_run_t *NBody_run_nonblock(
	max_engine_t *engine,
	NBody_actions_t *interface_actions);

/**
 * \brief Group run advanced static function for the interface 'default'.
 * 
 * \param [in] group Group to use.
 * \param [in,out] interface_actions Actions to run.
 *
 * Run the actions on the first device available in the group.
 */
void NBody_run_group(max_group_t *group, NBody_actions_t *interface_actions);

/**
 * \brief Group run advanced static non-blocking function for the interface 'default'.
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
max_run_t *NBody_run_group_nonblock(max_group_t *group, NBody_actions_t *interface_actions);

/**
 * \brief Array run advanced static function for the interface 'default'.
 * 
 * \param [in] engarray The array of devices to use.
 * \param [in,out] interface_actions The array of actions to run.
 *
 * Run the array of actions on the array of engines.  The length of interface_actions
 * must match the size of engarray.
 */
void NBody_run_array(max_engarray_t *engarray, NBody_actions_t *interface_actions[]);

/**
 * \brief Array run advanced static non-blocking function for the interface 'default'.
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
max_run_t *NBody_run_array_nonblock(max_engarray_t *engarray, NBody_actions_t *interface_actions[]);

/**
 * \brief Converts a static-interface action struct into a dynamic-interface max_actions_t struct.
 *
 * Note that this is an internal utility function used by other functions in the static interface.
 *
 * \param [in] maxfile The maxfile to use.
 * \param [in] interface_actions The interface-specific actions to run.
 * \return The dynamic-interface actions to run, or NULL in case of error.
 */
max_actions_t* NBody_convert(max_file_t *maxfile, NBody_actions_t *interface_actions);

/**
 * \brief Initialise a maxfile.
 */
max_file_t* NBody_init(void);

/* Error handling functions */
int NBody_has_errors(void);
const char* NBody_get_errors(void);
void NBody_clear_errors(void);
/* Free statically allocated maxfile data */
void NBody_free(void);
/* These are dummy functions for hardware builds. */
int NBody_simulator_start(void);
int NBody_simulator_stop(void);

#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* SLIC_DECLARATIONS_NBody_H */

