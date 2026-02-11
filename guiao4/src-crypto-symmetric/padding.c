// Helper file for SIC Lab on Symmetric Cryptography

#include <stdint.h>
#include <assert.h>

#include "aes.h"
#include "padding.h"

// Adds PKCS#7 padding and returns the new plaintext length

int
add_padding( uint8_t * plain, const int plain_size )
{
    assert( plain != 0 );
    // TODO - done
    /* PKCS#7 padding: always add padding. pad_len in [1..AES128_BLOCK_SIZE] */
    if (plain_size < 0) return -1;

    int rem = plain_size % AES128_BLOCK_SIZE;
    int pad_len = (rem == 0) ? AES128_BLOCK_SIZE : (AES128_BLOCK_SIZE - rem);

    for (int i = 0; i < pad_len; ++i) {
        plain[plain_size + i] = (uint8_t) pad_len;
    }

    return plain_size + pad_len;

    // until here
}

/*
 * Checks PKCS#7 padding and returns the original plaintext length (w/o padding)
 * If an error is found in the padding, it returns -1.
*/

int
rm_padding( uint8_t * padded, const int full_size )
{
    assert( padded != 0 );
    // TODO - done
    /* Validate PKCS#7 padding and return original length (without padding)
     * Return -1 on invalid padding
     */
    if (full_size <= 0) return -1;
    if (full_size % AES128_BLOCK_SIZE != 0) return -1;

    uint8_t pad = padded[full_size - 1];
    if (pad == 0 || pad > AES128_BLOCK_SIZE) return -1;

    for (int i = 0; i < pad; ++i) {
        if (padded[full_size - 1 - i] != pad) return -1;
    }

    return full_size - pad;
    
// until here
}
