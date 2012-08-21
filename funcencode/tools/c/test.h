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

#ifndef DLL_H_
#define DLL_H_

#ifdef BUILD_DLL
/* DLL export */
#define EXPORT __declspec(dllexport)
#else
/* EXE import */
#define EXPORT __declspec(dllimport)
#endif

EXPORT void hello(unsigned char canwe []);
EXPORT void endmarker(void);

#endif /* DLL_H_ */
