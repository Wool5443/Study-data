#include <stdio.h>
#include <math.h>
#include <stddef.h>

//FLAGS: "-lm"

void clean_buffer(void);
void print_array(size_t size, const double array[size]);

int main()
{
    constexpr size_t LMAX = 256;

    printf("Лабораторная работа №1\n");

    printf("Задание №1\n");

    size_t n = 0;
    do
    {
        printf("Введите n от 1 до %zu:\n", LMAX);
        scanf("%zu", &n);
        clean_buffer();
    } while (!(1 <= n && n <= LMAX));

    double a = 0, x = 0, h = 0;
    do
    {
        printf("Введите a, x, h:\n");
        scanf("%lg%lg%lg", &a, &x, &h);
        clean_buffer();
    }
    while (!isfinite(a) || !isfinite(x) || !isfinite(h));

    double r[LMAX + 1] = {};
    for (size_t i = 1; i <= n; i++)
    {
        r[i] = 1.25 * sin(3 * a * x - i * h);
    }

    print_array(n, r);

    printf("Задание №2\n");

    size_t n1 = 1;
    for (size_t i = 2; i <= n; i++)
    {
        if (fabs(r[i]) > fabs(r[n1]))
        {
            n1 = i;
        }
    }

    size_t n2 = n + 1;
    for (size_t i = 1; i <= n; i++)
    {
        if (r[i] > 0)
        {
            n2 = i;
        }
    }

    if (n1 > n2)
    {
        size_t c = n1;
        n1 = n2;
        n2 = c;
    }

    ptrdiff_t m = n2 - n1 - 1;

    size_t k = m > 0 ? n - m : n;
    for (size_t i = n1 + 1; i <= k; i++)
    {
        r[i] = r[i + m];
    }

    if (k < n)
    {
        print_array(k, r);
    }
    else
    {
        printf("Нет удалений\n");
    }

    printf("Задание №3\n");

    size_t km = 1;
    for (size_t i = 2; i <= k; i++)
    {
        if (r[i] <= r[km])
        {
            km = i;
        }
    }

    double sum = 0;
    for (size_t i = 1; i <= km; i++)
    {
        sum += r[i];
    }

    double average = sum / km;

    printf("Среднее вышло: %lg\n", average);
}

void print_array(size_t size, const double array[size])
{
    printf("%lg", array[1]);
    for (size_t i = 2; i <= size; i++)
    {
        printf(" %lg", array[i]);
    }
    printf("\n");
}

void clean_buffer(void)
{
    while (getchar() != '\n');
}
