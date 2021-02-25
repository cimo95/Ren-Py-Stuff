#define anticheat variables for save files and persistent
define anticheat = None
define persistent.anticheat = None
#define device lock variables for persistent
define persistent.devicelock = None

init python:
    #function to generates anticheat value. this can be anything as long as its random
    def genAntiCheat():
        #for example, i want to generate random string to use as anticheat value
        import string
        return "".join(renpy.random.choices(string.ascii_uppercase + string.digits,k=16))
    
    #function to generates devicelock value, this is depend on what device / platform the game is being supported
    def genDevLock():
        #for example, i want to create a game which support PC and Android, so i do this:
        if renpy.variant('pc'):
            #getting pc uuid
            import uuid
            return uuid.UUID(int=uuid.getnode())
        elif renpy.variant('touch'):
            #getting android device serial number
            import subprocess
            return subprocess.check_output(['getprop','ro.serialno'])
            
label start:
    #this part should be written at the beginning of any initial section like "start:" or "splashscreen:"
    #so anticheat will be created immediately
    if not persistent.anticheat:
        $ persistent.anticheat = genAntiCheat()
        anticheat = persistent.anticheat
    #this part should be written at the beginning of any initial section like "start:" or "splashscreen:"
    #so device lock check will be executed immediately
    if not persistent.devicelock:
        $ persistent.devicelock = getDevLock()
    else:
        $ currentDevice = getDevLock()
        if currentDevice != persistent.devicelock:
            #for example, i want game to exit while the device lock value does not match
            renpy.quit()
        
#this part should be written at the beginning of "after_load:" section, to check if the anticheat value match or not
label after_load:
    if anticheat != persistent.anticheat:
        #for example, i want game to exit while anticheat from persistent does not match with the one in loaded save data
        $ renpy.quit()
