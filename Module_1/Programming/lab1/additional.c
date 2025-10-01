// Find pair with max sum

#include <limits.h>
#include <stdio.h>

#define MAX(x__, y__)                                                          \
    ({                                                                         \
        auto x_t = (x__);                                                      \
        auto y_t = (y__);                                                      \
        x_t > y_t ? x_t : y_t;                                                 \
    })

int main()
{
    constexpr int array[] = {3,   42,  -38, -7,  -8,  -43, -9, 30,  11,  14,
                             20,  32,  17,  -36, -28, 2,   20, -39, -14, 9,
                             21,  -4,  -30, 22,  40,  -30, 28, -27, 44,  -6,
                             -11, 42,  25,  0,   3,   45,  31, 42,  -40, 8,
                             24,  -45, -36, 1,   -36, -2,  16, -35, 1,   33};

    constexpr size_t N = sizeof(array) / sizeof(*array);

    int prev_max = array[0];
    int max_sum = INT_MIN;

    for (size_t i = 1; i < N; i++)
    {
        max_sum = MAX(max_sum, array[i] + prev_max);
        prev_max = MAX(prev_max, array[i]);
    }

    printf("Max sum = %d\n", max_sum);

    max_sum = 0;

    for (size_t i = 0; i < N; i++)
    {
        for (size_t j = i + 1; j < N; j++)
        {
            max_sum = MAX(max_sum, array[i] + array[j]);
        }
    }

    printf("Max sum = %d\n", max_sum);
}
