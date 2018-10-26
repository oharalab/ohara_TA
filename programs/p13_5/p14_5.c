#include <stdio.h>

int main() {
  char buf[64];
  char file[32] = "p14_5.c";

  FILE *input;

  if((input = fopen(file, "r")) == NULL) {
    printf("開けませんでした\n");
    return 1;
  }
  while(fgets(buf, 64, input) != NULL) {
    printf("%s", buf);
  }
  fclose(input);

  return 0;
}
