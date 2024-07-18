#include "huffman.h"
#include "slurp.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    const char *data = slurp(stdin);
    size_t size = strlen(data);

    HuffmanTree *tree = build_huffman_tree((const unsigned char *)data, size);

    unsigned char *encoded_data;
    size_t encoded_size;
    encode_data(tree, (const unsigned char *)data, size, &encoded_data, &encoded_size);

    printf("Encoded data in hex:\n");
    for (size_t i = 0; i < encoded_size; i++) {
        printf("%02x", encoded_data[i]);
    }
    printf("\n");

    unsigned char *decoded_data;
    size_t decoded_size;
    decode_data(tree, encoded_data, encoded_size, &decoded_data, &decoded_size);

    printf("Decoded data:\n");
    fwrite(decoded_data, 1, decoded_size, stdout);
    printf("\n");

    free(encoded_data);
    free(decoded_data);
    free_huffman_tree(tree);
}
