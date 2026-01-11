#include <assert.h>

#include "common.h"

typedef struct Matrix
{
    int data[LMAX + 1][LMAX + 1];
} Matrix;

static Matrix input_matrix(size_t n);
static int max(size_t n, size_t i, const Matrix* matrix);

int main()
{
    printf("Лабораторная работа №3\nЗадание №2\n");

    size_t n = input_n();
    Matrix matrix = input_matrix(n);

    int min = max(n, 1, &matrix);

    for (size_t i = 2; i <= n; i++)
    {
        int t = max(n, i, &matrix);
        if (t < min)
        {
            min = t;
        }
    }

    printf("Минимальный максимум строк матрицы = %d\n", min);
}

static Matrix input_matrix(size_t n)
{
    printf("Введите целочисленную матрицу C[1:n, 1:n]:\n");

    Matrix m = {};
    for (size_t i = 1; i <= n; i++)
    {
        for (size_t j = 1; j <= n; j++)
        {
            scanf("%d", &m.data[i][j]);
        }
    }

    return m;
}

static int max(size_t n, size_t i, const Matrix* matrix)
{
    assert(matrix);

    int max = matrix->data[i][1];

    for (size_t j = 2; j <= n; j++)
    {
        if (matrix->data[i][j] > max)
        {
            max = matrix->data[i][j];
        }
    }

    return max;
}
