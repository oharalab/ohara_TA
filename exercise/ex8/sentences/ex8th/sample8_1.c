/*
 * sample8_1.c
 */
#include<stdio.h>

void print_msg(char n[]);

int main(){
	int n;
	
	print_msg("整数値を入力してください：");
	scanf("%d", &n);
	printf("入力値：%d\n", n);
	
	return 0;
}

void print_msg(char n[]){
	printf("%s", n);
}
