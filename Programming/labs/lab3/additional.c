#include <stdio.h>
#include <limits.h>

#define min(a, b) (a < b ? a : b)

int main()
{
    int a[] = {1, 2, 3, 7, 4, 5, 5, 5};
    // int a[] = {1, 2, 3};
    size_t n = sizeof(a) / sizeof(*a);
    size_t k = 3;

    int maxes[k] = {};
    for (size_t i = 0; i < k; i++)
    {
        maxes[i] = INT_MIN;
    }

    for (size_t i = 0; i < n; i++)
    {
        if (a[i] >= maxes[0])
        {
            for (size_t j = 1; j <= min(i, k - 1); j++)
            {
                maxes[k - j] = maxes[k - j - 1];
            }
            maxes[0] = a[i];
        }
        for (size_t i = 0; i < k; i++)
        {
            printf("%d ", maxes[i]);
        }
        printf("\n");
    }

    for (size_t i = 0; i < k; i++)
    {
        printf("%d ", maxes[i]);
    }
    printf("\n");
}
