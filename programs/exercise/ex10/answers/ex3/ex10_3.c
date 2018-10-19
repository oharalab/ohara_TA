#include <stdio.h>

int main(){
    int ch;

    while((ch = getchar()) != EOF){
      if (ch == '\n') {
        printf("\n");

      } else if (ch >= 65 && ch <= 90) {
        printf("%c", (char)ch);

      } else if (ch >= 97 && ch <= 122) {
        printf("%c", (char)(ch - 32));

      } else {
        printf("*");
      }
    }

    return (0);
}
