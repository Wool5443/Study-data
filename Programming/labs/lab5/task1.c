#include <stdio.h>
#include <math.h>

static void read_stdin(const char* save_path);
static double find_max_neg(const char* path);

int main()
{
    puts("Лабораторная работа №5");

    puts("Задание №1");

    read_stdin("data.txt");

    double max = find_max_neg("data.txt");

    if (max == -INFINITY)
    {
        puts("В последовательности не было отрицательных чисел");
    }
    else
    {
        printf("max = %lg\n", max);
    }
}

static void read_stdin(const char* save_path)
{
    FILE* save = fopen(save_path, "w");

    char buffer[512] = "";

    puts("Введите действительные числа, ввод закончите пустой строкой:");

    fgets(buffer, sizeof(buffer), stdin);
    while (buffer[1] != '\0')
    {
        double n = 0;
        sscanf(buffer, "%lg", &n);
        fprintf(save, "%lg\n", n);
        fgets(buffer, sizeof(buffer), stdin);
    }

    fclose(save);
}

static double find_max_neg(const char* path)
{
    FILE* f = fopen(path, "r");

    char buffer[512] = "";

    double max = -INFINITY;

    while (fgets(buffer, sizeof(buffer), f))
    {
        double n = 0;
        sscanf(buffer, "%lg", &n);

        if (n < 0 && n > max)
        {
            max = n;
        }
    }

    fclose(f);

    return max;
}
