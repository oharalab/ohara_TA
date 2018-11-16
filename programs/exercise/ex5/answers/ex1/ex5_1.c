#include <stdio.h>

int main() {
  int price;

  printf("定価=");
  scanf("%d", &price);

  if (price % 10 == 0) {
    printf("代金=%d\n", price);
  } else {
    printf("定価が正しくありません．\n");
  }
}
