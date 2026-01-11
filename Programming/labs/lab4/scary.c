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
}

