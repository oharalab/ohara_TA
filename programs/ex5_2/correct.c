#include <stdio.h>

int main() {
  int num;

  printf("1, 2, 3のいずれかを入力してください:");
  scanf("%d", &num);

  switch(num) {
  case 2:
    printf("あたり\n");
    break;
  case 1:
  case 3:
    printf("はずれ\n");
    break;
  default:
    printf("無効です\n");
  }

  return 0;
}
