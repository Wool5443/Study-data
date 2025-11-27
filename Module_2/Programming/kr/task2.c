// Дана символьная строка. Обращаться к символам по указателю. Ввод
// данных, анализ существования и вывод результата оформить в главной
// функции, вычисления – в отдельной функции с параметрами. Заменить
// каждую цифру на латинскую букву. ‘a’ на ‘0’, ‘b’ на  ‘1’ и т.д.

#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>

static bool replace_latin(char* string);

static void clean_buffer()
{
    while (getchar() != '\n');
}

int main()
{
    size_t len = 0;
    do
    {
        puts("Введите длину строки:");
        scanf("%zu", &len);
        clean_buffer();
    } while (len == 0);

    puts("Введите строку:");
    char* string = (char*)calloc(len + 1, 1);

    fgets(string, len, stdin);

    bool replaced = replace_latin(string);

    if (replaced)
    {
        puts("После замены:");
        puts(string);
    }
    else
    {
        puts("Замен не произошло");
    }

    free(string);
}

static bool replace_latin(char* string)
{
    bool replaced = false;
    while (*string)
    {
        if (isdigit(*string))
        {
            *string += 'a' - '0';
            replaced = true;
        }
        string++;
    }

    return replaced;
}
