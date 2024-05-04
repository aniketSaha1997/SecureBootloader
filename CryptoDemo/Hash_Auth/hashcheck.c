/**
 * @file       hashcheck.c
 *
 * @brief
 *
 */

/******************************************************************************
 * Include Header Files
 ******************************************************************************/
#include "crypto.h"
#include "hashcheck.h"
#include <stdio.h>
#include <string.h>

/******************************************************************************
 * Private Function Declarations
 ******************************************************************************/
static int32_t Sha256HashDigestCompute(uint8_t* InputMessage_pu8, uint32_t InputMessageLength_u32,
                                        uint8_t *MessageDigest_pu8, int32_t* MessageDigestLength_ps32);
static void Fatal_Error_Handler(void);

/******************************************************************************
 * Extern Function Definitions
 ******************************************************************************/
extern void FwHashVerify(void)
{
	uint8_t MessageDigest_au8[HASH_SIZE];
	int32_t MessageDigestLength_s32 = HASH_SIZE;
	int32_t result_s32 = -1L;

	/* Enable CRC to allow cryptolib to work */
	__CRC_CLK_ENABLE();

	printf("\r\nStart FW Hash Check...\r\n");
	printf("\tFW start address: 0x%08x\r\n", FW_START_ADD);
	printf("\tFW size: 0x%08x\r\n", FW_SIZE_ALIGNED);
	printf("\tFW HASH address: 0x%08x\r\n", HASH_ADD);
	printf("\tFW HASH SIZE: 0x%08x\r\n", HASH_SIZE);

	result_s32 = Sha256HashDigestCompute((uint8_t*)FW_START_ADD,
									   (uint32_t)(FW_SIZE_ALIGNED),
									   MessageDigest_au8,
									   &MessageDigestLength_s32);
	if (result_s32 == HASH_SUCCESS && MessageDigestLength_s32 == HASH_SIZE)
	{
		uint8_t i_u8;
		printf("\r\nFW HASH Result: \r\n");
		for ( i_u8 = 0u; i_u8 < HASH_SIZE; i_u8++ )
		{
			printf("%02x",MessageDigest_au8[i_u8]);
		}
		printf("\r\nExpected HASH Result: \r\n");
		for ( i_u8 = 0u; i_u8 < HASH_SIZE; i_u8++ )
		{
			printf("%02x",((uint8_t*)HASH_ADD)[i_u8]);
		}

		printf("\r\n");
		if (memcmp((uint8_t*)HASH_ADD, MessageDigest_au8, (uint32_t)HASH_SIZE) == 0)
		{
			printf("\r\nFW Hash check pass\r\n");
		}
		else
		{
			printf("\r\nFW Hash check fail\r\n");
			goto ERROR;
		}
	}
	else
	{
		printf("\r\nFW Hash computation fail!\r\n");
		goto ERROR;
	}

	return;
  
ERROR:
  FatalErrorHandler();
}


/******************************************************************************
 * Private Function Definitions
 ******************************************************************************/

/**
  * @brief  SHA256 HASH digest compute example.
  * @param  InputMessage: pointer to input message to be hashed.
  * @param  InputMessageLength: input data message length in byte.
  * @param  MessageDigest: pointer to output parameter that will handle message digest
  * @param  MessageDigestLength: pointer to output digest length.
  * @retval error status: can be HASH_SUCCESS if success or one of
  *         HASH_ERR_BAD_PARAMETER, HASH_ERR_BAD_CONTEXT,
  *         HASH_ERR_BAD_OPERATION if error occured.
  */
static int32_t Sha256HashDigestCompute(uint8_t* InputMessage_pu8, uint32_t InputMessageLength_u32,
                                        uint8_t *MessageDigest_pu8, int32_t* MessageDigestLength_ps32)
{
	SHA256ctx_stt P_pSHA256ctx;
	uint32_t error_u32 = HASH_SUCCESS;

	/* Set the size of the desired hash digest */
	P_pSHA256ctx.mTagSize = CRL_SHA256_SIZE;

	/* Set flag field to default value */
	P_pSHA256ctx.mFlags = E_HASH_DEFAULT;

	error_u32 = SHA256_Init(&P_pSHA256ctx);

	/* check for initialization errors */
	if (error_u32 == HASH_SUCCESS)
	{
		/* Add data to be hashed */
		error_u32 = SHA256_Append(&P_pSHA256ctx,
									 InputMessage_pu8,
									 InputMessageLength_u32);

		if (error_u32 == HASH_SUCCESS)
		{
		  /* retrieve */
		  error_u32 = SHA256_Finish(&P_pSHA256ctx, MessageDigest_pu8, MessageDigestLength_ps32);
		}
	}

	return error_u32;
}


extern void FatalErrorHandler(void)
{
	printf("\r\nFatal error! Enter endless loop!\r\n");
	while(1){};
}
