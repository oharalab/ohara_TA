#include <stdio.h>

int main() {
  int i;
  char name[32];

  for (i = 0; i < 32; i ++)
    name[i] = '\0';

  printf("名前をローマ字で入力してください：");
  scanf("%[^\n]", name);

  for (i = 0; i < 32; i ++) {
    if (name[i] == ' ')
      continue;
    if (name[i] == '\0')
      break;
    printf("%c[%d]\n", name[i], name[i]);
  }

  return 0;
}
