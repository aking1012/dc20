/**
DISCLAIMER: I am NOT a C programmer...no warranty of any kind is stated or implied.
This code could have disastorous effects and I will NOT be held liable.  Use at
your own risk and for educational purposes only.

I compiled with i586-mingw32-gcc with the expected results
Check the readme for commands I used

Copyright 2011
Andrew King
aking1012.com@gmail.com
**/

#include <windows.h>
#include <stdio.h>	

int main () {
	
	/*Typedef the hello function*/
	typedef void (*pfunc)();
	
	/*Windows handle*/
	HANDLE hdll;
	
	/*A pointer to a function*/
	pfunc hello;
	
	/*LoadLibrary*/
	hdll = LoadLibrary("test.dll");
	
	/*GetProcAddress*/
	hello = (pfunc)GetProcAddress(hdll, "hello");
	
	/*Call the function*/
	unsigned char canwe [] = "Yes we can!";
	hello(canwe);
	printf("Infinite loop to check things in a debugger if you like...");
	while (1){
		//Nothing going on here...
	}
	return 0;
}
