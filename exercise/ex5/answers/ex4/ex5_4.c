#include <stdio.h>

int main() {
  int year, month, days;

  printf("年を入力>");
  scanf("%d", &year);

  printf("月を入力>");
  scanf("%d", &month);

  if (month == 1 || month == 3 || month == 5 || month == 7 ||
      month == 8 || month == 10 || month == 12) {
    days = 31;
  }
  if (month == 4 || month == 6 || month == 9 || month == 11) {
    days = 30;
  }
  if (month == 2) {
    if (year % 400 == 0) {
      days = 29;
    } else if (year % 100 == 0) {
      days = 28;
    } else if (year % 4 == 0) {
      days = 29;
    } else {
      days = 28;
    }
  }

  printf("%d年%d月の日数は%d日です\n", year, month, days);

  return 0;
}
