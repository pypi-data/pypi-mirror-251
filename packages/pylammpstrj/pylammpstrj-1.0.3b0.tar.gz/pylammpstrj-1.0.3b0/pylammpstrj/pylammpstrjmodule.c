#define PY_SSIZE_T_CLEAN

#include "pylammpstrjmodule.h"
#include "pyatom.h"
#include "pybox.h"
#include "pytrajectory.h"
#include "trajectory.h"

#include <stdio.h>
#include <Python.h>
#include <pyerrors.h>

PyObject *pylammpstrj_read(PyObject *Py_UNUSED(self), PyObject *args,
                           PyObject *kwargs)
{
    char *kwlist[] = {"", "start", "delay", "batch_size", NULL};
    char *file_name;
    unsigned long start = 0;
    int delay = 0;
    unsigned int batch_size = 100;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "s|$ipi", kwlist, &file_name,
                                     &start, &delay, &batch_size))
        return NULL;

    // Initializing
    if (delay)
    {
        PyTrajectoryFileObject *pytrajectory_file =
            (PyTrajectoryFileObject *) PyTrajectoryFile_new(
                &PyTrajectoryFileType, NULL, NULL);
        if (pytrajectory_file == NULL)
            return NULL;

        struct TrajectoryFile trajectory_file = trajectoryfile_new(file_name, NULL, batch_size);
        if (errno != 0)
        {
            PyTrajectoryFileType.tp_free((PyObject *) pytrajectory_file);
            perror(
                "Error while creating the TrajectoryFile (pylammpstrj_read.trajectory_file)");
            return PyErr_SetFromErrno(PyExc_RuntimeError);
        }

        PyTrajectoryFile_initialize(pytrajectory_file, trajectory_file);
        return (PyObject *) pytrajectory_file;
    }

    PyTrajectoryObject *pytrajectory =
        (PyTrajectoryObject *) PyTrajectory_new(&PyTrajectoryType, NULL, NULL);
    if (pytrajectory == NULL)
        return NULL;

    struct Trajectory trajectory;
    trajectory_read(file_name, start, NULL, &trajectory);
    if (errno != 0)
    {
        PyTrajectoryType.tp_free((PyObject *) pytrajectory);
        perror("Error while reading the trajectory (pylammpstrj_read.trajectory)");
        return PyErr_SetFromErrno(PyExc_RuntimeError);
    }

    PyTrajectory_initialize(pytrajectory, trajectory);
    return (PyObject *) pytrajectory;
}

PyMethodDef pylammpstrj_methods[] = {
    {"read", (PyCFunction) pylammpstrj_read, METH_VARARGS | METH_KEYWORDS,
     "Read a trajectory file."},
    {0}};

struct PyModuleDef pylammpstrjmodule = {
    .m_base = PyModuleDef_HEAD_INIT,
    .m_name = "pylammpstrj",
    .m_doc = "A module to read and process LAMMPS trajectory files.",
    .m_size = -1,
    .m_methods = pylammpstrj_methods};

PyMODINIT_FUNC PyInit_pylammpstrj(void)
{
    PyObject *m;

    if (PyType_Ready(&PyAtomType) < 0) return NULL;
    if (PyType_Ready(&PyBoxType) < 0) return NULL;
    if (PyType_Ready(&PyTrajectoryType) < 0) return NULL;
    if (PyType_Ready(&PyTrajectoryFileType) < 0) return NULL;

    m = PyModule_Create(&pylammpstrjmodule);
    if (m == NULL) return NULL;

    Py_INCREF(&PyAtomType);
    if (PyModule_AddObject(m, "PyAtom", (PyObject *) &PyAtomType) < 0)
    {
        Py_DECREF(&PyAtomType);
        Py_DECREF(&m);
        return NULL;
    }

    Py_INCREF(&PyBoxType);
    if (PyModule_AddObject(m, "PyBox", (PyObject *) &PyBoxType) < 0)
    {
        Py_DECREF(&PyBoxType);
        Py_DECREF(&PyAtomType);
        Py_DECREF(&m);
        return NULL;
    }

    Py_INCREF(&PyTrajectoryType);
    if (PyModule_AddObject(m, "PyTrajectory", (PyObject *) &PyTrajectoryType) <
        0)
    {
        Py_DECREF(&PyTrajectoryType);
        Py_DECREF(&PyBoxType);
        Py_DECREF(&PyAtomType);
        Py_DECREF(&m);
        return NULL;
    }

    Py_INCREF(&PyTrajectoryFileType);
    if (PyModule_AddObject(m, "PyTrajectoryFile",
                           (PyObject *) &PyTrajectoryFileType) < 0)
    {
        Py_INCREF(&PyTrajectoryFileType);
        Py_DECREF(&PyTrajectoryType);
        Py_DECREF(&PyBoxType);
        Py_DECREF(&PyAtomType);
        Py_DECREF(&m);
        return NULL;
    }

    // Module constants
    PyModule_AddIntConstant(m, "LESS_THAN", (long) OPERATOR_LT);
    PyModule_AddIntConstant(m, "LESS_THAN_EQUAL_TO", (long) OPERATOR_LEQ);
    PyModule_AddIntConstant(m, "EQUAL_TO", (long) OPERATOR_EQ);
    PyModule_AddIntConstant(m, "GREATER_THAN_EQUAL_TO", (long) OPERATOR_GEQ);
    PyModule_AddIntConstant(m, "GREATER_THAN", (long) OPERATOR_GT);

    return m;
}
