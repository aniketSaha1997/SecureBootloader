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
