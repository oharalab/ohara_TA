#include <stdio.h>

int main() {
  int year;

  printf("年を入力>");
  scanf("%d", &year);

  if (year % 400 == 0) {
    printf("%d年はうるう年です\n", year);
  } else if (year % 100 == 0) {
    printf("%d年はうるう年ではありません\n", year);
  } else if (year % 4 == 0) {
    printf("%d年はうるう年です\n", year);
  } else {
    printf("%d年はうるう年ではありません\n", year);
  }
  
  return 0;
}
