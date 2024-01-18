#include "atom.h"
#include "utils.h"

#include <Python.h>

enum Operator parse_operator(const long input_op);

unsigned int parse_field_name(const struct AtomBuilder atom_builder,
                              const char *field_name);

union AtomField parse_value(const struct AtomBuilder atom_builder,
                            const unsigned int field, PyObject *input_value);
