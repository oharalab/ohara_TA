/*
 * ex7_2.c
 */
#include<stdio.h>
#include<string.h>

typedef struct {
	char name[30];
	int age;
	int grade;
	double gpa;
} personal_data;

void print_data(personal_data d);
void clear1(personal_data d);
void clear2(personal_data d[]);

int main() {
	personal_data data[5] = {"Aoyama Taro", 20, 2, 3.0};
	
	printf("in main\n");
	print_data(data[0]);

	clear1(data[0]);
	
	printf("in main\n");
	print_data(data[0]);

	clear2(data);
	
	printf("in main\n");
	print_data(data[0]);

	return(0);
}

void clear1(personal_data d){
	d.name[0] = '\0';
	d.age = 0;
	d.grade = 0;
	d.gpa = 0.0;
	
	printf("in clear1\n");
	print_data(d);
}

void clear2(personal_data d[]){
	d[0].name[0] = '\0';
	d[0].age = 0;
	d[0].grade = 0;
	d[0].gpa = 0.0;

	printf("in clear2\n");
	print_data(d[0]);
}

void print_data(personal_data d){
	printf("氏名：%s\n", d.name);
	printf("年齢：%d\n", d.age);
	printf("学年：%d\n", d.grade);
	printf("GPA：%.2f\n", d.gpa);
	printf("\n");
}

