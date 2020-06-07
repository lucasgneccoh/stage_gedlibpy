#include "functions.h"
int factorial(int n){
    if(n>1){return (factorial(n-1)*n);}
    else{return(1);}
}

int fibonacci(int n){
    if(n==1 || n==2){return(1);}
    else{return(fibonacci(n-1) + fibonacci(n-2));}
}
