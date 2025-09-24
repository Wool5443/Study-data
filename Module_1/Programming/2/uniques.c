#include <stdio.h>
#include <limits.h>

constexpr size_t LMAX = 100;

int main()
{
    int a[LMAX] = {};

    size_t na = 0;
    do
    {
        printf("Input length of A. Should be an integer from 1 to %zu\n", LMAX);
        scanf("%zu", &na);
        while (getchar() != '\n');
    } while (!(0 < na && na < LMAX));

    printf("Input A\n");
    for (size_t i = 0; i < na; i++)
    {
        scanf("%d", a + i);
    }

    int b[LMAX] = {};
    size_t nb = 0;
    for (size_t i = 0; i < na; i++)
    {
        size_t j = 0;
        for (j = 0; j < nb && b[j] != a[i]; j++);
        if (j >= nb)
        {
            b[nb++] = a[i];
        }
    }

    printf("B:\n");
    for (size_t i = 0; i < nb; i++)
    {
        printf("%d ", b[i]);
    }
    printf("\n");
}
