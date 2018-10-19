#include <stdio.h>

int main(){
	double weight, height, BMI;

	printf("体重（kg）を入力してください：\n");
	scanf("%lf\n", &weight);

	printf("身長（m）を入力してください：\n");
	scanf("%lf\n", &height);

	BMI = weight / (height * height);
	printf("BMI値：%.2f\n", BMI);

	return (0);
}
