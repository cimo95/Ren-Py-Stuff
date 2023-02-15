init -999 python:
    import os, time
    config.label_overrides["splashscreen"]="cimosoft_splashscreen"
    config.label_overrides["start"]="cimosoft_splashscreen"
    config.mouse = None
    achievement.steam_position = "bottom right"

    def doreset():
        for savegame in renpy.list_saved_games(fast=True):
            renpy.unlink_save(savegame)
        persistent._clear(True)
        Show("cimosoft_prompt",message="The reset has been completed.\nPlease delete or move the resetter file ({b}renpy reset.rpyc{/b}) outside this \"game\" folder, to start a new game.",ok_action=Quit(False),okonly=True)()
        return None 

    def dobackup():
        savedir = config.savedir.replace("\\","/")+"/"
        backupdir = config.basedir.replace("\\","/")+"/backup"
        try:
            os.makedirs(backupdir)
        except:
            backupdir += str(renpy.random.randint(10000,99999))
            os.makedirs(backupdir)

        backupdir += "/"
        for savegame in renpy.list_saved_games(fast=True):
            try:
                open(backupdir+savegame+"-LT1.save","wb").write(renpy.file(savedir+savegame+"-LT1.save").read())             
            except:
                pass
        try:
            open(backupdir+"persistent","wb").write(renpy.file(savedir+"persistent").read()) 
        except:
            pass

        Show("cimosoft_prompt",message="The backup has been completed.\nYour save data and configuration for \""+config.name+"\" has backed up to \""+backupdir+"\"",okonly=True)()
        return None

screen cimosoft_prompt(message, yes_action=NullAction(), no_action=NullAction(), ok_action=Hide("cimosoft_prompt"), okonly=False):

    modal True

    window:
        style "gm_root"

    frame:
        style_group "yesno"

        xfill True
        xmargin .05
        ypos .1
        yanchor 0
        ypadding .05

        has vbox:
            xalign .5
            yalign .5
            spacing 30

        label _(message):
            xalign 0.5

        hbox:
            xalign 0.5
            spacing 100
            if okonly:
                textbutton _("OK") action ok_action
            else:
                textbutton _("Yes") action yes_action
                textbutton _("No") action no_action

    key "game_menu" action no_action

init -2:
    style yesno_button:
        size_group "yesno"

    style yesno_label_text:
        text_align 0.5
        layout "subtitle"

screen cimosoft_pop:
    modal False
    # zorder 1090
    $ tooltip = GetTooltip()

    frame:
        style_group ""

        has side "t c b":
            spacing gui._scale(10)

        side "c r":
            xfill True
            label _("A game reset has initiated.")
            text "{size=-3}[config.version!q]\n[renpy.version_only!q]\n[renpy.platform!q]{/size}" text_align 1.0 yalign 0.5

        viewport :
            id "viewport"
            child_size (4000, None)
            mousewheel True
            draggable True
            scrollbars "vertical"
            has vbox

            text "Sometimes, you want to play a visual novel story or a game again, and you may not know how to go about it.\nTherefore, this patch was created.\n\nJust put this {b}renpy reset.rpyc{/b} in the \"game\" folder inside your game folder, and run the game.\nThen this message will appear, interrupting the splash screen that should have appeared the first time.\n\nHere besides providing the RESET function, there is also a BACKUP function which allows you to back up all game\nsave data including configurations, before doing RESET.\n\nYou must move this {b}renpy reset.rpyc{/b} file out of the \"game\" folder before you can play the game again.\n\n\nCurrent game :\n{size=+2}{b}"+config.name+"{/b}{/size}\n\nTotal of save data (including quick and auto) :\n{size=+2}{b}"+str(len(renpy.list_saved_games(fast=True)))+" item(s){/size}{/b}" substitute False

        vbox:
            hbox:
                spacing gui._scale(25)

                textbutton _("Reset"):
                    action Show("cimosoft_prompt",message="Are you sure to delete all save data and reset the configuration of \""+config.name+"\"?\nThis action cannot be {b}undone{/b}.",yes_action=Function(doreset),no_action=Hide("cimosoft_prompt"))
                    tooltip "Perform the reset action. Any deleted data related to this action WILL NOT be restorable."

                textbutton _("Backup"):
                    action Function(dobackup)
                    tooltip "Backup all current game save state and configuration to \""+config.basedir+"\"."


                vbox:
                    xfill True

                    textbutton _("Quit"):
                        xalign 1.0
                        action Quit(False)
                        tooltip "Quits the game."

            # Tooltip.
            if tooltip:
                text "[tooltip]"
            else:
                text "{i}RENPY_RESET, a simple RenPy game resetter made by Cimo95 (github.com/cimo95){/i}"


label cimosoft_splashscreen:
    show screen cimosoft_pop
    pause
    jump cimosoft_splashscreen
