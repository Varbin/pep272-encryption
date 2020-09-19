#include <Python.h>

#include <stdlib.h>


static PyObject* fast_xor(PyObject *self, PyObject *args, PyObject *kwargs) {
    Py_ssize_t a_length, b_length, length;
    char *a, *b, *out;

    if(!PyArg_ParseTuple(args, "y#y#",
                         &a, &a_length, &b, &b_length)) {
        return NULL;
    }

    if (NULL == a || NULL == b) {
        PyErr_SetString(PyExc_TypeError, "One of the parameters is None");
        return NULL;
    }

    if (0 == a_length || 0 == b_length) {
        // Both are non-zero
        return Py_BuildValue("y#", a, 0);
    }

    length = a_length < b_length ? a_length : b_length;
    out = malloc(length);

    for (Py_ssize_t i = 0; i < length; i++) {
        out[i] = a[i] ^ b[i];
    }

    PyObject* output = Py_BuildValue("y#", out, length);
    free(out);

    return output;
};


static PyMethodDef fastXorMethods[] = {
    {"fast_xor", (PyCFunction) fast_xor, METH_VARARGS, "XOR to bytestrings"},
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef fastXorModule = {
    PyModuleDef_HEAD_INIT,
    "_fast_xor",
    NULL,
    -1,
    fastXorMethods
};

PyMODINIT_FUNC
PyInit__fast_xor() {
    return PyModule_Create(&fastXorModule);
}
