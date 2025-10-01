// Sum of auxilarry diagonal

#include <stdio.h>

int main()
{
    int matrix[][3] = {
        {1, 2, 3},
        {4, 5, 6},
        {7, 8, 9},
    };

    // aux: 0 2, 1, 1, 2, 0 : sum = N - 1

    size_t N = sizeof(matrix) / sizeof(*matrix);

    int sum = 0;

    for (size_t i = 0; i < N; i++)
    {
        sum += matrix[i][N - 1 - i];
    }

    printf("%d\n", sum);

}
