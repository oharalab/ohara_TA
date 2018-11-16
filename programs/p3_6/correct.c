/* 
 * p3_6
 */

#include <stdio.h>

int main() {
  int a, b, tmp;

  a = 10;
  printf("a = %d\n", a);
  a = a + 5;
  printf("a = %d (a = a + 5)\n", a);
  b = 20;
  printf("a = %d, b = %d\n", a, b);
  a = b;
  b = a;
  printf("a = %d, b = %d (a = b, b = a)\n", a, b);
  a = 10;
  printf("a = %d, b = %d\n", a, b);
  tmp = a;
  a = b;
  b = tmp;
  printf("a = %d, b = %d (tmp = a, a = b, b = tmp)\n", a, b);

  return 0;
}

