#include <stdio.h>

int main() {
  int price[10] = {100, 200, 300, 400, 500, 600, 700, 800, 900, 1000};
  int num;

  printf("商品番号を入力して下さい：");
  scanf("%d", &num);
  while (num < 0 || num > 10) {
    printf("商品番号は1から10までの整数にして下さい：");
    scanf("%d", &num);    
  }

  while (num != 0) {
    printf("商品%dの値段：%d円\n", num, price[num-1]);

    printf("商品番号を入力して下さい：");
    scanf("%d", &num);
    while (num < 0 || num > 10) {
      printf("商品番号は1から10までの整数にして下さい：");
      scanf("%d", &num);    
    }
  }
  printf("終了します\n");

  return 0;
}
