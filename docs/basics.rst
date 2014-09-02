.. default-role:: code
===============
PyMsgBox Basics
===============


Installation
============

PyMsgBox can be installed from PyPI with pip:

    `pip install PyMsgBox`

OS X and Linux may require sudo to install the module:

    `sudo pip install PyMsgBox`

PyMsgBox uses Python's built-in TKinter module for its GUI. It is cross-platform and runs on Python 2 and Python 3.

PyMsgBox's code is derived from Stephen Raymond Ferg's EasyGui. http://easygui.sourceforge.net/

Usage
=====

There are four functions in PyMsgBox, which follow JavaScript's message box naming conventions:

 - `alert(text='', title='', button='OK')`

    Displays a simple message box with text and a single OK button. Returns the text of the button clicked on.

 - `confirm(text='', title='', buttons=['OK', 'Cancel'])`

    Displays a message box with OK and Cancel buttons. Number and text of buttons can be customized. Returns the text of the button clicked on.

 - `prompt(text='', title='' , defaultValue='')`

    Displays a message box with text input, and OK & Cancel buttons. Returns the text entered, or None if Cancel was clicked.

 - `password(text='', title='', defaultValue='', mask='*')`

    Displays a message box with text input, and OK & Cancel buttons. Typed characters appear as *. Returns the text entered, or None if Cancel was clicked.

