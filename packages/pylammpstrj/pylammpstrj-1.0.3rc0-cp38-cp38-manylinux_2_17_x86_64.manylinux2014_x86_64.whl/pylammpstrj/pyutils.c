#include "atom.h"
#include "utils.h"

#include <Python.h>

enum Operator parse_operator(const long input_op)
{
    enum Operator op = (enum Operator) input_op;
    if (op < 0 || 4 < op)  // Assuming there are only 4 comparison operators
        PyErr_SetString(
            PyExc_RuntimeError,
            "Invalid operator: pylammpstrj operators should be used.");
    return op;
}

unsigned int parse_field_name(const struct AtomBuilder atom_builder,
                                     const char *field_name)
{
    for (unsigned int f = 0; f < atom_builder.N_fields; f++)
        if (strcmp(field_name, atom_builder.field_names[f]) == 0) return f;
    PyErr_SetString(PyExc_RuntimeError,
                    "Attribute does not match any attribute.");
    return 0;
}

union AtomField parse_value(const struct AtomBuilder atom_builder,
                                   const unsigned int field,
                                   PyObject *input_value)
{
    enum AtomFieldType type = atom_builder.fields_types[field];
    union AtomField value = {0};
    if (PyObject_TypeCheck(input_value, &PyLong_Type) &&
        type == AFT_INT)  // Only accepts PyLong
        value.i = (int) PyLong_AsLong(input_value);
    else if (type == AFT_DOUBLE)  // if double then accept PyFloat and PyLong
                                  // for convenience
    {
        if (PyObject_TypeCheck(input_value, &PyFloat_Type))
            value.d = PyFloat_AsDouble(input_value);
        else if (PyObject_TypeCheck(input_value, &PyLong_Type))
        {
            PyErr_Warn(PyExc_UserWarning, "value cast from 'int' to 'float'");
            value.d = PyLong_AsDouble(input_value);
        }
        else
            PyErr_SetString(PyExc_RuntimeError,
                            "Argument value does not match attribute type.");
    }
    else if (PyObject_TypeCheck(input_value, &PyUnicode_Type) &&
             type == AFT_STRING)
        strncpy(value.s, PyUnicode_AsUTF8(input_value), LABEL_LIMIT);
    else
        PyErr_SetString(PyExc_RuntimeError,
                        "Argument value does not match attribute type.");
    return value;
}

