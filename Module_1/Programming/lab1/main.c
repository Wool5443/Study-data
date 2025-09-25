#include <stdio.h>

void clean_buffer(void);

int main()
{
    constexpr size_t LMAX = 256;

    size_t n = 0;
    do
    {
        printf("Введите n от 1 до %zu", LMAX);
        scanf("%zu", &n);
        clean_buffer();
    } while (!(1 <= n && n <= LMAX));
}

void clean_buffer(void)
{
    for (int c = getchar(); c != '\n' && c != EOF; c = getchar());
}
