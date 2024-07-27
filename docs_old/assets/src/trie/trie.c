#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define ALPHABET_SIZE 26

typedef struct Node {
    int occurrences;
    struct Node *children[ALPHABET_SIZE];
} Node;

Node* createNode() {
    Node *node = (Node *)malloc(sizeof(Node));
    if (node) {
        node->occurrences = 0;
        for (int i = 0; i < ALPHABET_SIZE; i++) {
            node->children[i] = NULL;
        }
    }
    return node;
}

void insert(Node *root, const char *word) {
    Node *current = root;
    while (*word) {
        if (!current->children[*word - 'a']) {
            current->children[*word - 'a'] = createNode();
        }
        current = current->children[*word - 'a'];
        word++;
    }
    current->occurrences++;
}

int search(Node *root, const char *word) {
    Node *current = root;
    while (*word) {
        if (!current->children[*word - 'a']) {
            return 0;
        }
        current = current->children[*word - 'a'];
        word++;
    }
    return current->occurrences;
}

void freeTrie(Node *root) {
    for (int i = 0; i < ALPHABET_SIZE; i++) {
        if (root->children[i]) {
            freeTrie(root->children[i]);
        }
    }
    free(root);
}

int main() {
    Node *root = createNode();

    insert(root, "frodo");
    insert(root, "sam");
    insert(root, "gandalf");
    // Add more words as needed

    printf("Occurrences of 'frodo': %d\n", search(root, "frodo"));
    printf("Occurrences of 'sam': %d\n", search(root, "sam"));
    printf("Occurrences of 'gandalf': %d\n", search(root, "gandalf"));

    freeTrie(root);
}
