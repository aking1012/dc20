;; 	 [ The .data section ]		
;; This section is for defining constants, such as filenames or buffer sizes,
;; It includes the initialized variables
;;
;;	var1	db	31
;;	var2	dw	-1
	
section .data


;; [ The .bss section ]
;; This section is where you declare your uninitialized variables.
;; They look something like this:
;; 
;; 	filename:	resb	255 	; REServe 255 Bytes
;; 	number:		resb	1	; REServe 1 Byte
section .bss

;; [ The .text section ]
;;
;; This is where the actual assembly code is written. 
section .text
    global _start                       ;must be declared for linker (ld)
;; just like main in C -- if linking with gcc, must be main, otherwise does not have to.

_start:                                 ;tell linker entry point

MOV EAX, ESP ;replaceme

;; this is where we get ready to exit cleanly
	mov eax, 1
	mov ebx, 0
	int 80h
