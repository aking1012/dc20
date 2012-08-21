#Use mingw32-gcc
CC=i586-mingw32msvc-gcc
#set CFLAGS and DLLNAME
CFLAGS=-c
DLLNAME=test

all: loader.exe

loader.exe: test.dll loader.o
	$(CC) -o loader.exe -mwindows loader.o $(DLLNAME).dll
	$(CC) -o loadera.exe -mwindows loadera.o $(DLLNAME)a.dll

test.dll: test.o
	$(CC) -shared -o $(DLLNAME).dll test.o -Wl,--out-implib,libtest.a
	$(CC) -shared -o $(DLLNAME)a.dll testa.o -Wl,--out-implib,libtesta.a

test.o:
	$(CC) $(CFLAGS) -DBUILD_DLL -DWIN32 test.c
	$(CC) $(CFLAGS) -DBUILD_DLL -DWIN32 testa.c

loader.o:
	$(CC) $(CFLAGS) loader.c
	$(CC) $(CFLAGS) loadera.c

clean:
	rm -rf *o *.exe *.dll *a

debug: dloader.exe
	$(CC) $(CFLAGS) -DBUILD_DLL -DWIN32 -DDEBUG test.c
	$(CC) $(CFLAGS) -DBUILD_DLL -DWIN32 -DDEBUG testa.c
	
dloader.exe: dtest.dll dloader.o
	$(CC) -o loader.exe loader.o $(DLLNAME).dll
	$(CC) -o loadera.exe loadera.o $(DLLNAME)a.dll

dtest.dll: dtest.o
	$(CC) -shared -o $(DLLNAME).dll test.o -Wl,--out-implib,libtest.a
	$(CC) -shared -o $(DLLNAME)a.dll testa.o -Wl,--out-implib,libtesta.a

dtest.o:
	$(CC) $(CFLAGS) -DBUILD_DLL -DWIN32 -DDEBUG test.c
	$(CC) $(CFLAGS) -DBUILD_DLL -DWIN32 -DDEBUG testa.c

dloader.o:
	$(CC) $(CFLAGS) loader.c
	$(CC) $(CFLAGS) loadera.c

