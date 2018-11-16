#include <stdio.h>

int main() {

  int i;

  for (i = 32; i < 127; i ++) {
    printf("%c %3d  ", (char)i, i);

    if ((i + 1) % 8 == 0) {
      printf("\n");
    }
  }
  printf("\n");
  
  return 0;
}
