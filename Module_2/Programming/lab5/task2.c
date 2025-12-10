#include <stdio.h>
#include <stdlib.h>

typedef struct Node
{
    int data;
    struct Node* next;
} Node;

typedef struct Queue
{
    Node* head;
    Node* tail;
} Queue;

static void push(Queue* q, int n);
static void insert(Node* after, int n);
static void queue_dtor(Queue* queue);
static void print_queue(const Queue queue);
static Queue input_queue(void);
static void insert_after_odd(Queue* queue, int a1);

static Node* find_positive(Queue queue);
static void sort(Node* node);

int main()
{
    puts("Лабораторная работа №5");

    puts("Задание №2");

    Queue q = input_queue();
    puts("Очередь:");
    print_queue(q);

    int a1 = 0;
    puts("Введите A1:");
    scanf("%d", &a1);
    insert_after_odd(&q, a1);
    puts("Очередь:");
    print_queue(q);

    Node* pos = find_positive(q);
    if (!pos)
    {
        puts("Нет положительных элементов");
    }
    else
    {
        sort(pos->next);
        puts("Очередь:");
        print_queue(q);
    }

    queue_dtor(&q);
}

static void push(Queue* q, int n)
{
    if (q->tail == NULL)
    {
        q->tail = calloc(1, sizeof(Node));
        q->tail->data = n;
        q->head = q->tail;
        return;
    }

    Node* new_node = calloc(1, sizeof(Node));
    new_node->data = n;

    q->tail->next = new_node;
    q->tail = new_node;
}

static void insert(Node* after, int n)
{
    Node* new_node = calloc(1, sizeof(Node));
    new_node->data = n;
    new_node->next = after->next;
    after->next = new_node;
}

static void queue_dtor(Queue* queue)
{
    Node* cur = queue->head;

    while (cur)
    {
        Node* next = cur->next;
        free(cur);
        cur = next;
    }

    *queue = (Queue){};
}

static void print_queue(const Queue queue)
{
    Node* cur = queue.head;

    while (cur)
    {
        Node* next = cur->next;
        printf("%d\n", cur->data);
        cur = next;
    }
}

static Queue input_queue(void)
{
    Queue q = {};

    char buffer[512] = "";

    puts("Введите целые числа, ввод закончите пустой строкой:");

    fgets(buffer, sizeof(buffer), stdin);
    while (buffer[1] != '\0')
    {
        int n = 0;
        sscanf(buffer, "%d", &n);
        push(&q, n);
        fgets(buffer, sizeof(buffer), stdin);
    }

    return q;
}

static void insert_after_odd(Queue* queue, int a1)
{
    size_t n = 1;
    Node* cur = queue->head;

    while (cur)
    {
        Node* next = cur->next;
        if (n % 2 == 1)
        {
            insert(cur, a1);
        }
        cur = next;
        n++;
    }
}

static Node* find_positive(Queue queue)
{
    Node* cur = queue.head;

    while (cur)
    {
        if (cur->data > 0)
        {
            return cur;
        }
        cur = cur->next;
    }

    return NULL;
}

static void sort(Node* node)
{
    if (!node)
    {
        return;
    }

    Node* n1 = node;

    while (n1)
    {
        Node* n2 = n1->next;
        while (n2)
        {
            if (n1->data < n2->data)
            {
                int t = n2->data;
                n2->data = n1->data;
                n1->data = t;
            }
            n2 = n2->next;
        }
        n1 = n1->next;
    }
}
