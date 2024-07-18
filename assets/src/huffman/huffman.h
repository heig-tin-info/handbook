#pragma once

#include <stddef.h>

typedef struct HuffmanNode {
    unsigned char character;
    unsigned int frequency;
    struct HuffmanNode *left;
    struct HuffmanNode *right;
} HuffmanNode;

typedef struct {
    HuffmanNode *root;
    char **codes;
} HuffmanTree;

HuffmanTree *build_huffman_tree(const unsigned char *data, size_t size);
void free_huffman_tree(HuffmanTree *tree);
void encode_data(HuffmanTree *tree, const unsigned char *data, size_t size, unsigned char **encoded_data, size_t *encoded_size);
void decode_data(HuffmanTree *tree, const unsigned char *encoded_data, size_t encoded_size, unsigned char **decoded_data, size_t *decoded_size);
