#include <stdio.h>

int main() {
  int week, day, day_week;

  printf("今月の1日の曜日を選択してください\n");
  printf("(0: 日曜日 1: 月曜日 2: 火曜日 3: 水曜日 4: 木曜日 5: 金曜日 6: 土曜日)\n");
  scanf("%d", &week);

  printf("今月の日付を入力してください:");
  scanf("%d", &day);

  day_week = (day + week - 1) % 7;

  switch (day_week) {
  case 0:
    printf("%d日は日曜日です\n", day);
    break;
  case 1:
    printf("%d日は月曜日です\n", day);
    break;
  case 2:
    printf("%d日は火曜日です\n", day);
    break;
  case 3:
    printf("%d日は水曜日です\n", day);
    break;
  case 4:
    printf("%d日は木曜日です\n", day);
    break;
  case 5:
    printf("%d日は金曜日です\n", day);
    break;
  case 6:
    printf("%d日は土曜日です\n", day);
    break;
  }

  return 0;
}
