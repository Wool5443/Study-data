// Даны целочисленная матрица A[0:N-1,0:M-1] и целочисленный массив
// B[0:K-1]. Написать программу, которая удаляет путем сдвига
// элементы тех столбцов A, номера которых присутствуют в массиве B,
// и вычисляет сумму элементов оставшихся столбцов. Вычисления
// оформить в виде функции с параметрами. Ввод данных и вывод
// результата записать в основной программе. Обращение к элементам
// матрицы и массива – по индексу

#include <stdio.h>
#include <stdlib.h>

constexpr size_t ARRAY_SIZE = 512;

static void clean_buffer();
static bool check_size(size_t s)
{
    return s != 0 && s <= ARRAY_SIZE;
}

static int solution(size_t n, size_t* m, int A[ARRAY_SIZE][ARRAY_SIZE], size_t k, size_t B[k]);
static void delete_column(size_t column, size_t n, size_t* m, int A[ARRAY_SIZE][ARRAY_SIZE]);

static int comparator(const void* a, const void* b)
{
    size_t a_s = *(const size_t*)a;
    size_t b_s = *(const size_t*)b;

    return b_s - a_s;
}

int main()
{
    size_t n = 0, m = 0, k = 0;
    do
    {
        printf("Введите n, m и k от 1 до %zu:\n", ARRAY_SIZE);
        scanf("%zu%zu%zu", &n, &m, &k);
        clean_buffer();
    } while (!check_size(n) || !check_size(m) || !check_size(k));
    size_t old_m = m;

    int A[ARRAY_SIZE][ARRAY_SIZE] = {};
    size_t B[ARRAY_SIZE] = {};

    printf("Введите матрицу A[%zu][%zu]:\n", n, m);
    for (size_t i = 0; i < n; i++)
    {
        for (size_t j = 0; j < m; j++)
        {
            scanf("%d", &A[i][j]);
        }
    }

    printf("Введите массив B[%zu]:\n", k);
    for (size_t i = 0; i < k; i++)
    {
        scanf("%zu", &B[i]);
    }
    qsort(B, k, sizeof(*B), comparator);

    int sum = solution(n, &m, A, k, B);
    if (m == 0)
    {
        printf("Матрица полностью удалена, суммма элементов = 0\n");
        return 0;
    }

    printf("После удаления %zu столбцов:\n", old_m - m);
    for (size_t i = 0; i < n; i++)
    {
        printf("%d", A[i][0]);
        for (size_t j = 1; j < m; j++)
        {
            printf(" %d", A[i][j]);
        }
        printf("\n");
    }

    printf("Сумма элементов матрицы = %d\n", sum);
}

static int solution(size_t n, size_t* m, int A[ARRAY_SIZE][ARRAY_SIZE], size_t k, size_t B[k])
{
    for (size_t i = 0; i < k; i++)
    {
        delete_column(B[i], n, m, A);
    }

    int sum = 0;

    for (size_t i = 0; i < n; i++)
    {
        for (size_t j = 0; j < *m; j++)
        {
            sum += A[i][j];
        }
    }

    return sum;
}

static void delete_column(size_t column, size_t n, size_t* m, int A[ARRAY_SIZE][ARRAY_SIZE])
{
    if (column >= *m)
    {
        return;
    }

    for (size_t i = 0; i < n; i++)
    {
        for (size_t j = column; j < *m - 1; j++)
        {
            A[i][j] = A[i][j + 1];
        }
    }
    --*m;
}

static void clean_buffer()
{
    while (getchar() != '\n');
}
