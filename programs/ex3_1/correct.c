#include <stdio.h>

int main(){
	int a, b, c;

	/* 変数 a への数値の代入 */
        a = 4;
	/* 変数 b への数値の代入 */
        b = 3;
	printf("a = %d\n", a);
	printf("b = %d\n", b);

	/* 変数 a と b の和を計算し，a に代入 */
        a += b;
	printf("a = %d\n", a);

	/* 変数 a と b の値を入れ替える代入文 1 */
        c = a;
	/* 変数 a と b の値を入れ替える代入文 2 */
        a = b;
	/* 変数 a と b の値を入れ替える代入文 3 */
        b = c;
	printf("a = %d, b = %d\n", a, b);

	/* 変数 b の値を画面に出力する printf() （ただし，単項演算子も利用） */
        printf("b = %d\n", b++);
	printf("b = %d\n", b);
	/* 変数 a の値を画面に出力する printf() （ただし，単項演算子も利用） */
	printf("a = %d\n", --a);
	printf("a = %d\n", a);

	return (0);
}
