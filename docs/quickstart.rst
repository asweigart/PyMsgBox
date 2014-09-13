
.. default-role:: code

==========
Quickstart
==========

On Linux Python 2, you need to first install Tkinter by running: `sudo apt-get install python-tk`

All of the arguments to PyMsgBox functions are optional.

    >>> import pymsgbox
    >>> pymsgbox.alert('This is an alert.')
    >>> pymsgbox.confirm('Click OK to continue, click Cancel to cancel.')
    >>> pymsgbox.prompt('Enter your name.')
    >>> pymsgbox.password('Enter your password. (It will appear hidden in this text field.)')

Here are the default arguments for each function.

    >>> pymsgbox.alert(text='', title='', button='OK')
    >>> pymsgbox.confirm(text='', title='', buttons=['OK', 'Cancel'])
    >>> pymsgbox.prompt(text='', title='' , defaultValue='')
    >>> pymsgbox.password(text='', title='', defaultValue='', mask='*')

To use native operating system message boxes, run the following:

    >>> import pymsgbox.native as pymsgbox

(Only a few of the message boxes have native support. Unsupported message boxes will default to the normal message boxes.)