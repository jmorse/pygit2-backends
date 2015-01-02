#include <Python.h>

PyMethodDef module_methods[] = {
  {NULL}
};


#if PY_MAJOR_VERSION < 3
PyMODINIT_FUNC
init_pygit2_backends(void)
{
  PyObject* m;
  m = Py_InitModule3("_pygit2_backends", module_methods,
                     "Backend facilities for pygit2");
  (void)m;
  return;
}
#else
struct PyModuleDef moduledef = {
  PyModuleDef_HEAD_INIT,
  "_pygit2_backends",              /* m_name */
  "Backend facilities for pygit2", /* m_doc */
  -1,                              /* m_size */
  module_methods,                  /* m_methods */
  NULL,                            /* m_reload */
  NULL,                            /* m_traverse */
  NULL,                            /* m_clear */
  NULL,                            /* m_free */
};

PyMODINIT_FUNC
init_pygit2_backends(void)
{
  PyObject* m;
  m = PyModule_Create(&moduledef);
  return m;
}
#endif
