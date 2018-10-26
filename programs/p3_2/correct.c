/* 
 * p3_2.c
 */

#include <stdio.h>
#include <limits.h>

int main() {

  printf("char のサイズ: %d bit\n", CHAR_BIT);
  printf("char の最大値: %u\n", CHAR_MAX);
  printf("char の最小値: %d\n", CHAR_MIN);
  printf("int の最大値: %d\n", INT_MAX);
  printf("int の最大値: %d\n", INT_MIN);
  printf("long の最大値: %ld\n", LONG_MAX);
  printf("long の最小値: %ld\n", LONG_MIN);
  printf("signed char の最大値: %d\n", SCHAR_MAX);
  printf("signed char の最小値: %d\n", SCHAR_MIN);
  printf("short の最大値: %d\n", SHRT_MAX);
  printf("short の最小値: %d\n", SHRT_MIN);
  printf("unsigned char の最大値: %u\n", UCHAR_MAX);
  printf("unsigned int の最大値: %u\n", UINT_MAX);
  printf("unsigned long の最大値: %lu\n", ULONG_MAX);
  printf("unsigned short の最大値: %u\n", USHRT_MAX);

  return 0;
}

