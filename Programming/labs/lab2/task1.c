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
    printf("Задание №1\n");

    size_t n = 0, m = 0, k = 0;
    do
    {
        printf("Введите n, m, k от 1 до %zu\n", LMAX);
        scanf("%zu%zu%zu", &n, &m, &k);
        clean_buffer();
    } while
    (!(
           in_range(n, 1, LMAX)
        && in_range(m, 1, LMAX)
        && in_range(k, 1, LMAX)
    ));

    printf("Введите матрицу x[1:%zu, 1:%zu]\n", n, m);
    int x[LMAX + 1][LMAX + 1] = {};
    for (size_t i = 1; i <= n; i++)
    {
        for (size_t j = 1; j <= m; j++)
        {
            scanf("%d", &x[i][j]);
        }
    }

    printf("Введите массив z[1:%zu]\n", k);
    int z[LMAX + 1] = {};
    for (size_t i = 1; i <= k; i++)
    {
        scanf("%d", &z[i]);
    }

    int e[LMAX + 1] = {};
    size_t t = 0;

    for (size_t i = 1; i <= n; i++)
    {
        for (size_t j = 1; j <= m; j++)
        {
            size_t found = 1;
            while (found <= k && x[i][j] != z[found])
            {
                found++;
            }
            if (found <= k)
            {
                x[i][j] = 0;
                t++;
                e[t] = z[found];
            }
        }
    }

    if (t == 0)
    {
        printf("Ноль обнулений\n");
    }
    else
    {
        printf("Обнулено %zu элементов:\n", t);
        print_array(t, e);
        printf("Матрица имеет следующий вид:\n");
        print_matrix(n, m, x);
    }
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
