#include <stdio.h>

int main() {

  int days[12]={31,28,31,30,31,30,31,31,30,31,30,31};
  char weekname[7][10]={
	"sunday","monday","tuesday", "wednesday", "thursday","friday", "saturday"};
  int day, month;
  int i, sum_days = 0;

  printf("月を入力してください\n");
  scanf("%d", &month);

  printf("日を入力してください\n");
  scanf("%d", &day);

  for (i = 0; i < month-1; i ++) {
    sum_days += days[i];
  }
  sum_days += day;

  printf("2018年での%d月%d日は%d日目で, 曜日は%sです.\n",
         month, day, sum_days, weekname[sum_days%7]);

  return 0;
}
