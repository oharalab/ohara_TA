#include <stdio.h>

int main() {
  int year, month, days;
  int day_week, total_days = 0;
  int i;

  int month_day[12] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
  
  printf("西暦を入力してください（2000年以降）：");
  scanf("%d", &year);

  printf("月を入力してください：");
  scanf("%d", &month);

  while (month < 1 || month > 12) {
    printf("月は1～12までの整数で入力してください：");
    scanf("%d", &month);
  }

  /* その月の日数を調べる start */
  if (month == 2 &&
      (year % 400 == 0 ||
       (year % 100 != 0 && year % 4 == 0))) {
    days = month_day[month - 1] + 1;
    
  } else {
    days = month_day[month - 1];
  }
  /* その月の日数を調べる end */

  
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
    if (i == 2 &&
        (year % 400 == 0 ||
         (year % 100 != 0 && year % 4 == 0))) {
      total_days += month_day[i - 1] + 1;
    
    } else {
      total_days = month_day[i - 1];
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
