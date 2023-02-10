#initialize function, usually you put this on "definitions.rpy"
init python:
    #remove any key for "screenshot" 
    config.keymap['screenshot'] = []
    #add new layer named "screenshot_layer" to the topmost, to make sure it can covers all in-game activity 
    config.layers = ['master', 'transient', 'screens', 'overlay', 'screenshot_layer']

    #the modified screenshot function
    def do_screenshot():
        import os.path
        import os
        import __main__
        try:
            #set where the result destination.
            #in this case, the result will be saved on "GameTitle/screenshot"
            destination_path = config.renpy_base.replace('\\','/')+'/screenshot'

            if renpy.macapp:
                destination_path = os.path.expanduser(b"~/Desktop").replace('\\','/')+'/screenshot'

            if not os.path.isdir(destination_path):
                os.makedirs(destination_path)

            #do loop to find that the filename is available
            i = 1
            while True:
                #its not that specific, you can do any simpler than these
                image_serial_number = "{0:0{1}X}".format(i,4)
                screenshot_filepath = os.path.join(destination_path, "screenshot_"+image_serial_number+".png")
                if not os.path.exists(screenshot_filepath):
                    break
                i += 1
                
            #doing raw screenshot using renpy built-in function and save them to screenshot_filepath
            if not renpy.screenshot(screenshot_filepath):
                #if raw screenshot failed for some reason, pops this message :
                renpy.notify("Failead to save screenshot as "+screenshot_filepath)
                return
            else:
                #we'll use pygame to merge screenshot with our watermark (.png)
                pygame.init()
                #creating the canvas
                image_canvas = pygame.Surface((1920,1080))
                #load the raw screenshot
                raw_screenshot_file = pygame.image.load(screenshot_filepath)
                #scale the loaded file to make sure it always fit our canvas dimension
                raw_screenshot_file = pygame.transform.scale(raw_screenshot_file,(1920,1080))
                #load watermark file (for easy use, make sure watermark already in canvas dimension)
                watermark_image = pygame.image.load(renpy.file("images/ssframe.png").read())
                #merge the loaded raw screenshot, with the watermark
                raw_screenshot_file.blit(watermark_image,(0,0))
                #remove old raw screenshot
                os.remove(screenshot_filepath)
                #save the result with the name of raw screenshot
                pygame.image.save(raw_screenshot_file,screenshot_filepath)
                return
        except Exception as error_message:
            #if something unexpected happen, show this message :
            renpy.notify("An Error Occured : "+str(error_message))
            return
            
    # Note :
    # For renpy.screenshot() should be more simplified by using the one which result 
    # to file-like object,this may make the process faster.
    # But im not using it, since i still experimenting with this, and use for my project

# the screen that we'll put on screenshot_layer to handle any screenshot key
# usually you put this on "screens.rpy"
screen screenshot_screen:
    #by default, pressing "s" will trigger screenshot, so we add it here
    key "s" action Function(do_screenshot)
    key "alt_K_s" action Function(do_screenshot)
    #we also capture Print Screen button too, though some of these won't work
    key "alt_K_PRINT" action Function(do_screenshot)
    key "K_PRINT" action Function(do_screenshot)
    key "alt_shift_K_PRINT" action Function(do_screenshot)
    key "meta_K_PRINT" action Function(do_screenshot)
    

# put the screenshot_screen screen, to screenshot_layer layer immediately on game start 
# usually you put this on "script.rpy"
label start:
    $ renpy.show_screen("screenshot_screen", _layer="screenshot_layer")
