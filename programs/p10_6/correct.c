/* 
 * p12_6
 */

#include <stdio.h>
#include <ctype.h>

int main(){

  int a;
  printf("学年を入力して下さい >");
  a=getchar();
  if(isdigit(a) == 0){
    printf("数字ではありません\n");
  }else{
    switch(a){
    case '1': printf("あなたは2018年入学ですね\n"); break;
    case '2': printf("あなたは2017年入学ですね\n"); break;
    case '3': printf("あなたは2016年入学ですね\n"); break;
    case '4': printf("あなたは2015年入学ですね\n"); break;
    default: printf("正しい学年ではありません\n");
    }
  }

  return 0;
}
