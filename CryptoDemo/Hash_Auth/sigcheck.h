/**
 ******************************************************************************
 * @file    sigcheck.h
 * @brief   Header file of signature check module.
 *          This file provides set of firmware functions to verify the signature
 *          of the firmware.
 ******************************************************************************
 */

#ifndef __SIGCHECK_H
#define __SIGCHECK_H
/******************************************************************************
 * Include Header Files
 ******************************************************************************/
#include "hashcheck.h"

/******************************************************************************
 * Macros Constant Declarations
 ******************************************************************************/
#define SIG_ADD (HASH_ADD + HASH_SIZE)
#define SIG_SIZE (64)
#define ECC_PUB_ADD (SIG_ADD + SIG_SIZE)
#define ECC_PUB_SIZE (64)

/******************************************************************************
 * Extern Functions Declarations
 ******************************************************************************/
/**
  * @brief  Verifies the signature of the firmware binary.
  *
  * @retval NONE
  */
extern void FwSignatureVerify(void);

#endif /* __SIGCHECK_H */
