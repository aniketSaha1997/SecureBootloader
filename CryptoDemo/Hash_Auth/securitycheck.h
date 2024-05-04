/**
  ******************************************************************************
  * @file    securitycheck.h
  * @brief   Header file for security check module.
  *          This file provides set of firmware functions to manage WRP and RDP
  *          toggle functionalities.
  ******************************************************************************
  */
#ifndef __SECURITYCHECK_H
#define __SECURITYCHECK_H

/******************************************************************************
 * Include Header Files
 ******************************************************************************/
#include "hashcheck.h"

/******************************************************************************
 * Macros Constant Declarations
 ******************************************************************************/
//#define WRP_PROTECT_ENABLE
//#define RDP_PROTECT_ENABLE

#define WRP_START_ADD 		((HASH_ADD - FLASH_BASE)/FLASH_SECTOR_SIZE(2))
#define WRP_END_ADD     	WRP_START_ADD
#define RDP_LEVEL_CONFIG 	OB_RDP_LEVEL_1

/******************************************************************************
 * Extern Functions Declaration
 ******************************************************************************/
/**
  * @brief  Check and if not applied apply the Static security  protections to
  *         critical sections in Flash: RDP, WRP. Static security protections
  *         those protections not impacted by a Reset. They are set using the Option Bytes
  *         When the device is locked (RDP Level2), these protections cannot be changed anymore
  * @param  None
  * @note   If security setting apply fails, enter Error Handler
  */
extern void CheckApplyStaticProtections(void);

#endif /* __SECURITYCHECK_H */
