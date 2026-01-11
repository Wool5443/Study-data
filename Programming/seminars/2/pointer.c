#include <stdio.h>
#include <limits.h>

constexpr size_t LMAX = 100;

int main()
{
    size_t na = 0;
    do
    {
        printf("Input length of A. Should be an integer from 1 to %zu\n", LMAX);
        scanf("%zu", &na);
        while (getchar() != '\n');
    } while (!(0 < na && na < LMAX));

    printf("Input A\n");
    int a[LMAX] = {};
    int* aptr = a;
    for (; aptr < a + na; aptr++)
    {
        scanf("%d", aptr);
    }

    int b[LMAX] = {};
    size_t nb = 0;
    for (int* aptr = a; aptr < a + na; aptr++)
    {
        int* bptr = b;
        for (; bptr < b + nb && *bptr != *aptr; bptr++);
        if (bptr == b + nb)
        {
            *bptr = *aptr;
            nb++;
        }
    }

    printf("B:\n");
    for (int* bptr = b; bptr < b + nb; bptr++)
    {
        printf("%d ", *bptr);
    }
    printf("\n");
}
