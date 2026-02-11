#include <stdint.h>
#include <memory.h>
#include <assert.h>

#include "aes.h"
#include "ecb.h"

void
aes128_ecb_enc ( const void * ctx, const uint8_t * plaintext, const int plain_size, uint8_t * ciphertext )
{
// TODO - done
    assert( ctx != 0 && plaintext != 0 && ciphertext != 0);
    /* ECB mode: independent block encryption
     * plaintext and ciphertext buffers must be block-aligned
     */
    assert( plain_size % AES128_BLOCK_SIZE == 0 );

    const int nblocks = plain_size / AES128_BLOCK_SIZE;
    for (int i = 0; i < nblocks; ++i) {
        const uint8_t *in = plaintext + i * AES128_BLOCK_SIZE;
        uint8_t *out = ciphertext + i * AES128_BLOCK_SIZE;
        aes128_block_enc( ctx, in, out );
    }

// until here
}

void
aes128_ecb_dec ( const void * ctx, const uint8_t * ciphertext, const int cipher_size, uint8_t * plaintext )
{
// TODO - done
    assert( ctx != 0 && plaintext != 0 && ciphertext != 0);
    /* ECB mode: independent block decryption
     * ciphertext and plaintext buffers must be block-aligned
     */
    assert( cipher_size % AES128_BLOCK_SIZE == 0 );

    const int nblocks = cipher_size / AES128_BLOCK_SIZE;
    for (int i = 0; i < nblocks; ++i) {
        const uint8_t *in = ciphertext + i * AES128_BLOCK_SIZE;
        uint8_t *out = plaintext + i * AES128_BLOCK_SIZE;
        aes128_block_dec( ctx, in, out );
    }

// until here
}
