#include "RandomVariable.h"
#include <math.h>

#define SQRT_2PI 2.50662827463100050242

double RandomVariable::PDF (double x) {
   return exp(-x * x / 2) / SQRT_2PI; // sqrt(2 * M_PI);
}

double RandomVariable::PDF (double x, double m, double s) {
	return PDF ((x - m) / s) / s;
}

double RandomVariable::CDF (double x) {
	if (x < -8.0)
		return 0.0;
   if (x >  8.0)
		return 1.0;
   double s = 0.0, t = x;
	for (int i = 3; s + t != s; i += 2) {
		s = s + t;
		t = t * x * x / i;
	}
	return 0.5 + s * PDF(x);
}

double RandomVariable::CDF (double x, double m, double s) {
	return CDF ((x - m) / s);
} 
