#define PY_SSIZE_T_CLEAN

#include "pytrajectory.h"
#include "atom.h"
#include "pyatom.h"
#include "pybox.h"
#include "pyutils.h"
#include "trajectory.h"

#include <errno.h>
#include <stdio.h>
#include <Python.h>
#include <listobject.h>

void PyTrajectory_dealloc(PyTrajectoryObject *self)
{
    trajectory_delete(&(self->trajectory));
    PyTrajectoryType.tp_free((PyObject *) self);
}

PyObject *PyTrajectory_new(PyTypeObject *type, PyObject *Py_UNUSED(args),
                           PyObject *Py_UNUSED(kwargs))
{
    PyTrajectoryObject *self;
    self = (PyTrajectoryObject *) type->tp_alloc(type, 0);
    return (PyObject *) self;
}

PyObject *PyTrajectory_get_N_configurations(PyTrajectoryObject *self,
                                            void *Py_UNUSED(closure))
{
    return (PyObject *) PyLong_FromLong(self->trajectory.N_configurations);
}

PyObject *PyTrajectory_get_steps(PyTrajectoryObject *self,
                                 void *Py_UNUSED(closure))
{
    unsigned long N_configurations;
    unsigned long *steps;
    N_configurations = self->trajectory.N_configurations;
    steps = (unsigned long *) self->trajectory.steps;

    PyObject *list = PyList_New(N_configurations);
    for (unsigned int c = 0; c < N_configurations; c++)
        PyList_SetItem(list, c, PyLong_FromLong(steps[c]));
    return list;
}

PyObject *PyTrajectory_get_N_atoms(PyTrajectoryObject *self,
                                   void *Py_UNUSED(closure))
{
    PyObject *list = PyList_New(self->trajectory.N_configurations);
    for (unsigned int c = 0; c < self->trajectory.N_configurations; c++)
        PyList_SetItem(list, c, PyLong_FromLong(self->trajectory.N_atoms[c]));
    return list;
}

PyObject *PyTrajectory_get_dump_format(PyTrajectoryObject *self,
                                       void *Py_UNUSED(closure))
{
    struct AtomBuilder atom_builder = self->trajectory.atom_builder;
    if (PyErr_Occurred()) return NULL;
    return PyUnicode_FromString(atom_builder.dump_format);
}

PyObject *PyTrajectory_get_field_names(PyTrajectoryObject *self,
                                       void *Py_UNUSED(closure))
{
    struct AtomBuilder atom_builder = self->trajectory.atom_builder;
    if (PyErr_Occurred()) return NULL;
    PyObject *list = PyList_New(atom_builder.N_fields);
    for (unsigned int f = 0; f < atom_builder.N_fields; f++)
        PyList_SetItem(list, f,
                       PyUnicode_FromString(atom_builder.field_names[f]));
    return list;
}

PyObject *PyTrajectory_get_additional_fields(PyTrajectoryObject *self,
                                             void *Py_UNUSED(closure))
{
    struct AtomBuilder atom_builder = self->trajectory.atom_builder;
    if (PyErr_Occurred()) return NULL;

    PyObject *list = PyList_New(atom_builder.N_additional);
    for (unsigned int f = 0, fa = 0; f < atom_builder.N_fields; f++)
    {
        if (!atom_builder.is_additional[f]) continue;
        PyList_SetItem(list, fa,
                       PyUnicode_FromString(atom_builder.field_names[f]));
        fa++;
    }
    return list;
}

PyObject *PyTrajectory_get_atoms(PyTrajectoryObject *self,
                                 void *Py_UNUSED(closure))
{
    PyObject *list = PyList_New(self->trajectory.N_configurations);
    if (list == NULL)
        return NULL;

    for (unsigned int c = 0, at = 0; c < self->trajectory.N_configurations; c++)
    {
        PyObject *inner_list = PyList_New(self->trajectory.N_atoms[c]);
        if (inner_list == NULL)
        {
            PyList_Type.tp_del(list);
            return NULL;
        }

        for (unsigned int a = 0; a < self->trajectory.N_atoms[c]; a++, at++)
        {
            PyAtomObject *atom =
                (PyAtomObject *) PyAtom_new(&PyAtomType, NULL, NULL);
            if (atom == NULL)
            {
                PyList_Type.tp_del(inner_list);
                PyList_Type.tp_del(list);
                return NULL;
            }

            PyAtom_initialize(atom, self, self->trajectory.atoms[at]);
            PyList_SetItem(inner_list, a, (PyObject *) atom);
        }
        PyList_SetItem(list, c, inner_list);
    }

    return list;
}

PyObject *PyTrajectory_get_boxes(PyTrajectoryObject *self,
                                 void *Py_UNUSED(closure))
{
    PyObject *list = PyList_New(self->trajectory.N_configurations);
    if (list == NULL)
        return NULL;

    for (unsigned int c = 0; c < self->trajectory.N_configurations; c++)
    {
        PyBoxObject *box = (PyBoxObject *) PyBox_new(&PyBoxType, NULL, NULL);
        if (box == NULL)
        {
            PyList_Type.tp_del(list);
            return NULL;
        }

        PyBox_initialize(box, self->trajectory.box[c]);
        PyList_SetItem(list, c, (PyObject *) box);
    }

    return list;
}

PyGetSetDef PyTrajectory_getset[] = {
    {.name = "N_configurations",
     .get = (getter) PyTrajectory_get_N_configurations,
     .doc = "The number of configurations"},
    {.name = "steps",
     .get = (getter) PyTrajectory_get_steps,
     .doc = "The timesteps."},
    {.name = "N_atoms",
     .get = (getter) PyTrajectory_get_N_atoms,
     .doc = "The number of configurations"},
    {.name = "dump_format",
     .get = (getter) PyTrajectory_get_dump_format,
     .doc = "The dump format."},
    {.name = "field_names",
     .get = (getter) PyTrajectory_get_field_names,
     .doc = "The names of the fields."},
    {.name = "additional_fields",
     .get = (getter) PyTrajectory_get_additional_fields,
     .doc = "The additionnal fields."},
    {.name = "atoms",
     .get = (getter) PyTrajectory_get_atoms,
     .doc = "The atoms."},
    {.name = "boxes",
     .get = (getter) PyTrajectory_get_boxes,
     .doc = "The boxes."},
    {NULL, NULL, NULL, NULL, NULL}};

PyObject *PyTrajectory_str(PyTrajectoryObject *self)
{
    return PyUnicode_FromFormat(
        "[%lu, %S, %s, %S, %S, %R]", self->trajectory.N_configurations,
        PyObject_Str(PyTrajectory_get_N_atoms(self, NULL)),
        PyObject_Str(PyTrajectory_get_dump_format(self, NULL)),
        PyObject_Str(PyTrajectory_get_field_names(self, NULL)),
        PyObject_Str(PyTrajectory_get_additional_fields(self, NULL)),
        PyObject_Repr(PyTrajectory_get_atoms(self, NULL)));
}

PyObject *PyTrajectory_repr(PyTrajectoryObject *self)
{
    return PyUnicode_FromFormat(
        "trajectory(N_configurations=%lu N_atoms=%S dump_format='%s' "
        "field_names=%S is_additional=%S atoms=%R)",
        self->trajectory.N_configurations,
        PyObject_Str(PyTrajectory_get_N_atoms(self, NULL)),
        PyObject_Str(PyTrajectory_get_field_names(self, NULL)),
        PyObject_Str(PyTrajectory_get_dump_format(self, NULL)),
        PyObject_Str(PyTrajectory_get_additional_fields(self, NULL)),
        PyObject_Repr(PyTrajectory_get_atoms(self, NULL)));
}

void PyTrajectory_initialize(PyTrajectoryObject *self,
                             struct Trajectory trajectory)
{
    self->trajectory = trajectory;
}

PyObject *PyTrajectory_select_atoms(PyTrajectoryObject *self, PyObject *args,
                                    PyObject *kwargs)
{
    char *kwlist[] = {"", "", "", "inplace", NULL};
    unsigned int field;
    enum Operator op;
    union AtomField value;
    char *field_name;
    long input_op;
    PyObject *input_value;  // Needs to be freed?
    int inplace = false;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "siO|$p", kwlist,
                                     &field_name, &input_op, &input_value,
                                     &inplace))
        return NULL;

    field = parse_field_name(self->trajectory.atom_builder, field_name);
    if (PyErr_Occurred()) return NULL;

    op = parse_operator(input_op);
    if (PyErr_Occurred()) return NULL;

    value = parse_value(self->trajectory.atom_builder, field, input_value);
    if (PyErr_Occurred()) return NULL;

    PyTrajectoryObject *new =
        (PyTrajectoryObject *) PyTrajectory_new(Py_TYPE(self), NULL, NULL);
    if (new == NULL)
        return NULL;

    struct Trajectory trajectory;
    if (!inplace)
    {
        select_atoms(&(self->trajectory), field, op, value, false, &trajectory);
        if (errno != 0) return PyErr_SetFromErrno(PyExc_RuntimeError);
        PyTrajectory_initialize(new, trajectory);
        return (PyObject *) new;
    }

    select_atoms(&(self->trajectory), field, op, value, true, NULL);
    if (errno != 0) return PyErr_SetFromErrno(PyExc_RuntimeError);

    // Need to return None otherwise it segfaults if the result is not assigned
    return Py_None;
}

PyObject *PyTrajectory_compute_average(PyTrajectoryObject *self, PyObject *args)
{
    char *field_name;
    if (!PyArg_ParseTuple(args, "s", &field_name)) return NULL;

    // Converting the field name
    unsigned int field =
        parse_field_name(self->trajectory.atom_builder, field_name);
    if (PyErr_Occurred()) return NULL;

    // Computing the averages
    unsigned int N_configurations = 0;
    double *averages = trajectory_average_property(self->trajectory, field);
    if (errno != 0)  // Something went wrong
    {
        perror(
            "Error while computing the average (PyTrajectory_compute_average)");
        return PyErr_SetFromErrno(PyExc_RuntimeError);
    }

    // Converting the array
    PyObject *list = PyList_New(N_configurations);
    if (PyErr_Occurred())
    {
        free(averages);
        return NULL;
    }

    for (unsigned int c = 0; c < self->trajectory.N_configurations; c++)
        PyList_SetItem(list, c, PyFloat_FromDouble(averages[c]));

    // Finishing
    free(averages);
    return list;
}

PyMethodDef PyTrajectory_methods[] = {
    {"select_atoms", (PyCFunction) PyTrajectory_select_atoms,
     METH_VARARGS | METH_KEYWORDS, "Select atoms."},
    {"average_property", (PyCFunction) PyTrajectory_compute_average,
     METH_VARARGS,
     "Computes the average of an atomic property throughout the simulation."},
    {NULL, NULL, 0, NULL}};

PyTypeObject PyTrajectoryType = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_name = "pylammpstrj.PyTrajectory",
    .tp_doc = "Trajectory objects",
    .tp_basicsize = sizeof(PyTrajectoryObject),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_dealloc = (destructor) PyTrajectory_dealloc,
    .tp_new = PyTrajectory_new,
    .tp_getset = PyTrajectory_getset,
    .tp_methods = PyTrajectory_methods,
    .tp_str = (reprfunc) PyTrajectory_str,
    .tp_repr = (reprfunc) PyTrajectory_repr};
