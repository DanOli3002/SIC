// Helper file for SIC Lab on Symmetric Cryptography

#include <stdint.h>
#include <memory.h>
#include <assert.h>

#include "aes.h"
#include "cbc.h"

void
aes128_cbc_enc( void * ctx, const uint8_t * iv, const uint8_t * plaintext, const int plain_size, uint8_t * ciphertext )
{
    assert( ctx != 0 && iv != 0 && plaintext != 0 && ciphertext != 0);
    // TODO -done
    /* CBC encryption: C_i = E_K( P_i XOR C_{i-1} ), with C_0 = IV */
    assert( plain_size % AES128_BLOCK_SIZE == 0 );

    uint8_t prev[AES128_BLOCK_SIZE];
    memcpy( prev, iv, AES128_BLOCK_SIZE );

    const int nblocks = plain_size / AES128_BLOCK_SIZE;
    for (int i = 0; i < nblocks; ++i) {
        const uint8_t *pblock = plaintext + i * AES128_BLOCK_SIZE;
        uint8_t *cblock = ciphertext + i * AES128_BLOCK_SIZE;

        uint8_t xored[AES128_BLOCK_SIZE];
        for (int j = 0; j < AES128_BLOCK_SIZE; ++j) {
            xored[j] = pblock[j] ^ prev[j];
        }

        aes128_block_enc( ctx, xored, cblock );

        /* update prev = ciphertext block */
        memcpy( prev, cblock, AES128_BLOCK_SIZE );
    }
    // until here
}

void
aes128_cbc_dec( void * ctx, const uint8_t * iv, const uint8_t * ciphertext, const int cipher_size, uint8_t * plaintext )
{
    assert( ctx != 0 && iv != 0 && plaintext != 0 && ciphertext != 0);
    // TODO -done
    /* CBC decryption: P_i = D_K(C_i) XOR C_{i-1}, with C_0 = IV */
    assert( cipher_size % AES128_BLOCK_SIZE == 0 );

    uint8_t prev[AES128_BLOCK_SIZE];
    memcpy( prev, iv, AES128_BLOCK_SIZE );

    const int nblocks = cipher_size / AES128_BLOCK_SIZE;
    for (int i = 0; i < nblocks; ++i) {
        const uint8_t *cblock = ciphertext + i * AES128_BLOCK_SIZE;
        uint8_t *pblock = plaintext + i * AES128_BLOCK_SIZE;

        uint8_t dec[AES128_BLOCK_SIZE];
        aes128_block_dec( ctx, cblock, dec );

        for (int j = 0; j < AES128_BLOCK_SIZE; ++j) {
            pblock[j] = dec[j] ^ prev[j];
        }

        /* update prev = current ciphertext block */
        memcpy( prev, cblock, AES128_BLOCK_SIZE );
    }
    // until here
}
