#include <stdio.h>
#include <string.h>

int main() {
  char sei[32], mei[32], name[64];

  printf("ローマ字で姓を入力．最後に空白1個を入力>");
  scanf("%[^\n]", sei); getchar();
  printf("ローマ字で名を入力>");
  scanf("%[^\n]", mei); getchar();

  strcpy(name, sei);
  strcat(name, mei);

  printf("あなたの名前は %s ですね\n", name);

  return 0;
}
