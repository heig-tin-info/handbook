#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "min-heap.h"
#include "huffman.h"

static int huffman_compare(const void *a, const void *b) {
    return ((HuffmanNode *)a)->frequency - ((HuffmanNode *)b)->frequency;
}

static HuffmanNode *create_huffman_node(unsigned char character, unsigned int frequency) {
    HuffmanNode *node = (HuffmanNode *)malloc(sizeof(HuffmanNode));
    node->character = character;
    node->frequency = frequency;
    node->left = node->right = NULL;
    return node;
}

static void build_codes(HuffmanNode *node, char *code, int depth, char **codes) {
    if (node->left == NULL && node->right == NULL) {
        code[depth] = '\0';
        codes[node->character] = strdup(code);
        return;
    }
    if (node->left) {
        code[depth] = '0';
        build_codes(node->left, code, depth + 1, codes);
    }
    if (node->right) {
        code[depth] = '1';
        build_codes(node->right, code, depth + 1, codes);
    }
}

HuffmanTree *build_huffman_tree(const unsigned char *data, size_t size) {
    unsigned int frequency[256] = {0};
    for (size_t i = 0; i < size; i++) {
        frequency[data[i]]++;
    }

    MinHeap *heap = min_heap_create(256, huffman_compare);
    for (int i = 0; i < 256; i++) {
        if (frequency[i]) {
            HuffmanNode *node = create_huffman_node((unsigned char)i, frequency[i]);
            min_heap_insert(heap, node);
        }
    }

    while (heap->size > 1) {
        HuffmanNode *left = (HuffmanNode *)min_heap_extract_min(heap);
        HuffmanNode *right = (HuffmanNode *)min_heap_extract_min(heap);
        HuffmanNode *node = create_huffman_node('\0', left->frequency + right->frequency);
        node->left = left;
        node->right = right;
        min_heap_insert(heap, node);
    }

    HuffmanNode *root = (HuffmanNode *)min_heap_extract_min(heap);
    HuffmanTree *tree = (HuffmanTree *)malloc(sizeof(HuffmanTree));
    tree->root = root;
    tree->codes = (char **)calloc(256, sizeof(char *));
    char code[256];
    build_codes(root, code, 0, tree->codes);

    min_heap_free(heap);
    return tree;
}

void free_huffman_tree(HuffmanTree *tree) {
    if (tree == NULL) return;

    // Recursive function to free the Huffman tree
    void free_node(HuffmanNode *node) {
        if (node == NULL) return;
        free_node(node->left);
        free_node(node->right);
        free(node);
    }

    free_node(tree->root);
    for (int i = 0; i < 256; i++) {
        if (tree->codes[i]) {
            free(tree->codes[i]);
        }
    }
    free(tree->codes);
    free(tree);
}

void encode_data(HuffmanTree *tree, const unsigned char *data, size_t size, unsigned char **encoded_data, size_t *encoded_size) {
    size_t buffer_size = size * 8; // Maximum possible size
    unsigned char *buffer = (unsigned char *)malloc(buffer_size);
    memset(buffer, 0, buffer_size); // Initialiser à 0
    size_t bit_pos = 0;

    for (size_t i = 0; i < size; i++) {
        char *code = tree->codes[data[i]];
        for (size_t j = 0; j < strlen(code); j++) {
            if (code[j] == '1') {
                buffer[bit_pos / 8] |= (1 << (7 - (bit_pos % 8)));
            }
            bit_pos++;
        }
    }

    *encoded_size = (bit_pos + 7) / 8; // Round up to the nearest byte
    *encoded_data = (unsigned char *)malloc(*encoded_size);
    memcpy(*encoded_data, buffer, *encoded_size);
    free(buffer);
}

void decode_data(HuffmanTree *tree, const unsigned char *encoded_data, size_t encoded_size, unsigned char **decoded_data, size_t *decoded_size) {
    size_t buffer_size = encoded_size * 8; // Maximum possible size
    unsigned char *buffer = (unsigned char *)malloc(buffer_size);
    size_t decoded_pos = 0;

    HuffmanNode *current = tree->root;
    for (size_t i = 0; i < encoded_size * 8; i++) {
        if (encoded_data[i / 8] & (1 << (7 - (i % 8)))) {
            current = current->right;
        } else {
            current = current->left;
        }

        if (current->left == NULL && current->right == NULL) {
            buffer[decoded_pos++] = current->character;
            current = tree->root;
        }
    }

    *decoded_data = (unsigned char *)malloc(decoded_pos);
    memcpy(*decoded_data, buffer, decoded_pos);
    *decoded_size = decoded_pos;
    free(buffer);
}
