/* 
 * p12_3
 */

#include <stdio.h>

int main(){

  int ch;
  while((ch = getchar()) != EOF){
    switch(ch){
    case 'a': ch = 'A'; break;
    case 'b': ch = 'B'; break;
    case 'c': ch = 'C'; break;
    case 'd': ch = 'D'; break;
    case 'e': ch = 'E'; break;
    case 'f': ch = 'F'; break;
    case 'g': ch = 'G'; break;
    case 'z': ch = 'Z'; break;
    }
    putchar(ch);
  }
  putchar('\n');

  return(0);
}
