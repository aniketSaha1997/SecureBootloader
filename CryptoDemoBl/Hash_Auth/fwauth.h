/**
  ******************************************************************************
  * @file    fwauth.h
  * @brief   Header file of security config check module.
  *
  ******************************************************************************
  */
#ifndef __FW_AUTH_H
#define __FW_AUTH_H

/******************************************************************************
 * Include Header Files
 ******************************************************************************/
#include "stdint.h"
#include "stdio.h"

/******************************************************************************
 * Global variables
 ******************************************************************************/
extern const volatile unsigned int  _Addr_Application_Header, _Addr_Application;

/******************************************************************************
 * Macros Constant Declarations
 ******************************************************************************/
#define FW_HASH_LEN             32u /* SHA256*/
#define FW_META_SIG_LEN         64u /* ECDSA P256*/
#define FW_MAGIC                'FWMA'
#define FW_META_DATA_ADD        (uint32_t)(&_Addr_Application_Header)
#define FW_ADD                  (uint32_t)(&_Addr_Application)

/******************************************************************************
 * Type Declarations
 ******************************************************************************/
/* 
 * FW meta data for verification 
 * Totoal size 128 bytes, with 20 reserved bytes not used 
 */
typedef struct {
  uint32_t FWMagic;               /*!< FW Magic 'FWMA'*/
  uint32_t FwSize;                 /*!< Firmware size (bytes)*/
  uint32_t FwVersion;              /*!< Firmware version*/
  uint8_t  FwTag[FW_HASH_LEN];      /*!< Firmware Tag*/
  uint8_t  Reserved[84];          /*!< Reserved for future use: 84 extra bytes to have a header size (to be signed) of 128 bytes */
  uint8_t  MetaTag[FW_HASH_LEN];  /*!< Signature of the header message (before MetaTag)*/
  uint8_t  MetaSig[FW_META_SIG_LEN];  /*!< Signature of the header message (before MetaTag)*/
}FW_Meta_t;

/******************************************************************************
 * Extern Functions Declaration
 ******************************************************************************/
/**
  * @brief  Verifies the integrity of the application binary.
  *
  * @retval NONE
  */
extern int32_t FwVerify(void);

#endif /* __FW_AUTH_H */
