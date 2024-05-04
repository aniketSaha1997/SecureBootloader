/**
 * @file       map_linker.h
 *
 * @brief      This file contains memory elements mapped to the linker.
 *             It handles function to jump between 2 softwares.
 *
 */

#ifndef MAP_LINKER_H_
#define MAP_LINKER_H_

/******************************************************************************
 * Include Header Files
 ******************************************************************************/

/******************************************************************************
 * Extern Functions Declarations
 ******************************************************************************/
/**
 * @brief This function make the jump to the application code.
 */
extern void MapLinkerJumpToAppl(void);

#endif /* MAP_LINKER_H_ */
