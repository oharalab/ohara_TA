#include <stdio.h>

int main() {
  int ans1, ans2, ans3;
  int total;

  printf("コンビニに行くときは（1:車で 2:自転車で 3:歩いて）行く\n");
  scanf("%d", &ans1);

  printf("1:汗をかいた記憶がない 2:たまに汗をかく 3:よく汗をかく\n");
  scanf("%d", &ans2);

  if (ans2 == 1) {
    total = ans1 + ans2;

  } else {
    printf("汗をかいたのは, ");
    printf("(2:寝汗 3:軽い運動をしたから 4:激しい運動をしたから)\n");
    scanf("%d", &ans3);
    if (ans3 == 2) {
      total = ans1 + ans2;
      
    } else {
      total = ans1 + ans3;
    }
  }

  if (total < 4) {
    printf("運動不足です\n");

  } else {
    printf("よく運動していますね\n");
  }

  return 0;
}
