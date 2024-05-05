/**
 * @file       map_linker.c
 *
 * @brief      This file contains memory elements mapped to the linker.
 *             It handles function to jump between 2 softwares.
 *
 */

/******************************************************************************
 * Include Header Files
 ******************************************************************************/
#include <stdint.h>
#include <stddef.h>
#include "string.h"
#include "map_linker.h"

/* cubeMX */
#include "main.h"

/******************************************************************************
 * #6 Module Global Variable Declarations
 ******************************************************************************/
extern const volatile unsigned int  _Addr_Application;
extern unsigned int _start_sharedElements;
extern unsigned int _end_sharedElements;

/******************************************************************************
 * Macro Constant Declarations
 ******************************************************************************/
#define MAP_LINKER_ADDR_APPL     (uint32_t)(&_Addr_Application)
#define MAP_LINKER_SRAM_ERASE()  memset(&_start_sharedElements, 0u, &_end_sharedElements - &_start_sharedElements)
//#define SECURE_USER_PROTECT_ENABLE
/******************************************************************************
 * Type Declarations
 ******************************************************************************/
typedef void (*pFunction)(void);

/******************************************************************************
 * Static Function Declarations
 ******************************************************************************/
static void MapLinkerDeinitModule(void);

/******************************************************************************
 * Extern Function Definitions
 ******************************************************************************/
__attribute__((optimize("-O0")))
extern void MapLinkerJumpToAppl(void)
{
#if !(defined(SECURE_USER_PROTECT_ENABLE))
    MapLinkerDeinitModule();

    /* Destroy the Volatile data and CSTACK in SRAM used by Secure Boot in order to prevent any access to sensitive data
       from the loader.
    */
    MAP_LINKER_SRAM_ERASE();


    uint32_t jumpAddress_u32;
    pFunction jumpToApplication_p;

    jumpAddress_u32 = *(uint32_t *)(MAP_LINKER_ADDR_APPL + 4uL);

    jumpToApplication_p = (pFunction) jumpAddress_u32;

    __disable_irq();

    __set_MSP(*(uint32_t *)(MAP_LINKER_ADDR_APPL));
    jumpToApplication_p();

#else

#define MAP_LINKER_BL_EXIT	 		0x1FFF6800
#define MAP_LINKER_MAGIC_NUMBER		0x08192A3C


  {
    //R0: MAP_LINKER_BL_EXIT vector table address
    //R1: magic number
    //R2: application address
    typedef  void (*pFunction)(uint32_t a, uint32_t b, uint32_t c);

    pFunction jumpToApplication_p;
    uint32_t jumpAddress_u32;

    MapLinkerDeinitModule();
    MAP_LINKER_SRAM_ERASE();

    /* Jump to user application */
    jumpAddress_u32 = *(uint32_t *)(MAP_LINKER_BL_EXIT + 4uL);
    jumpToApplication_p = (pFunction) jumpAddress_u32;
    jumpToApplication_p(jumpAddress_u32, MAP_LINKER_MAGIC_NUMBER, MAP_LINKER_ADDR_APPL);

  }

#endif /* SECURE_USER_PROTECT_ENABLE */
}

/******************************************************************************
 * Static Function Definitions
 ******************************************************************************/
static void MapLinkerDeinitModule(void)
{
    HAL_DeInit();

    /* This defaults the system clock to default values before jumping.
     * Prevents Sysclock configuration faults in case of different clock configs
     * across jumps. */
    HAL_RCC_DeInit();
}
