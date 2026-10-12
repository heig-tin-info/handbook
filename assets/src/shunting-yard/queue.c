#include "queue.h"

#include <stdlib.h>

Queue queue_create() {
    Queue queue;
    queue.front = NULL;
    queue.rear = NULL;
    return queue;
}

void queue_push(Queue *queue, char value) {
    QueueNode *newNode = (QueueNode *)malloc(sizeof(QueueNode));
    newNode->data = value;
    newNode->next = NULL;
    if (queue->rear)
        queue->rear->next = newNode;
    else
        queue->front = newNode;
    queue->rear = newNode;
}

char queue_pop(Queue *queue) {
    if (queue->front == NULL)
        return '\0';
    QueueNode *node = queue->front;
    char value = node->data;
    queue->front = node->next;
    if (queue->front == NULL)
        queue->rear = NULL;
    free(node);
    return value;
}

int queue_empty(Queue *queue) {
    return queue->front == NULL;
}
