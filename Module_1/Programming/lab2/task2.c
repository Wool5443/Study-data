#include <stdio.h>

constexpr size_t LMAX = 1000;

static void clean_buffer(void);
static void print_array(size_t size, const int array[LMAX + 1]);
static void print_matrix(size_t n, size_t m, const int
        matrix[LMAX + 1][LMAX + 1]);
static bool in_range(size_t val, size_t a, size_t b);

int main()
{
    printf("Лабораторная работа №2\n");
    printf("Задание №2\n");

    size_t n = 0;
    do
    {
        printf("Введите n от 1 до %zu\n", LMAX);
        scanf("%zu", &n);
        clean_buffer();
    } while (!(in_range(n, 1, LMAX)));

    printf("Введите массив a[1:%zu]\n", n);
    int a[LMAX + 1] = {};
    for (size_t i = 1; i <= n; i++)
    {
        scanf("%d", &a[i]);
    }

    int p[LMAX + 1] = {};
    for (size_t i = 1; i <= n; i++)
    {
        int val = a[i];
        int prod = a[i] ? 1 : 0;

        while (val)
        {
            prod *= val % 10;
            val /= 10;
        }
        p[i] = prod;
    }

    printf("Массивы произведений цифр:\n");
    print_array(n, p);
}

static void print_array(size_t size, const int array[LMAX + 1])
{
    printf("%d", array[1]);
    for (size_t i = 2; i <= size; i++)
    {
        printf(" %d", array[i]);
    }
    printf("\n");
}

static void print_matrix(size_t n, size_t m, const int
        matrix[LMAX + 1][LMAX + 1])
{
    for (size_t i = 1; i <= n; i++)
    {
        print_array(m, matrix[i]);
    }
}

static void clean_buffer(void)
{
    while (getchar() != '\n');
}

static bool in_range(size_t val, size_t a, size_t b)
{
    return a <= val && val <= b;
}
