#pragma once

typedef struct QueueNode {
    char data;
    struct QueueNode *next;
} QueueNode;

typedef struct {
    QueueNode *front;
    QueueNode *rear;
} Queue;

Queue queue_create();
void queue_push(Queue *queue, char value);
char queue_pop(Queue *queue);
int queue_empty(Queue *queue);
