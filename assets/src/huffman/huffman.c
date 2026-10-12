#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "min-heap.h"
#include "huffman.h"
#include "vector.h"

typedef struct {
    unsigned char character;
    unsigned int frequency;
} FrequencyEntry;

typedef struct {
    unsigned char character;
    char *code;
} CodeEntry;

static int huffman_compare(const void *a, const void *b) {
    return (*(HuffmanNode **)a)->frequency - (*(HuffmanNode **)b)->frequency;
}

static HuffmanNode *create_huffman_node(unsigned char character, unsigned int frequency) {
    HuffmanNode *node = (HuffmanNode *)malloc(sizeof(HuffmanNode));
    if (node == NULL) return NULL;
    node->character = character;
    node->frequency = frequency;
    node->left = node->right = NULL;
    return node;
}

static void build_codes(HuffmanNode *node, char *code, int depth, Vector *codes) {
    if (node == NULL) return;
    if (node->left == NULL && node->right == NULL) {
        code[depth] = '\0';
        CodeEntry *entry = (CodeEntry *)malloc(sizeof(CodeEntry));
        entry->character = node->character;
        entry->code = strdup(code);
        vector_push_back(codes, entry);
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

static void print_codes(const Vector *codes) {
    for (size_t i = 0; i < vector_size(codes); i++) {
        CodeEntry *entry = (CodeEntry *)vector_get(codes, i);
        if (entry != NULL) {
            printf("%c: %s\n", entry->character, entry->code);
        }
    }
}

static void * print_element(void *element, FILE *output) {
    HuffmanNode *node = *(HuffmanNode **)element;
    if (node->character == '\0') {
        fprintf(output, "*: %u", node->frequency);
    } else {
        // If the character is not printable, print its ASCII code
        if (node->character < 32 || node->character > 126) {
            fprintf(output, "0x%x: %u", node->character, node->frequency);
        } else {
            fprintf(output, "%c: %u", node->character, node->frequency);
        }
    }
    return NULL;
}

HuffmanTree *build_huffman_tree(const unsigned char *data, size_t size) {
    Vector *frequencies = vector_create(sizeof(FrequencyEntry), free);
    if (frequencies == NULL) return NULL;

    // Calcul des fréquences
    for (size_t i = 0; i < size; i++) {
        int found = 0;
        for (size_t j = 0; j < vector_size(frequencies); j++) {
            FrequencyEntry *entry = (FrequencyEntry *)vector_get(frequencies, j);
            if (entry->character == data[i]) {
                entry->frequency++;
                found = 1;
                break;
            }
        }
        if (!found) {
            FrequencyEntry *new_entry = (FrequencyEntry *)malloc(sizeof(FrequencyEntry));
            if (new_entry == NULL) {
                vector_destroy(frequencies);
                return NULL;
            }
            new_entry->character = data[i];
            new_entry->frequency = 1;
            vector_push_back(frequencies, new_entry);
        }
    }

    MinHeap *heap = min_heap_create(sizeof(HuffmanNode *), huffman_compare, NULL);
    if (!heap) {
        vector_destroy(frequencies);
        return NULL;
    }

    for (size_t i = 0; i < vector_size(frequencies); i++) {
        FrequencyEntry *entry = (FrequencyEntry *)vector_get(frequencies, i);
        HuffmanNode *node = create_huffman_node(entry->character, entry->frequency);
        if (node == NULL) {
            min_heap_destroy(heap);
            vector_destroy(frequencies);
            return NULL;
        }
        min_heap_insert(heap, &node);
    }

    min_heap_to_mermaid(heap, stdout, print_element);

    while (min_heap_size(heap) > 1) {
        HuffmanNode *left = *(HuffmanNode **)min_heap_extract_min(heap);
        HuffmanNode *right = *(HuffmanNode **)min_heap_extract_min(heap);
        printf("Pop: %c: %u + %c: %u\n", left->character, left->frequency, right->character, right->frequency);
        HuffmanNode *node = create_huffman_node('\0', left->frequency + right->frequency);
        if (node == NULL) {
            free(left);
            free(right);
            min_heap_destroy(heap);
            vector_destroy(frequencies);
            return NULL;
        }
        node->left = left;
        node->right = right;
        min_heap_insert(heap, &node);

        min_heap_to_mermaid(heap, stdout, print_element);
    }

    HuffmanNode *root = *(HuffmanNode **)min_heap_extract_min(heap);
    HuffmanTree *tree = (HuffmanTree *)malloc(sizeof(HuffmanTree));
    if (tree == NULL) {
        free(root);
        min_heap_destroy(heap);
        vector_destroy(frequencies);
        return NULL;
    }
    tree->root = root;
    tree->codes = vector_create(sizeof(CodeEntry), free);
    if (tree->codes == NULL) {
        free_huffman_tree(tree);
        min_heap_destroy(heap);
        vector_destroy(frequencies);
        return NULL;
    }

    printf("Arbre de Huffman après construction:\n");
    print_huffman_tree(tree);

    char code[256];
    build_codes(root, code, 0, tree->codes);

    // Afficher les codes créés
    printf("Codes de Huffman:\n");
    print_codes(tree->codes);

    vector_destroy(frequencies);
    min_heap_destroy(heap);
    return tree;
}

void free_huffman_tree(HuffmanTree *tree) {
    if (tree == NULL) return;

    // Fonction récursive pour libérer l'arbre de Huffman
    void free_node(HuffmanNode *node) {
        if (node == NULL) return;
        free_node(node->left);
        free_node(node->right);
        free(node);
    }

    free_node(tree->root);

    for (size_t i = 0; i < vector_size(tree->codes); i++) {
        CodeEntry *entry = (CodeEntry *)vector_get(tree->codes, i);
        free(entry->code);
        free(entry);
    }

    vector_destroy(tree->codes);
    free(tree);
}

void encode_data(HuffmanTree *tree, const unsigned char *data, size_t size, unsigned char **encoded_data, size_t *encoded_size) {
    size_t buffer_size = size * 8; // Taille maximale possible
    unsigned char *buffer = (unsigned char *)malloc(buffer_size);
    memset(buffer, 0, buffer_size); // Initialiser à 0
    size_t bit_pos = 0;

    for (size_t i = 0; i < size; i++) {
        char *code = NULL;
        for (size_t j = 0; j < vector_size(tree->codes); j++) {
            CodeEntry *entry = (CodeEntry *)vector_get(tree->codes, j);
            if (entry->character == data[i]) {
                code = entry->code;
                break;
            }
        }
        for (size_t j = 0; j < strlen(code); j++) {
            if (code[j] == '1') {
                buffer[bit_pos / 8] |= (1 << (7 - (bit_pos % 8)));
            }
            bit_pos++;
        }
    }

    *encoded_size = (bit_pos + 7) / 8; // Arrondir au prochain octet
    *encoded_data = (unsigned char *)malloc(*encoded_size);
    memcpy(*encoded_data, buffer, *encoded_size);
    free(buffer);
}

void decode_data(HuffmanTree *tree, const unsigned char *encoded_data, size_t encoded_size, unsigned char **decoded_data, size_t *decoded_size) {
    size_t buffer_size = encoded_size * 8; // Taille maximale possible
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

// Fonction pour afficher l'arbre de Huffman
static void print_huffman_node(const HuffmanNode *node, int depth) {
    if (node == NULL) return;
    for (int i = 0; i < depth; i++) {
        printf("  ");
    }
    if (node->character != '\0') {
        printf("%c: %u\n", node->character, node->frequency);
    } else {
        printf("*: %u\n", node->frequency);
    }
    print_huffman_node(node->left, depth + 1);
    print_huffman_node(node->right, depth + 1);
}

void print_huffman_tree(const HuffmanTree *tree) {
    if (tree == NULL || tree->root == NULL) {
        printf("L'arbre de Huffman est vide.\n");
        return;
    }
    print_huffman_node(tree->root, 0);
}
