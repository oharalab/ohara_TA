#define _CRT_SECURE_NO_WARNINGS   // Visual Studio で scanf() 関数を使う場合にのみ必要な設定
#include <stdio.h>

int main(){
  int x, y;

  printf("整数値を入力してください：");
  scanf("%d", &x);    // キーボードから入力された整数値を変数 x に保存（来週説明）
  /* 変数 x の内容を実行例のように出力する printf() を記述 */
  printf("x = %d\n", x);

  printf("整数値を入力してください：");
  scanf("%d", &y);    // キーボードから入力された整数値を変数 y に保存（来週説明）
  /* 変数 y の内容を実行例のように出力する printf() を記述 */
  printf("y = %d\n", y);

  /* 変数 x と y の和を画面に表示する printf() を記述 */
  printf("x + y = %d\n", x + y);
  /* 変数 x と y の差を画面に表示する printf() を記述 */
  printf("x - y = %d\n", x - y);

  return (0);

}
