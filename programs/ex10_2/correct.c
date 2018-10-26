#include <stdio.h>

int main(){
    int ch;

    while((ch = getchar()) != EOF){
      if (ch == '\n') {
        printf("\n");
        continue;
      }
      printf("%c(%d)", (char)ch, ch);
    }

    return (0);
}
