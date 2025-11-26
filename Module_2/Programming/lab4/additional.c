// Найти подстроку-палиндром

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

static bool is_palindrome(const char* start, const char* end);
static void print_string(const char* start, const char* end);

static void solution(const char* string)
{
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

int main()
{
    const char* s = "abdabdABBAabdabd";
    solution(s);
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
