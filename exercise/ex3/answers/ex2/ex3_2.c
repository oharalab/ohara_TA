#include <stdio.h>
#include <math.h>

int main(){
	double a, b, c = 100;

	a = log10(c);
	b = log10(6.0 / 16.0);

	printf("a = %7.3f\n", a);
	printf("b = %7.3f\n", b);
	printf("c = %7.3f\n", c);

	printf("b = %7.3f\n", log10(2) + log10(3) - log10(16));

	return(0);
        
}
