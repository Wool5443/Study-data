#ifndef COMMON_H_
#define COMMON_H_

#include <stdio.h>

static constexpr size_t LMAX = 512;

static void clean_buffer(void)
{
    while (getchar() != '\n');
}

[[maybe_unused]] static size_t input_n(void)
{
    size_t n = 0;
    do
    {
        printf("Введите n от 1 до %zu:\n", LMAX);
        scanf("%zu", &n);
        clean_buffer();
    } while (!(1 <= n && n <= LMAX));

    return n;
}

#endif // COMMON_H_
