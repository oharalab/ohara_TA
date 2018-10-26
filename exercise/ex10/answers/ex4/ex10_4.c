#include <stdio.h>
#include <ctype.h>

int main(){
  int ch;

  while((ch = getchar()) != EOF) {
    if (ch == '\n') {
      printf("\n");

    } else if (isalpha(ch)) {
      printf("%c", toupper(ch));

    } else {
      printf("*");
    }
  }

  return (0);
}
