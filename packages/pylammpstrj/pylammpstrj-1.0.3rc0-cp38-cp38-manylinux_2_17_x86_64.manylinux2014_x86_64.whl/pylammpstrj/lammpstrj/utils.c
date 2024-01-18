#include "utils.h"
#include <string.h>

void string_remove_newlines(char *str, char chr)
{
    for (int c = strlen(str) - 1; 0 <= c; c--)
        if (str[c] == '\0')
            continue;
        else if (str[c] == '\n')
            str[c] = chr;
}

