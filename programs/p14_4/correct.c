/* 
 * p15_4
 */

#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

void opening(void);
double getdata(void);
double en_menseki(double r);
void dispdata(double dt);

int main() {

  double hankei, menseki;
  opening();
  hankei = getdata();
  menseki = en_menseki(hankei);
  dispdata(menseki);

  return 0;
}

void opening(void){
  printf("円の面積を計算します\n");
}

double getdata(void){

  double wk;
  printf("半径を入力してください： ");
  scanf("%lf", &wk);
  return wk;

}

double en_menseki(double r){
  return r * r * 3.14159;
}

void dispdata(double dt){
  printf("面積 ＝ %f\n", dt);
}
