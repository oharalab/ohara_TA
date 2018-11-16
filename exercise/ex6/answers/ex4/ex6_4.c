#include <stdio.h>

int main() {
  int heighest = 0, sec_heighest = 0;
  int height;
  int i;

  for (i = 1; i <= 10; i ++) {
    printf("%d番目の身長を入力 : ", i);
    scanf("%d", &height);

    if (heighest < height) {
      sec_heighest = heighest;
      heighest = height;
    } else if (sec_heighest < height) {
      sec_heighest = height;
    }
  }

  printf("一番めに背が高いのは%d\n", heighest);
  printf("二番めに背が高いのは%d\n", sec_heighest);

  return 0;
}
