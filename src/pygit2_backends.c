#include <Python.h>
#include <git2.h>
#include <git2/odb_backend.h>

/* Declare other symbols that are going to be linked into this module. In an
 * ideal world the backends repo would export these via a header, that can be
 * worked towards */

int git_odb_backend_mysql_open(git_odb_backend **backend_out,
         const char *mysql_host,
         const char *mysql_user, const char *mysql_passwd, const char *mysql_db,
         unsigned int mysql_port, const char *mysql_unix_socket,
	 unsigned long mysql_client_flag);

int git_odb_backend_mysql_create(const char *mysql_host,
         const char *mysql_user, const char *mysql_passwd, const char *mysql_db,
         unsigned int mysql_port, const char *mysql_unix_socket,
	 unsigned long mysql_client_flag);

PyObject *
open_mysql_backend(PyObject *self, PyObject *args)
{
  const char *host, *user, *passwd, *sql_db, *unix_socket;
  git_odb_backend *backend;
  int portno, ret;

  if (!PyArg_ParseTuple(args, "ssssis", &host, &user, &passwd, &sql_db,
			  &portno, &unix_socket))
    return NULL;

  /* XXX -- allow for connection options such as compression and SSL */
  ret = git_odb_backend_mysql_open(&backend, host, user, passwd, sql_db, portno,
		  unix_socket, 0);
  if (ret == GIT_ENOTFOUND) {
    PyErr_Format(PyExc_Exception, "No git db found in specified database");
    return NULL;
  } else if (ret < 0) {
    /* An error occurred -- XXX however there's currently no facility for
     * identifying what error that is and telling the user about it, which is
     * poor. For now, just raise a generic error */
    PyErr_Format(PyExc_Exception, "Failed to connect to mysql server");
    return NULL;
  }

  /* On success, return a PyCapsule containing the created backend for the
   * moment. TODO, in the future pump this into a repository structure.
   * No destructor, manual deallocation occurs */
  return PyCapsule_New(backend, "", NULL);
}

PyObject *
create_mysql_backend(PyObject *self, PyObject *args)
{
  const char *host, *user, *passwd, *sql_db, *unix_socket;
  int portno, ret;

  if (!PyArg_ParseTuple(args, "ssssis", &host, &user, &passwd, &sql_db,
			  &portno, &unix_socket))
    return NULL;

  /* XXX -- allow for connection options such as compression and SSL */
  ret = git_odb_backend_mysql_create(host, user, passwd, sql_db, portno,
                                     unix_socket, 0);
  if (ret < 0) {
    /* An error occurred -- XXX however there's currently no facility for
     * identifying what error that is and telling the user about it, which is
     * poor. For now, just raise a generic error */
    PyErr_Format(PyExc_Exception, "Failed to create git db");
    return NULL;
  }

  Py_RETURN_NONE;
}

PyMethodDef module_methods[] = {
  {"open_mysql_backend", open_mysql_backend, METH_VARARGS, NULL},
  {"create_mysql_backend", create_mysql_backend, METH_VARARGS, NULL},
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
