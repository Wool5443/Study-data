#include "common.h"

typedef struct Array
{
    int data[LMAX];
} Array;

static Array input_array(size_t n);
static void output_array(size_t n, int array[n]);

int main()
{
    printf("Лабораторная работа №3\nЗадание №3\n");

    size_t n = input_n();
    Array a = input_array(n);

    int counts[LMAX] = {};
    for (int* p = counts; p < counts + n; p++)
    {
        *p = 1;
    }

    for (int* ai = a.data + 1, *ci = counts + 1; ai < a.data + n; ai++, ci++)
    {
        for (int* aj = a.data, *cj = counts; aj < ai; aj++, cj++)
        {
            if (*aj == *ai)
            {
                ++*cj;
                *ci = *cj;
            }
        }
    }

    printf("Частоты чисел в массиве:\n");
    output_array(n, counts);

    size_t k = 1;

    Array b = {};
    b.data[0] = a.data[0];

    for (int* ai = a.data + 1; ai < a.data + n; ai++)
    {
        int* found = b.data;
        while (found < b.data + k && *found != *ai)
        {
            found++;
        }

        if (found == b.data + k)
        {
            *found = *ai;
            k++;
        }
    }

    printf("Уникальные числа в массиве в количестве %zu штук:\n", k);
    output_array(k, b.data);
}

static Array input_array(size_t n)
{
    printf("Введите целочисленный массив A[0:n-1]:\n");

    Array a = {};
    int* p = a.data;

    for (size_t i = 0; i < n; i++)
    {
        scanf("%d", p++);
    }

    return a;
}

static void output_array(size_t n, int array[n])
{
    if (n == 0)
    {
        return;
    }

    printf("%d", *array);

    for (int* p = array + 1; p < array + n; p++)
    {
        printf(" %d", *p);
    }
    printf("\n");
}
