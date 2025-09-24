#include <stdio.h>
#include <limits.h>

bool is_in_matrix(int value, const int* array, size_t n)
{
    for (size_t i = 0; i < n; i++)
    {
        if (array[i] == value)
        {
            return true;
        }
    }
    return false;
}

int main()
{
    constexpr size_t LMAX = 100;

    size_t na = 0, ma = 0;
    do
    {
        printf("Input dimensions of A [1; %zu]\n", LMAX);
        scanf("%zu%zu", &na, &ma);
        while (getchar() != '\n');
    } while (!((1 <= na && na <= LMAX) && (1 <= ma && ma <= LMAX)));

    printf("Input A\n");
    int a[LMAX][LMAX] = {};
    for (size_t i = 0; i < na; i++)
    {
        for (size_t j = 0; j < ma; j++)
        {
            scanf("%d", &a[i][j]);
        }
    }

    printf("Input B\n");
    size_t nb = 0;
    do
    {
        printf("Input length of B [1; %zu]\n", LMAX);
        scanf("%zu", &nb);
        while (getchar() != '\n');
    } while (!(1 <= nb && nb <= LMAX));

    int b[LMAX] = {};
    for (size_t i = 0; i < nb; i++)
    {
        scanf("%d", b + i);
    }

    int min = INT_MAX;
    bool found_min = false;

    for (size_t i = 0; i < na; i++)
    {
        for (size_t j = 0; j < ma; j++)
        {
            if (!is_in_matrix(a[i][j], b, nb))
            {
                if (a[i][j] < min)
                {
                    min = a[i][j];
                    found_min = true;
                }
            }
        }
    }

    if (found_min)
    {
        printf("Found min: %d", min);
    }
    else
    {
        printf("No minumum");
    }
}
