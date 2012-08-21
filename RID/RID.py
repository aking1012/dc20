import th32wrapper, vmemfuncwrapper
import pickle

#########################################################
#       Reflective Injection Detector - RID             #
#              by aking1012.com@gmail.com               #
#      Just my opinion of how it should be done         #
#  I was about 3/4 of the way through when I started    #
#        questioning why I didn't just do it in C.      #
#    Also, there is no x64 support.  I'll do it if:     #
#        a)I get around to it                           #
#        b)It becomes a commercial tool                 #
#        c)I get enough donations                       #
#              --no loud complaints do not count        #
#        d)I have to use it on x64                      #
#        e)other - never say never                      #
#    It wouldn't need a whole lot to work on x64...     #
#########################################################

#Automation
def auto():
    snapHandle = th32wrapper.getSnapAll()
    th32wrapper.getProcs(snapHandle)
    th32wrapper.getModLists(snapHandle)
    th32wrapper.bigdict = vmemfuncwrapper.slowCheck(th32wrapper.bigdict)
    return th32wrapper.bigdict
        
if __name__ == "__main__":
    this = auto()
    #do your parsing here...or wait for a UI