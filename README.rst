PyMsgBox
========

 A simple, cross-platform, pure Python module for JavaScript-like message boxes.

To import, run:

    >>> from pymsgbox import *`

There are four functions in PyMsgBox, which follow JavaScript's message box naming conventions:

    >>> alert(text='', title='', button='OK')`

    Displays a simple message box with text and a single OK button. Returns the text of the button clicked on.

    >>> confirm(text='', title='', buttons=['OK', 'Cancel'])`

    Displays a message box with OK and Cancel buttons. Number and text of buttons can be customized. Returns the text of the button clicked on.

    >>> prompt(text='', title='' , defaultValue='')`

    Displays a message box with text input, and OK & Cancel buttons. Returns the text entered, or None if Cancel was clicked.

    >>> password(text='', title='', defaultValue='', mask='*')`

    Displays a message box with text input, and OK & Cancel buttons. Typed characters appear as \*. Returns the text entered, or None if Cancel was clicked.

You can also use your platform's native system calls for displaying a message box with the OS's look-and-feel. (Currently this is only supported by alert() and confirm() on Windows.)

    >>> import pymsgbox.native as pymsgbox

Modified BSD License

Derived from Stephen Raymond Ferg's EasyGui http://easygui.sourceforge.net/


