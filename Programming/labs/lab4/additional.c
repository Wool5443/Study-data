// Найти подстроку-палиндром

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

static bool is_palindrome(const char* start, const char* end);
static void print_string(const char* start, const char* end);

static void solution(const char* string)
{
    printf("Naive\n");

    size_t len = strlen(string);

    for (const char* start = string; start < string + len; start++)
    {
        for (const char* end = start + 1; end < string + len; end++)
        {
            if (is_palindrome(start, end))
            {
                print_string(start, end);
                printf("\n");
            }
        }
    }
}

static void solution2(const char* string)
{
    printf("Linear\n");

    size_t len = strlen(string);
    size_t new_len = 2 * len + 3;
    char* new_string = calloc(new_len + 1, 1);

    constexpr char GUARD = 1;

    new_string[0] = GUARD;
    new_string[new_len - 2] = '\0';
    new_string[new_len - 1] = GUARD;

    for (size_t i = 0; i < len; i++)
    {
        new_string[2 * i + 1] = '\0';
        new_string[2 * i + 2] = string[i];
    }

    size_t* radiuses = calloc(new_len, sizeof(*radiuses));

    for (size_t i = 1; i < new_len - 1; i++)
    {
        size_t r = 0;

        while (new_string[i - r] != GUARD && new_string[i + r] != GUARD && new_string[i - r] == new_string[i + r])
        {
            r++;
        }
        r--;
        radiuses[i] = r;
    }

    for (size_t i = 0; i < new_len; i++)
    {
        if (radiuses[i] > 1)
        {
            const char* start = &new_string[i - radiuses[i]];
            const char* end = &new_string[i + radiuses[i]];

            while (start <= end)
            {
                if (*start != '#')
                {
                    fputc(*start, stdout);
                }
                start++;
            }
            printf("\n");
        }
    }
    free(new_string);
    free(radiuses);
}

int main()
{
    const char* s = "abEFEdabdABBAabdabd";
    // s = "AA";
    s = "ABBBBBA";
    solution(s);
    solution2(s);
}

static bool is_palindrome(const char* start, const char* end)
{
    while (start < end)
    {
        if (*start != *end)
        {
            return false;
        }
        start++;
        end--;
    }
    return true;
}

static void print_string(const char* start, const char* end)
{
    while (start <= end)
    {
        fputc(*start, stdout);
        start++;
    }
}
