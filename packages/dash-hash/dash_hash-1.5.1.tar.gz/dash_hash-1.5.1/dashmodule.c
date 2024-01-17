#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "dash.h"

#if PY_MAJOR_VERSION >= 3 || PY_MAJOR_VERSION == 3 && PY_MINOR_VERSION >= 7
#define SIZE_ARG_TYPE Py_ssize_t
#else
#define SIZE_ARG_TYPE int
#endif

static PyObject *dash_getpowhash(PyObject *self, PyObject *args)
{
    char *output;
    PyObject *value;
#if PY_MAJOR_VERSION >= 3
    PyBytesObject *input;
#else
    PyStringObject *input;
#endif
    if (!PyArg_ParseTuple(args, "S", &input))
        return NULL;
    Py_INCREF(input);
    output = PyMem_Malloc(32);

#if PY_MAJOR_VERSION >= 3
    dash_hash((char *)PyBytes_AsString((PyObject*) input), (int)PyBytes_Size((PyObject*) input), output);
#else
    dash_hash((char *)PyString_AsString((PyObject*) input), (int)PyString_Size((PyObject*) input), output);
#endif
    Py_DECREF(input);
#if PY_MAJOR_VERSION >= 3
    value = Py_BuildValue("y#", output, (SIZE_ARG_TYPE)32);
#else
    value = Py_BuildValue("s#", output, 32);
#endif
    PyMem_Free(output);
    return value;
}

static PyMethodDef DashMethods[] = {
    { "getPoWHash", dash_getpowhash, METH_VARARGS, "Returns the proof of work hash using dash hash" },
    { NULL, NULL, 0, NULL }
};

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef DashModule = {
    PyModuleDef_HEAD_INIT,
    "dash_hash",
    "...",
    -1,
    DashMethods
};

PyMODINIT_FUNC PyInit_dash_hash(void) {
    return PyModule_Create(&DashModule);
}

#else

PyMODINIT_FUNC initdash_hash(void) {
    (void) Py_InitModule("dash_hash", DashMethods);
}
#endif
