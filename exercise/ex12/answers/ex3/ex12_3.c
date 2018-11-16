#include <stdio.h>

int main() {
  int i, counter = 0;
  char input[63];
  char target;

  for (i = 0; i < 63; i ++ ) {
    input[i] = '\0';
  }

  printf("英字の文字列を入力(63字まで)>");
  scanf("%[^\n]", input); getchar();

  printf("数える英字は>");
  scanf("%c", &target);

  for (i = 0; i < 63; i ++) {
    if (input[i] == target)
      counter++;
  }
  printf("文字列：%s に含まれる %c の字数は %d個です\n", input, target, counter);

  return 0;
}
