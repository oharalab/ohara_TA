#include <stdio.h>

int main() {
  int year, month, days;

  printf("年を入力>");
  scanf("%d", &year);

  printf("月を入力>");
  scanf("%d", &month);

  switch (month) {
  case 1: case 3: case 5:
  case 7: case 8: case 10:
  case 12:
    days = 31; break;

  case 4: case 6: case 9:
  case 11:
    days = 30; break;

  case 2:
    if (year % 400 == 0) {
      days = 29;
    } else if (year % 100 == 0) {
      days = 28;
    } else if (year % 4 == 0) {
      days = 29;
    } else {
      days = 28;
    }
    break;
  }
  
  printf("%d年%d月の日数は%d日です\n", year, month, days);

  return 0;
}
