#include<iostream>
#include "functions.h"


using namespace std;


int main(int argc, char** argv)
{	
	cout<<"############# Hello ########## \n";
	if(argc > 1){
		for(auto i{1}; i<argc; i++){
			cout<<"arg #"<<i<<": "<< argv[i]<<endl;
			cout<<"Factorial: "<< factorial(stoi(argv[i]))<<"\n";
			cout<<"Fibonacci: "<< fibonacci(stoi(argv[i]))<<"\n";
		}
		
	}
	else{
		cout<<"No arguments passed"<<endl;
	}
}
