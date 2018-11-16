#include <stdio.h>

int main(){
	int n;
	double ave, num;

	n = 0;
	printf("%dつ目の数値を入力してください：", ++n);
	scanf("%lf", &num);
	ave = num;

	printf("%dつ目の数値を入力してください：", ++n);
	scanf("%lf", &num);
	ave += num;

	printf("%dつ目の数値を入力してください：", ++n);
	scanf("%lf", &num);
	ave += num;

	printf("%dつ目の数値を入力してください：", ++n);
	scanf("%lf", &num);
	ave += num;

	ave /= n;
	printf("%dつの値の平均値：%.3f\n", n, ave);

	return (0);
}