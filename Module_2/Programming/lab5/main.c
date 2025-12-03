#include <stdio.h>
#include <math.h>
#include <stdlib.h>

typedef struct Node
{
    int data;
    struct Node* prev;
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

static void clean_buffer(FILE* stream);

static void read_stdin(const char* save_path);
static double find_max_neg(const char* path);

int main()
{
    puts("Лабораторная работа №5");

    puts("Задание №1");

    read_stdin("data.txt");

    double max = find_max_neg("data.txt");

    if (max == -INFINITY)
    {
        puts("В последовательности не было отрицательных чисел");
    }
    else
    {
        printf("max = %lg\n", max);
    }

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

    puts("Задание №3");
    Node* pos = find_positive(q);
    if (!pos)
    {
        puts("Нет положительных элементов");
    }
    else
    {
        sort(pos);
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
    new_node->prev = q->tail;

    q->tail->next = new_node;
    q->tail = new_node;
}

static void insert(Node* after, int n)
{
    Node* new_node = calloc(1, sizeof(Node));
    new_node->data = n;
    new_node->next = after->next;
    new_node->prev = after;

    if (after->next)
    {
        after->next->prev = new_node;
    }
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

    puts("Введите целые числа:");

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

static void read_stdin(const char* save_path)
{
    FILE* save = fopen(save_path, "w");

    char buffer[512] = "";

    puts("Введите действительные числа:");

    fgets(buffer, sizeof(buffer), stdin);
    while (buffer[1] != '\0')
    {
        double n = 0;
        sscanf(buffer, "%lg", &n);
        fprintf(save, "%lg\n", n);
        fgets(buffer, sizeof(buffer), stdin);
    }

    fclose(save);
}

static double find_max_neg(const char* path)
{
    FILE* f = fopen(path, "r");

    char buffer[512] = "";

    double max = -INFINITY;

    while (fgets(buffer, sizeof(buffer), f))
    {
        double n = 0;
        sscanf(buffer, "%lg", &n);

        if (n < 0 && n > max)
        {
            max = n;
        }
    }

    fclose(f);

    return max;
}

static void clean_buffer(FILE* stream)
{
    while (fgetc(stream) != '\n');
}
