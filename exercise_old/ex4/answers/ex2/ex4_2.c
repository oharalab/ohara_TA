#include <stdio.h>
#include <math.h>

int main() {
    double x, y;

    printf("ｘのｙ乗を計算します\n");
    printf("ｘとｙの値を半角空白で区切って入力＞");
    scanf("%lf %lf", &x, &y);

    printf("%.3fの%.3f乗は%.3fです\n", x, y, pow(x, y));

    return (0);
}