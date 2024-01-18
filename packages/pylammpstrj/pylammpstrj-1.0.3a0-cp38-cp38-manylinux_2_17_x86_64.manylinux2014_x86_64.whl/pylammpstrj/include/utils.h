/**
 * \file
 * Contains the utilities' prototypes and definitions.
 *
 * Contains the trajectory, box, atom definitions as well as
 * their `define`s, and their functions.
 */
#ifndef _UTILS_H
#define _UTILS_H

/** The maximum number of characters read at once. */
#define BUFFER_LIMIT 128

/** An enum to compare `Atom`s properties. */
enum Operator
{
    OPERATOR_LT,
    OPERATOR_LEQ,
    OPERATOR_EQ,
    OPERATOR_GEQ,
    OPERATOR_GT
};

/** Replaces all new line characters in `str` by `chr`. */
void string_remove_newlines(char *str, char chr);

#endif
