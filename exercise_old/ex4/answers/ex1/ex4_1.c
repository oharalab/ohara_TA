#include <stdio.h>

int main() {
    int x, y;

    printf("2つの整数値を1つの半角空白で区切って入力してください：");
    scanf("%d %d", &x, &y);

    printf("x = %d\n", x);
    printf("y = %d\n", y);
    printf("x + y = %d\n", x + y);
    printf("x - y = %d\n", x - y);

    return 0;
}