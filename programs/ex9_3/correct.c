#include <stdio.h>

int main() {
  int year, month, days;
  int day_week, total_days = 0;
  int i;

  printf("西暦を入力してください（2000年以降）：");
  scanf("%d", &year);

  printf("月を入力してください：");
  scanf("%d", &month);

  while (month < 1 || month > 12) {
    printf("月は1～12までの整数で入力してください：");
    scanf("%d", &month);
  }

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

  /* うるう年判定しながら日付けを足していく start */
  for (i = 2000; i < year; i ++) {
    if (i % 400 == 0) {
      total_days += 366;
    } else if (i % 100 == 0) {
      total_days += 365;
    } else if (i % 4 == 0) {
      total_days += 366;
    } else {
      total_days += 365;
    }
  }
  /* うるう年判定しながら日付けを足していく end */

  
  /* その年の入力された年まで足していく start */
  for (i = 1; i < month; i ++) {
    switch(i) {
    case 1: case 3: case 5:
    case 7: case 8: case 10: case 12:
      total_days += 31;
      break;

    case 4: case 6: case 9: case 11:
      total_days += 30;
      break;
      
    case 2:
      if (year % 400 == 0) {
        total_days += 29;
      } else if (year % 100 == 0) {
        total_days += 28;
      } else if (year % 4 == 0) {
        total_days += 29;
      } else {
        total_days += 28;
      }
      break;

    default: break;
    }
  }
  /* その年の入力された年まで足していく end */

  day_week = (total_days + 6) % 7;   /* 曜日を求める */
  
  /* カレンダーの出力 start */
  printf("%d年%d月\n", year, month);
  printf("Sun Mon Tue Wed Thu Fri Sat\n");

  for (i = 0; i < day_week; i ++) {   /* 空白出力 */
    printf("    ");
  }

  for (i = 1; i <= days; i ++) {   /* 日付けの出力 */
    printf("%3d ", i);
    if ((i + day_week) % 7 == 0) {
      printf("\n");
    }
  }
  printf("\n");
  /* カレンダーの出力 end */

  return 0;
}
