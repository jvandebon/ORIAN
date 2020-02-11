#ifndef __RANDOMVARIABLE_H
#define __RANDOMVARIABLE_H

class RandomVariable {
public:
   static double PDF (double x);
   static double PDF (double x, double m, double s);
   static double CDF (double x);
   static double CDF (double x, double m, double s);
};

#endif
