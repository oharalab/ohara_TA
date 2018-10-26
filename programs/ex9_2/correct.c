#include <stdio.h>

int main() {

  int i, num;
  printf("2以上の整数値を入力してください:");
  scanf("%d", &num);

  while (num > 0) {
    for(i = 2; i < num; i ++) {
      if (num % i == 0) {
        printf("素数ではありません\n");
        break;
      }
    }
    if (i == num) {
        printf("素数です\n");
    }
    printf("2以上の整数値を入力してください:");
    scanf("%d", &num);
  }
  printf("終了\n");

  return 0;
}
