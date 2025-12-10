#include <stdio.h>
#include <stdlib.h>

typedef struct Node
{
    struct Node* prev;
    struct Node* next;
    int data;
} Node;

typedef struct Control_Node
{
    Node* tail;
    Node* head;
} Control_Node;

typedef struct Queue
{
    Control_Node* control;
} Queue;


static Node* node_ctor(int data);
static Queue queue_ctor();
static void queue_dtor(Queue* queue);

static void insert_after(Node* after, int data);
static void remove_node(Node* node);

static void sort(Queue* queue);

static Queue input_queue(void);
static void print_queue(const Queue queue);

int main()
{
    // Queue q = queue_ctor();
    // insert_after(q.control->tail, 30);
    // insert_after(q.control->tail, 10);
    // insert_after(q.control->tail, 20);
    // print_queue(q);

    Queue q = input_queue();
    print_queue(q);

    sort(&q);
    puts("After sort");
    print_queue(q);

    queue_dtor(&q);
}

static Node* node_ctor(int data)
{
    Node* n = calloc(1, sizeof(*n));
    n->data = data;
    return n;
}

static Queue queue_ctor()
{
    Control_Node* control = calloc(1, sizeof(Control_Node));
    control->head = (Node*)control;
    control->tail = (Node*)control;
    return (Queue){control};
}

static void queue_dtor(Queue* queue)
{
    if (!queue)
    {
        return;
    }

    Node* cur = queue->control->head;

    while (cur != (Node*)queue->control)
    {
        Node* next = cur->next;
        free(cur);
        cur = next;
    }

    free(queue->control);

    *queue = (Queue){};
}

static void insert_after(Node* after, int data)
{
    if (!after)
    {
        return;
    }

    Node* new_node = node_ctor(data);

    new_node->prev = after;
    new_node->next = after->next;
    if (new_node->next)
    {
        new_node->next->prev = new_node;
    }

    after->next = new_node;
}

static void remove_node(Node* node)
{
    if (node->next)
    {
        node->next->prev = node->prev;
    }

    if (node->prev)
    {
        node->prev->next = node->next;
    }

    free(node);
}

static void sort(Queue* queue)
{
    if (!queue)
    {
        return;
    }

    Node* n1 = queue->control->tail;

    while (n1 != (Node*)queue->control)
    {
        Node* prev_n1 = n1->prev;
        Node* n2 = prev_n1;
        while (n2 != (Node*)queue->control)
        {
            Node* prev_n2 = n2->prev;
            if (n1->data > n2->data)
            {
                n2->next = n1->next;
                n2->next->prev = n2;
                n1->next = n2;
                n1->prev = n2->prev;
                n1->prev->next = n1;
                n2->prev = n1;
            }
            n2 = prev_n2;
        }
        n1 = prev_n1;
    }
}

static Queue input_queue(void)
{
    Queue q = queue_ctor();

    char buffer[512] = "";

    puts("Введите целые числа, ввод закончите пустой строкой:");

    fgets(buffer, sizeof(buffer), stdin);
    while (buffer[1] != '\0')
    {
        int n = 0;
        sscanf(buffer, "%d", &n);
        insert_after(q.control->tail, n);
        fgets(buffer, sizeof(buffer), stdin);
    }

    return q;
}

static void print_queue(const Queue queue)
{
    Node* cur = queue.control->head;

    while (cur != (Node*)queue.control)
    {
        printf("%d\n", cur->data);
        cur = cur->next;
    }
}
