/**
 ******************************************************************************
 * @file    hashcheck.h
 * @brief   Header file for hashcheck module.
 *          This file provides set of firmware functions to manage hash
 *          verification functionalities.
 ******************************************************************************
 */
#ifndef __HASHCHECK_H
#define __HASHCHECK_H

/******************************************************************************
 * Include Header Files
 ******************************************************************************/
#include "main.h"

/******************************************************************************
 * Macros Parameter Declarations
 ******************************************************************************/
#if defined (__ICCARM__)
#pragma section = "Firmware"
#define FW_END ((uint32_t)__section_end("Firmware"))
#elif defined (__CC_ARM)
extern uint32_t Image$$ER_IROM1$$Limit;
#define FW_END         ((uint32_t)&Image$$ER_IROM1$$Limit)
#elif  defined(__GNUC__)
extern const volatile uint32_t __FW_SECTION_END;
#define FW_END (uint32_t)((uint8_t*)& __FW_SECTION_END)
#else
#error "NOT SUPPORTED"
#endif

/******************************************************************************
 * Global variables
 ******************************************************************************/
static const uint32_t flashSectorSize_au32[] = {
		0x00008000U,        // Sector 0 (32 KB)
		0x00008000U,        // Sector 1 (32 KB)
		0x00008000U,      	// Sector 2 (32 KB)
		0x00008000U,      	// Sector 3 (32 KB)
		0x00020000U,      	// Sector 4 (128 KB)
		0x00040000U,      	// Sector 5 (256 KB)
		0x00040000U,      	// Sector 6 (256 KB)
		0x00040000U,      	// Sector 7 (256 KB)
		0x00040000U,     	// Sector 8 (256 KB)
		0x00040000U,     	// Sector 9 (256 KB)
		0x00040000U,     	// Sector 10 (256 KB)
		0x00040000U      	// Sector 11 (256 KB)
};

/******************************************************************************
 * Macros Constant Declarations
 ******************************************************************************/
/* FW start from user flash base address */
#define FW_START_ADD (FLASH_BASE)
#define FLASH_SECTOR_SIZE(sector) (flashSectorSize_au32[(sector)])
#define FW_SIZE (FW_END - FW_START_ADD)

/* The firmware has to be aligned with the sector boundary in order to seperate the hash into another sector */
#define FW_SIZE_ALIGNED  (FW_SIZE % FLASH_SECTOR_SIZE(2) == 0? FW_SIZE : (FW_SIZE / FLASH_SECTOR_SIZE(2) + 1) * FLASH_SECTOR_SIZE(2))
#define HASH_ADD (FW_START_ADD + FW_SIZE_ALIGNED)

/* SHA256 outputs 32 bit always */
#define HASH_SIZE (32)

/******************************************************************************
 * Extern Functions Declarations
 ******************************************************************************/
/**
  * @brief  Verifies the hash of the firmware binary.
  *
  * @retval NONE
  */
extern void FwHashVerify(void);

/**
  * @brief  Error handler, called in case of any error during verification process.
  *
  * @retval NONE
  */
extern void FatalErrorHandler(void);

#endif /* __HASHCHECK_H */
