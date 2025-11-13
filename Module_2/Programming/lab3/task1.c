#include <math.h>

#include "common.h"

typedef struct Function
{
    union
    {
        struct
        {
            double X1, X2, X3, Y1, Y2, Y3;
        };
        double table[2][3];
    };
} Function;

static Function input_function_table(void);
static double input_x(double x1, double x3);
static double interpolate(double x, double x_left, double y_left, double x_right, double y_right);

int main()
{
    printf("Лабораторная работа №3\nЗадание №1\n");

    Function f = input_function_table();
    double x = input_x(f.X1, f.X3);

    double res = NAN;

    if (f.X1 <= x && x < f.X2)
    {
        res = interpolate(x, f.X1, f.Y1, f.X2, f.Y2);
    }
    else if (f.X2 <= x && x < f.X3)
    {
        res = interpolate(x, f.X2, f.Y2, f.X3, f.Y3);
    }
    else
    {
        res = f.Y3;
    }

    printf("Приблизительное значение функции = %lg\n", res);
}

static Function input_function_table(void)
{
    Function f = {};
    do
    {
        printf("Введите действительные X1, X2, X3, Y1, Y2, Y3:\n");
        for (size_t i = 0; i < sizeof(f) / sizeof(**f.table); i++)
        {
            scanf("%lg", *f.table + i);
        }
        clean_buffer();
    } while
    (!(
        isfinite(f.X3) && isfinite(f.Y1) && isfinite(f.Y2) && isfinite(f.Y3)
        && f.X1 <= f.X2 && f.X2 <= f.X3
    ));

    return f;
}

static double input_x(double x1, double x3)
{
    double x = NAN;
    do
    {
        printf("Введите действительный x, принадлежащий [X1, X3]:\n");
        scanf("%lg", &x);
        clean_buffer();
    } while (!(x1 <= x && x <= x3));

    return x;
}

static double interpolate(double x, double x_left, double y_left, double x_right, double y_right)
{
    return y_left + (x - x_left) * (y_right - y_left) / (x_right - x_left);
}
