// Даны целочисленная матрица A[0:N-1,0:M-1] и целочисленный массив
// B[0:K-1]. Написать программу, которая удаляет путем сдвига
// элементы тех столбцов A, номера которых присутствуют в массиве B,
// и вычисляет сумму элементов оставшихся столбцов. Вычисления
// оформить в виде функции с параметрами. Ввод данных и вывод
// результата записать в основной программе. Обращение к элементам
// матрицы и массива – по индексу

#include <stdio.h>
#include <stdlib.h>

typedef struct Matrix
{
    int* data;
    size_t n, m;
    size_t current_m;
} Matrix;

static void clean_buffer();

static int solution(Matrix* A, size_t k, size_t* B);
static void delete_column(size_t column, Matrix* A);

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
        puts("Введите n, m и k от 1:");
        scanf("%zu%zu%zu", &n, &m, &k);
        clean_buffer();
    } while (!(n > 0 && m > 0 && k > 0));

    Matrix A = {
        (int*)calloc(n * m, sizeof(int)),
        n,
        m,
        m
    };
    size_t* B = (size_t*)calloc(k, sizeof(*B));

    printf("Введите матрицу A[%zu][%zu]:\n", n, m);
    for (size_t i = 0; i < n; i++)
    {
        for (size_t j = 0; j < m; j++)
        {
            scanf("%d", A.data + i * m + j);
        }
    }

    printf("Введите массив B[%zu]:\n", k);
    for (size_t i = 0; i < k; i++)
    {
        scanf("%zu", &B[i]);
    }
    // Сортировка по убыванию
    qsort(B, k, sizeof(*B), comparator);

    int sum = solution(&A, k, B);
    if (m == 0)
    {
        printf("Матрица полностью удалена, суммма элементов = 0\n");
    }
    else
    {
        printf("После удаления %zu столбцов:\n", A.m - A.current_m);
        for (size_t i = 0; i < A.n; i++)
        {
            printf("%d", *(A.data + i * m));
            for (size_t j = 1; j < A.current_m; j++)
            {
                printf(" %d", *(A.data + i * A.m + j));
            }
            printf("\n");
        }

        printf("Сумма элементов матрицы = %d\n", sum);
    }

    free(A.data);
    free(B);
}

static int solution(Matrix* A, size_t k, size_t* B)
{
    for (size_t i = 0; i < k; i++)
    {
        delete_column(B[i], A);
    }

    int sum = 0;

    for (size_t i = 0; i < A->n; i++)
    {
        for (size_t j = 0; j < A->current_m; j++)
        {
            sum += *(A->data + i * A->m + j);
        }
    }

    return sum;
}

static void delete_column(size_t column, Matrix* A)
{
    if (column >= A->current_m)
    {
        return;
    }

    for (size_t i = 0; i < A->n; i++)
    {
        for (size_t j = column; j < A->current_m - 1; j++)
        {
            *(A->data + i * A->m + j) = *(A->data + i * A->m + j + 1);
        }
    }

    A->current_m--;
}

static void clean_buffer()
{
    while (getchar() != '\n');
}
