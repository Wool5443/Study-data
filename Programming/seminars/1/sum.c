#include <stdio.h>
#include <stdint.h>

constexpr size_t L_MAX = SIZE_MAX;

int main()
{
    printf("%lf\n", 2.545);


    printf("Input array size\n");
    size_t n = 0;
    scanf("%zu", &n);

    printf("Input array\n");
    float a[SIZE_MAX + 1] = {};

    for (size_t i = 1; i <= n; i++)
    {
        scanf("%g", &a[i]);
    }

    size_t n1 = 0, n2 = 0;

    for (size_t i = 1; i <= n; i++)
    {
        if (a[i] < 0)
        {
            if (n1 == 0)
            {
                n1 = i;
            }
            n2 = i;
        }
    }

    if (n1 == 0)
    {
        printf("no negative elements\n");
    }
    else if (n1 == n2)
    {
        printf("one negative element: %lg\n", a[n1]);
    }
    else
    {
        float s = 0;
        for (size_t i = n1; i <= n2; i++)
        {
            s += a[i];
        }
        printf("%lg\n", s);
    }
}
