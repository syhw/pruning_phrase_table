#include <stdio.h>
#include <math.h>
#include <string.h>
#include <Python.h>

static PyObject *hypergeometric_distribution_ (PyObject *self, PyObject *args);
double hypergeometric_distribution (int i, int n, int B, int N);

////////////////////////////////////////////////////////////////////////////////

static PyObject *hypergeometric_distribution_ (PyObject *self, PyObject *args)
{
	int i, n, B, N;
	if (!PyArg_ParseTuple(args, "iiii", &i, &n, &B, &N))
		return NULL;
	
	double result = hypergeometric_distribution(i, n, B, N);

	return Py_BuildValue("d", result);
}

// Logarithm of the number of combinations of 'n' objects taken 'k' at a time
double ln_n_choose_k (int n, int k)
{
	return lgamma(n + 1) - lgamma(k + 1) - lgamma(n - k + 1);
}

// Compute the hypergeometric distribution, or probability that a list of
// n objects should contain i ones with a particular property when the
// list has been selected randomly without replacement from a set of N
// objects in which B exhibit the same property
double hypergeometric_distribution (int i, int n, int B, int N)
{
	return exp(ln_n_choose_k(B, i) + ln_n_choose_k(N - B, n - i) - ln_n_choose_k(N, n));
}

/* For education purpose: original Python implementation
 
def __hypergeometric_probability (i, n, B, N):
	return exp(
	  __lncombination(B, i) +
	  __lncombination(N - B, n - i) -
	  __lncombination(N, n)
	)
 
def __lncombination (n, p):
	return \
	  __lnfactorial(n) - \
	  __lnfactorial(p) - \
	  __lnfactorial(n - p)
 
# Logarithm of n! with algorithmic approximation
# Reference:
#   Lanczos, C. 'A precision approximation of the gamma function',
#   J. SIAM Numer. Anal., B, 1, 86-96, 1964."
#   http://www.matforsk.no/ola/fisher.htm 
def __lnfactorial (n):
	if (n <= 1):
		return 0
	else:
		return __lngamma(n + 1)
 
def __lngamma (z):
	x = 0
	x += 0.1659470187408462e-06 / (z + 7)
	x += 0.9934937113930748e-05 / (z + 6)
	x -= 0.1385710331296526 / (z + 5)
	x += 12.50734324009056 / (z + 4)
	x -= 176.6150291498386 / (z + 3)
	x += 771.3234287757674 / (z + 2)
	x -= 1259.139216722289 / (z + 1)
	x += 676.5203681218835 / (z)
	x += 0.9999999999995183
 
	return log(x) - 5.58106146679532777 - z + (z - 0.5) * log(z + 6.5)
*/

////////////////////////////////////////////////////////////////////////////////

static PyMethodDef methods[] =
{
	{"hypergeometric_distribution", hypergeometric_distribution_, METH_VARARGS, "hypergeometric_distribution"},
	{NULL, NULL, 0, NULL}
};


PyMODINIT_FUNC initenrichment_ (void)
{
	(void)Py_InitModule("enrichment_", methods);
}

main()
{
	int a, b, c;
	a, b, c = hypergeometric_distribution(2, 3, 2, 4);
	printf("%g %g %g\n", a, b, c);
}
