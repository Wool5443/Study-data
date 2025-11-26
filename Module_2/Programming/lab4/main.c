#include <stddef.h>
#include <stdio.h>
#include <string.h>

constexpr size_t STRING_SIZE = 1024;
constexpr size_t ARRAY_SIZE = 1024;

typedef struct String
{
    const char* data;
    size_t size;
} String;

typedef struct String_array
{
    String data[ARRAY_SIZE];
    size_t size;
} String_array;

static String_array
find_all_substrings(size_t k, const char strings[ARRAY_SIZE][STRING_SIZE]);
static String_array find_substrings(const char* string);
static String find_substring_with_brackets_and_digits(const String_array* substrs);
static bool check_string(String string);
static void clean_non_cyrillic(String* string);

static void print_string(String str);
static size_t input_k(void);
static void clean_buffer(void);

int main()
{
    size_t k = input_k();

    printf("Введите %zu строк длины не более %zu:\n", k, STRING_SIZE - 1);
    char strings[ARRAY_SIZE][STRING_SIZE] = {};

    for (size_t i = 0; i < k; i++)
    {
        fgets(strings[i], STRING_SIZE, stdin);
    }

    String_array substrs = find_all_substrings(k, strings);
    if (substrs.size)
    {
        printf("Нашлось %zu подстрок, ограниченных точками:\n", substrs.size);
        for (size_t i = 0; i < substrs.size; i++)
        {
            print_string(substrs.data[i]);
            printf("\n");
        }
    }
    else
    {
        printf("Не нашлось подстрок, ограниченных точками\n");
    }

    String found = find_substring_with_brackets_and_digits(&substrs);

    if (found.size)
    {
        printf("Нашлась строка со скобками и цифрами: \"");
        print_string(found);
        printf("\"\n");

        clean_non_cyrillic(&found);
        printf("После очистки букв не из русского алфавита: \"");
        print_string(found);
        printf("\"\n");
    }
    else
    {
        printf("Не нашлось строки со скобками и цифрами\n");
    }
}

static String_array
find_all_substrings(size_t k, const char strings[ARRAY_SIZE][STRING_SIZE])
{
    String_array result = {};

    for (size_t i = 0; i < k; i++)
    {
        String_array sub_res = find_substrings(strings[i]);

        for (size_t j = 0; j < sub_res.size; j++)
        {
            result.data[result.size++] = sub_res.data[j];
        }
    }

    return result;
}

static String_array find_substrings(const char* string)
{
    String_array result = {};
    size_t len = strlen(string);

    const char* start = strchr(string, '.');
    if (!start)
    {
        return result;
    }

    while (start < string + len)
    {
        while (start < string + len && *start == '.')
        {
            start++;
        }
        const char* end = strchr(start, '.');

        if (!end)
        {
            break;
        }

        result.data[result.size++] = (String) {start, end - start};
        start = end;
    }

    return result;
}

static String find_substring_with_brackets_and_digits(const String_array* substrs)
{
    for (size_t i = 0; i < substrs->size; i++)
    {
        if (check_string(substrs->data[i]))
        {
            return substrs->data[i];
        }
    }
    return (String){};
}

static bool check_string(String string)
{
    bool has_brackets = memchr(string.data, '(', string.size)
                        && memchr(string.data, ')', string.size);
    if (!has_brackets)
    {
        return false;
    }

    for (char digit = '0'; digit <= '9'; digit++)
    {
        if (memchr(string.data, digit, string.size))
        {
            return true;
        }
    }

    return false;
}

static void clean_non_cyrillic(String* string)
{
    const char* read = string->data;
    char* write = (char*)read;
    size_t new_size = string->size;

    while (read < string->data + string->size)
    {
        if (*read & (1 << 8))
        {
            *(write++) = *read;
        }
        else
        {
            new_size--;
        }
        read++;
    }
    *write = '\0';
    string->size = new_size;
}

static void print_string(String str)
{
    for (size_t i = 0; i < str.size; i++)
    {
        fputc(str.data[i], stdout);
    }
}

static void clean_buffer(void)
{
    while (getchar() != '\n')
        ;
}

static size_t input_k(void)
{
    size_t k = 0;
    do
    {
        printf("Введите k от 1 до %zu:\n", ARRAY_SIZE);
        scanf("%zu", &k);
        clean_buffer();
    } while (!(1 <= k && k <= ARRAY_SIZE));

    return k;
}
