# PyMsgBox - A simple, cross-platform, pure Python module for displaying message boxes, and just message boxes.
# Al Sweigart al@inventwithpython.com

# Modified BSD License
# Derived from Stephen Raymond Ferg's EasyGui http://easygui.sourceforge.net/

import platform
import os
import sys

RUNNING_PYTHON_2 = sys.version.startswith('2.')

if RUNNING_PYTHON_2:
    from Tkinter import *
else:
    from tkinter import *

rootWindowPosition = "+300+200"


if TkVersion < 8.0 :
    print('You are running Tk version: ' + str(TkVersion) + 'You must be using Tk version 8.0 or greater to use PyMsgBox.')
    sys.exit()


PROPORTIONAL_FONT_FAMILY = ("MS", "Sans", "Serif")
MONOSPACE_FONT_FAMILY    = ("Courier")

PROPORTIONAL_FONT_SIZE  = 10
MONOSPACE_FONT_SIZE     =  9  #a little smaller, because it it more legible at a smaller size
TEXT_ENTRY_FONT_SIZE    = 12  # a little larger makes it easier to see

#STANDARD_SELECTION_EVENTS = ["Return", "Button-1"]
STANDARD_SELECTION_EVENTS = ["Return", "Button-1", "space"]


# Initialize some global variables that will be reset later
__choiceboxMultipleSelect = None
__widgetTexts = None
__replyButtonText = None
__choiceboxResults = None
__firstWidget = None
__enterboxText = None
__enterboxDefaultText=""
__multenterboxText = ""
choiceboxChoices = None
choiceboxWidget = None
entryWidget = None
boxRoot = None
ImageErrorMsg = (
    "\n\n---------------------------------------------\n"
    "Error: %s\n%s")




def msgbox(msg="(Your message goes here)", title=" ", ok_button="OK",image=None,root=None):
    """
    Display a messagebox
    """
    assert type(ok_button) == str, "The 'ok_button' argument to msgbox must be a string."

    return buttonbox(msg=msg, title=title, choices=[ok_button], image=image,root=root)

def denyWindowManagerClose():
    """ don't allow WindowManager close
    """
    x = Tk()
    x.withdraw()
    x.bell()
    x.destroy()

def buttonbox(msg="",title=" "
    ,choices=("Ok", "Cancel")
    , image=None
    , root=None
    ):
    """
    Display a msg, a title, and a set of buttons.
    The buttons are defined by the members of the choices list.
    Return the text of the button that the user selected.

    @arg msg: the msg to be displayed.
    @arg title: the window title
    @arg choices: a list or tuple of the choices to be displayed
    """
    global boxRoot, __replyButtonText, __widgetTexts, buttonsFrame


    # Initialize __replyButtonText to the first choice.
    # This is what will be used if the window is closed by the close button.
    __replyButtonText = choices[0]

    if root:
        root.withdraw()
        boxRoot = Toplevel(master=root)
        boxRoot.withdraw()
    else:
        boxRoot = Tk()
        boxRoot.withdraw()

    boxRoot.protocol('WM_DELETE_WINDOW', denyWindowManagerClose )
    boxRoot.title(title)
    boxRoot.iconname('Dialog')
    boxRoot.geometry(rootWindowPosition)
    boxRoot.minsize(400, 100)

    # ------------- define the messageFrame ---------------------------------
    messageFrame = Frame(master=boxRoot)
    messageFrame.pack(side=TOP, fill=BOTH)

    # ------------- define the imageFrame ---------------------------------
    tk_Image = None
    if image:
        imageFilename = os.path.normpath(image)
        junk,ext = os.path.splitext(imageFilename)

        if os.path.exists(imageFilename):
            if ext.lower() in [".gif", ".pgm", ".ppm"]:
                tk_Image = PhotoImage(master=boxRoot, file=imageFilename)
            else:
                if PILisLoaded:
                    try:
                        pil_Image = PILImage.open(imageFilename)
                        tk_Image = PILImageTk.PhotoImage(pil_Image, master=boxRoot)
                    except:
                        msg += ImageErrorMsg % (imageFilename,
                            "\nThe Python Imaging Library (PIL) could not convert this file to a displayable image."
                            "\n\nPIL reports:\n" + exception_format())

                else:  # PIL is not loaded
                    msg += ImageErrorMsg % (imageFilename,
                    "\nI could not import the Python Imaging Library (PIL) to display the image.\n\n"
                    "You may need to install PIL\n"
                    "(http://www.pythonware.com/products/pil/)\n"
                    "to display " + ext + " image files.")

        else:
            msg += ImageErrorMsg % (imageFilename, "\nImage file not found.")

    if tk_Image:
        imageFrame = Frame(master=boxRoot)
        imageFrame.pack(side=TOP, fill=BOTH)
        label = Label(imageFrame,image=tk_Image)
        label.image = tk_Image # keep a reference!
        label.pack(side=TOP, expand=YES, fill=X, padx='1m', pady='1m')

    # ------------- define the buttonsFrame ---------------------------------
    buttonsFrame = Frame(master=boxRoot)
    buttonsFrame.pack(side=TOP, fill=BOTH)

    # -------------------- place the widgets in the frames -----------------------
    messageWidget = Message(messageFrame, text=msg, width=400)
    messageWidget.configure(font=(PROPORTIONAL_FONT_FAMILY,PROPORTIONAL_FONT_SIZE))
    messageWidget.pack(side=TOP, expand=YES, fill=X, padx='3m', pady='3m')

    __put_buttons_in_buttonframe(choices)

    # -------------- the action begins -----------
    # put the focus on the first button
    __firstWidget.focus_force()

    boxRoot.deiconify()
    boxRoot.mainloop()
    boxRoot.destroy()
    if root: root.deiconify()
    return __replyButtonText


def __put_buttons_in_buttonframe(choices):
    """Put the buttons in the buttons frame
    """
    global __widgetTexts, __firstWidget, buttonsFrame

    __firstWidget = None
    __widgetTexts = {}

    i = 0

    for buttonText in choices:
        tempButton = Button(buttonsFrame, takefocus=1, text=buttonText)
        bindArrows(tempButton)
        tempButton.pack(expand=YES, side=LEFT, padx='1m', pady='1m', ipadx='2m', ipady='1m')

        # remember the text associated with this widget
        __widgetTexts[tempButton] = buttonText

        # remember the first widget, so we can put the focus there
        if i == 0:
            __firstWidget = tempButton
            i = 1

        # for the commandButton, bind activation events to the activation event handler
        commandButton  = tempButton
        handler = __buttonEvent
        for selectionEvent in STANDARD_SELECTION_EVENTS:
            commandButton.bind("<%s>" % selectionEvent, handler)


def bindArrows(widget):
    widget.bind("<Down>", tabRight)
    widget.bind("<Up>"  , tabLeft)

    widget.bind("<Right>",tabRight)
    widget.bind("<Left>" , tabLeft)

def tabRight(event):
    boxRoot.event_generate("<Tab>")

def tabLeft(event):
    boxRoot.event_generate("<Shift-Tab>")


def __buttonEvent(event):
    """
    Handle an event that is generated by a person clicking a button.
    """
    global  boxRoot, __widgetTexts, __replyButtonText
    __replyButtonText = __widgetTexts[event.widget]
    boxRoot.quit() # quit the main loop


def enterbox(msg="Enter information", title="" , default="", strip=True, image=None, root=None):
    """
    Show a box in which a user can enter some text.

    You may optionally specify some default text, which will appear in the
    enterbox when it is displayed.

    Returns the text that the user entered, or None if he cancels the operation.

    By default, enterbox strips its result (i.e. removes leading and trailing
    whitespace).  (If you want it not to strip, use keyword argument: strip=False.)
    This makes it easier to test the results of the call::

        reply = enterbox(....)
        if reply:
            ...
        else:
            ...
    """
    result = __fillablebox(msg, title, default=default, mask=None,image=image,root=root)
    if result and strip:
        result = result.strip()
    return result


def passwordbox(msg="Enter information"
    , title=" "
    , default=""
    , image=None
    , root=None
    ):
    """
    Show a box in which a user can enter a password.
    The text is masked with asterisks, so the password is not displayed.
    Returns the text that the user entered, or None if he cancels the operation.
    """
    return __fillablebox(msg, title, default, mask="*",image=image,root=root)


def __fillablebox(msg
    , title=""
    , default=""
    , mask=None
    , image=None
    , root=None
    ):
    """
    Show a box in which a user can enter some text.
    You may optionally specify some default text, which will appear in the
    enterbox when it is displayed.
    Returns the text that the user entered, or None if he cancels the operation.
    """

    global boxRoot, __enterboxText, __enterboxDefaultText
    global cancelButton, entryWidget, okButton

    if title == None: title == ""
    if default == None: default = ""
    __enterboxDefaultText = default
    __enterboxText        = __enterboxDefaultText

    if root:
        root.withdraw()
        boxRoot = Toplevel(master=root)
        boxRoot.withdraw()
    else:
        boxRoot = Tk()
        boxRoot.withdraw()

    boxRoot.protocol('WM_DELETE_WINDOW', denyWindowManagerClose )
    boxRoot.title(title)
    boxRoot.iconname('Dialog')
    boxRoot.geometry(rootWindowPosition)
    boxRoot.bind("<Escape>", __enterboxCancel)

    # ------------- define the messageFrame ---------------------------------
    messageFrame = Frame(master=boxRoot)
    messageFrame.pack(side=TOP, fill=BOTH)

    # ------------- define the imageFrame ---------------------------------
    tk_Image = None
    if image:
        imageFilename = os.path.normpath(image)
        junk,ext = os.path.splitext(imageFilename)

        if os.path.exists(imageFilename):
            if ext.lower() in [".gif", ".pgm", ".ppm"]:
                tk_Image = PhotoImage(master=boxRoot, file=imageFilename)
            else:
                if PILisLoaded:
                    try:
                        pil_Image = PILImage.open(imageFilename)
                        tk_Image = PILImageTk.PhotoImage(pil_Image, master=boxRoot)
                    except:
                        msg += ImageErrorMsg % (imageFilename,
                            "\nThe Python Imaging Library (PIL) could not convert this file to a displayable image."
                            "\n\nPIL reports:\n" + exception_format())

                else:  # PIL is not loaded
                    msg += ImageErrorMsg % (imageFilename,
                    "\nI could not import the Python Imaging Library (PIL) to display the image.\n\n"
                    "You may need to install PIL\n"
                    "(http://www.pythonware.com/products/pil/)\n"
                    "to display " + ext + " image files.")

        else:
            msg += ImageErrorMsg % (imageFilename, "\nImage file not found.")

    if tk_Image:
        imageFrame = Frame(master=boxRoot)
        imageFrame.pack(side=TOP, fill=BOTH)
        label = Label(imageFrame,image=tk_Image)
        label.image = tk_Image # keep a reference!
        label.pack(side=TOP, expand=YES, fill=X, padx='1m', pady='1m')

    # ------------- define the buttonsFrame ---------------------------------
    buttonsFrame = Frame(master=boxRoot)
    buttonsFrame.pack(side=TOP, fill=BOTH)


    # ------------- define the entryFrame ---------------------------------
    entryFrame = Frame(master=boxRoot)
    entryFrame.pack(side=TOP, fill=BOTH)

    # ------------- define the buttonsFrame ---------------------------------
    buttonsFrame = Frame(master=boxRoot)
    buttonsFrame.pack(side=TOP, fill=BOTH)

    #-------------------- the msg widget ----------------------------
    messageWidget = Message(messageFrame, width="4.5i", text=msg)
    messageWidget.configure(font=(PROPORTIONAL_FONT_FAMILY,PROPORTIONAL_FONT_SIZE))
    messageWidget.pack(side=RIGHT, expand=1, fill=BOTH, padx='3m', pady='3m')

    # --------- entryWidget ----------------------------------------------
    entryWidget = Entry(entryFrame, width=40)
    bindArrows(entryWidget)
    entryWidget.configure(font=(PROPORTIONAL_FONT_FAMILY,TEXT_ENTRY_FONT_SIZE))
    if mask:
        entryWidget.configure(show=mask)
    entryWidget.pack(side=LEFT, padx="3m")
    entryWidget.bind("<Return>", __enterboxGetText)
    entryWidget.bind("<Escape>", __enterboxCancel)
    # put text into the entryWidget
    entryWidget.insert(0,__enterboxDefaultText)

    # ------------------ ok button -------------------------------
    okButton = Button(buttonsFrame, takefocus=1, text="OK")
    bindArrows(okButton)
    okButton.pack(expand=1, side=LEFT, padx='3m', pady='3m', ipadx='2m', ipady='1m')

    # for the commandButton, bind activation events to the activation event handler
    commandButton  = okButton
    handler = __enterboxGetText
    for selectionEvent in STANDARD_SELECTION_EVENTS:
        commandButton.bind("<%s>" % selectionEvent, handler)


    # ------------------ cancel button -------------------------------
    cancelButton = Button(buttonsFrame, takefocus=1, text="Cancel")
    bindArrows(cancelButton)
    cancelButton.pack(expand=1, side=RIGHT, padx='3m', pady='3m', ipadx='2m', ipady='1m')

    # for the commandButton, bind activation events to the activation event handler
    commandButton  = cancelButton
    handler = __enterboxCancel
    for selectionEvent in STANDARD_SELECTION_EVENTS:
        commandButton.bind("<%s>" % selectionEvent, handler)

    # ------------------- time for action! -----------------
    entryWidget.focus_force()    # put the focus on the entryWidget
    boxRoot.deiconify()
    boxRoot.mainloop()  # run it!

    # -------- after the run has completed ----------------------------------
    if root: root.deiconify()
    boxRoot.destroy()  # button_click didn't destroy boxRoot, so we do it now
    return __enterboxText


def __enterboxGetText(event):
    global __enterboxText

    __enterboxText = entryWidget.get()
    boxRoot.quit()


def __enterboxRestore(event):
    global entryWidget

    entryWidget.delete(0,len(entryWidget.get()))
    entryWidget.insert(0, __enterboxDefaultText)


def __enterboxCancel(event):
    global __enterboxText

    __enterboxText = None
    boxRoot.quit()
