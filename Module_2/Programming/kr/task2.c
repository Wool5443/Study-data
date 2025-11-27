// Дана символьная строка. Обращаться к символам по указателю. Ввод
// данных, анализ существования и вывод результата оформить в главной
// функции, вычисления – в отдельной функции с параметрами. Заменить
// каждую цифру на латинскую букву. ‘a’ на ‘0’, ‘b’ на  ‘1’ и т.д.

#include <stdio.h>
#include <ctype.h>

static bool replace_latin(char* string);

int main()
{
    constexpr size_t STRING_SIZE = 512;

    printf("Введите строку длиной до %zu символов\n", STRING_SIZE - 1);
    char string[STRING_SIZE] = "";

    fgets(string, STRING_SIZE, stdin);

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
