import unittest
import sys
import os
import time
import threading
import inspect

import pymsgbox

# Note: Yes, PyAutoGUI does have PyMsgBox itself as a dependency, but we won't be using that part of PyAutoGUI for this testing.
import pyautogui # PyAutoGUI simulates key presses on the message boxes.
pyautogui.PAUSE = 0.1


GUI_WAIT = 0.4 # if tests start failing, maybe try bumping this up a bit (though that'll slow the tests down)


"""
NOTE: You will often see this code in this test:

    print('Line', inspect.currentframe().f_lineno);

This is because due to the GUI nature of these tests, if something messes up
and PyAutoGUI is unable to click on the message box, this program will get
held up. By printing out the line number, you will at least be able to see
which line displayed the message box that is held up.

This is a bit unorthodox, and I'm welcome to other suggestions about how to
deal with this possible scenario.
"""

class KeyPresses(threading.Thread):
    def __init__(self, keyPresses):
        super(KeyPresses, self).__init__()
        self.keyPresses = keyPresses

    def run(self):
        time.sleep(GUI_WAIT)
        pyautogui.typewrite(self.keyPresses, interval=0.05)


class AlertTests(unittest.TestCase):
    def test_alert(self):
        for func in (pymsgbox._alertTkinter, pymsgbox.alert):
            if func is pymsgbox._alertTkinter:
                print('Testing tkinter alert()')
            elif func is pymsgbox.alert:
                print('Testing native alert()')
            # no text
            t = KeyPresses(['enter'])
            t.start()
            print('Line', inspect.currentframe().f_lineno)
            self.assertEqual(func(), 'OK')

            # text
            t = KeyPresses(['enter'])
            t.start()
            print('Line', inspect.currentframe().f_lineno)
            self.assertEqual(func('Hello'), 'OK')

            # text and title
            t = KeyPresses(['enter'])
            t.start()
            print('Line', inspect.currentframe().f_lineno)
            self.assertEqual(func('Hello', 'Title'), 'OK')

            # text, title, and custom button
            t = KeyPresses(['enter'])
            t.start()
            print('Line', inspect.currentframe().f_lineno)
            self.assertEqual(func('Hello', 'Title', 'Button'), 'Button')

            # using keyword arguments
            t = KeyPresses(['enter'])
            t.start()
            print('Line', inspect.currentframe().f_lineno)
            self.assertEqual(func(text='Hello', title='Title', button='Button'), 'Button')


class ConfirmTests(unittest.TestCase):
    def test_confirm(self):
        for func in (pymsgbox._confirmTkinter, pymsgbox.confirm):
            if func is pymsgbox._confirmTkinter:
                print('Testing tkinter confirm()')
            elif func is pymsgbox.confirm:
                print('Testing native confirm()')

            # press enter on OK
            t = KeyPresses(['enter'])
            t.start()
            print('Line', inspect.currentframe().f_lineno)
            self.assertEqual(func(), 'OK')

            # press right, enter on Cancel
            t = KeyPresses(['right', 'enter'])
            t.start()
            print('Line', inspect.currentframe().f_lineno)
            self.assertEqual(func(), 'Cancel')

            # press right, left, right, enter on Cancel
            t = KeyPresses(['right', 'left', 'right', 'enter'])
            t.start()
            print('Line', inspect.currentframe().f_lineno)
            self.assertEqual(func(), 'Cancel')

            # press tab, enter on Cancel
            t = KeyPresses(['tab', 'enter'])
            t.start()
            print('Line', inspect.currentframe().f_lineno)
            self.assertEqual(func(), 'Cancel')

            # press tab, tab, enter on OK
            t = KeyPresses(['tab', 'tab', 'enter'])
            t.start()
            print('Line', inspect.currentframe().f_lineno)
            self.assertEqual(func(), 'OK')

            # with text
            t = KeyPresses(['enter'])
            t.start()
            print('Line', inspect.currentframe().f_lineno)
            self.assertEqual(func('Hello'), 'OK')

            # with text, title
            t = KeyPresses(['enter'])
            t.start()
            print('Line', inspect.currentframe().f_lineno)
            self.assertEqual(func('Hello', 'Title'), 'OK')

            # with text, title, and one custom button
            t = KeyPresses(['enter'])
            t.start()
            print('Line', inspect.currentframe().f_lineno)
            self.assertEqual(func('Hello', 'Title', ['A']), 'A')

            # with text, title, and one custom blank button
            t = KeyPresses(['enter'])
            t.start()
            print('Line', inspect.currentframe().f_lineno)
            self.assertEqual(func('Hello', 'Title', ['']), '')

            # with text, title, and two custom buttons
            t = KeyPresses(['enter'])
            t.start()
            print('Line', inspect.currentframe().f_lineno)
            self.assertEqual(func('Hello', 'Title', ['A', 'B']), 'A')

            t = KeyPresses(['right', 'enter'])
            t.start()
            print('Line', inspect.currentframe().f_lineno)
            self.assertEqual(func('Hello', 'Title', ['A', 'B']), 'B')

            t = KeyPresses(['right', 'left', 'enter'])
            t.start()
            print('Line', inspect.currentframe().f_lineno)
            self.assertEqual(func('Hello', 'Title', ['A', 'B']), 'A')

            t = KeyPresses(['tab', 'enter'])
            t.start()
            print('Line', inspect.currentframe().f_lineno)
            self.assertEqual(func('Hello', 'Title', ['A', 'B']), 'B')

            t = KeyPresses(['tab', 'tab', 'enter'])
            t.start()
            print('Line', inspect.currentframe().f_lineno)
            self.assertEqual(func('Hello', 'Title', ['A', 'B']), 'A')

            # with text, title, and three custom buttons
            t = KeyPresses(['tab', 'tab', 'enter'])
            t.start()
            print('Line', inspect.currentframe().f_lineno)
            self.assertEqual(func('Hello', 'Title', ['A', 'B', 'C']), 'C')

            # with text, title, and four custom buttons
            t = KeyPresses(['tab', 'tab', 'tab', 'enter'])
            t.start()
            print('Line', inspect.currentframe().f_lineno)
            self.assertEqual(func('Hello', 'Title', ['A', 'B', 'C', 'D']), 'D')

            # with text, title, and five custom buttons
            t = KeyPresses(['tab', 'tab', 'tab', 'tab', 'enter'])
            t.start()
            print('Line', inspect.currentframe().f_lineno)
            self.assertEqual(func('Hello', 'Title', ['A', 'B', 'C', 'D', 'E']), 'E')

            # with text, title, and three custom buttons specified with keyword arguments
            t = KeyPresses(['tab', 'tab', 'enter'])
            t.start()
            print('Line', inspect.currentframe().f_lineno)
            self.assertEqual(func(text='Hello', title='Title', buttons=['A', 'B', 'C']), 'C')

            # test that pressing Esc is the same as clicking Cancel (but only when there is a cancel button)
            t = KeyPresses(['escape'])
            t.start()
            print('Line', inspect.currentframe().f_lineno)
            self.assertEqual(func(text='Escape button press test'), 'Cancel')

            # Make sure that Esc keypress does nothing if there is no Cancel button.
            t = KeyPresses(['escape', 'enter'])
            t.start()
            print('Line', inspect.currentframe().f_lineno)
            self.assertEqual(func(text='Escape button press test', buttons=['OK', 'Not OK']), 'OK')

class PromptPasswordTests(unittest.TestCase):
    def test_prompt(self):
        self._prompt_and_password_tests(pymsgbox._promptTkinter, 'prompt()')

    def test_password(self):
        # NOTE: Currently there is no way to test the appearance of the * or custom mask characters.
        self._prompt_and_password_tests(pymsgbox._passwordTkinter, 'password()')

    def _prompt_and_password_tests(self, msgBoxFunc, msgBoxFuncName):
        # entering nothing
        t = KeyPresses(['enter'])
        t.start()
        print('Line', inspect.currentframe().f_lineno)
        self.assertEqual((msgBoxFuncName, msgBoxFunc()), (msgBoxFuncName, ''))

        # entering text
        t = KeyPresses(['a', 'b', 'c', 'enter'])
        t.start()
        print('Line', inspect.currentframe().f_lineno)
        self.assertEqual((msgBoxFuncName, msgBoxFunc()), (msgBoxFuncName, 'abc'))

        # entering text, tabbing to the Ok key
        t = KeyPresses(['a', 'b', 'c', 'tab', 'enter'])
        t.start()
        print('Line', inspect.currentframe().f_lineno)
        self.assertEqual((msgBoxFuncName, msgBoxFunc()), (msgBoxFuncName, 'abc'))

        # entering text but hitting cancel
        t = KeyPresses(['a', 'b', 'c', 'tab', 'tab', 'enter'])
        t.start()
        print('Line', inspect.currentframe().f_lineno)
        self.assertEqual((msgBoxFuncName, msgBoxFunc()), (msgBoxFuncName, None))

        # with text
        t = KeyPresses(['a', 'b', 'c', 'enter'])
        t.start()
        print('Line', inspect.currentframe().f_lineno)
        self.assertEqual((msgBoxFuncName, msgBoxFunc('Hello')), (msgBoxFuncName, 'abc'))

        # with text and title
        t = KeyPresses(['a', 'b', 'c', 'enter'])
        t.start()
        print('Line', inspect.currentframe().f_lineno)
        self.assertEqual((msgBoxFuncName, msgBoxFunc('Hello', 'Title')), (msgBoxFuncName, 'abc'))

        # with text, title and default value
        t = KeyPresses(['enter'])
        t.start()
        print('Line', inspect.currentframe().f_lineno)
        self.assertEqual((msgBoxFuncName, msgBoxFunc('Hello', 'Title', 'default')), (msgBoxFuncName, 'default'))

        # with text, title and default value specified by keyword arguments
        t = KeyPresses(['enter'])
        t.start()
        print('Line', inspect.currentframe().f_lineno)
        self.assertEqual((msgBoxFuncName, msgBoxFunc(text='Hello', title='Title', default='default')), (msgBoxFuncName, 'default'))

class TimeoutTests(unittest.TestCase):
    def test_timeout(self):
        # Note: If these test's fail, the unit tests will hang.
        self.assertEqual(pymsgbox._alertTkinter('timeout test', timeout=300), pymsgbox.TIMEOUT_RETURN_VALUE)
        self.assertEqual(pymsgbox._confirmTkinter('timeout test', timeout=300), pymsgbox.TIMEOUT_RETURN_VALUE)
        self.assertEqual(pymsgbox.prompt('timeout test', timeout=300), pymsgbox.TIMEOUT_RETURN_VALUE)
        self.assertEqual(pymsgbox.password('timeout test', timeout=300), pymsgbox.TIMEOUT_RETURN_VALUE)


""""
# NOTE: This is weird. This test fails (the additional typed in text gets added
# to the end of the default string, instead of replacing it), but when I run
# this same code using PyAutoGUI from the interactive shell (on Win7 Py3.3) it
# works. It also works when I type it in myself.
# Commenting this out for now.

class DefaultValueOverwriteTests(unittest.TestCase):
    def test_prompt(self):
        self._prompt_and_password_tests(pymsgbox.prompt, 'prompt()')

    def test_password(self):
        # NOTE: Currently there is no way to test the appearance of the * or custom mask characters.
        self._prompt_and_password_tests(pymsgbox.password, 'password()')

    def _prompt_and_password_tests(self, msgBoxFunc, msgBoxFuncName):
        # with text, title and default value that is typed over
        t = KeyPresses(['a', 'b', 'c', 'enter'])
        t.start()
        print('Line', inspect.currentframe().f_lineno); self.assertEqual((msgBoxFuncName, msgBoxFunc('Hello', 'Title', 'default')), (msgBoxFuncName, 'abc'))
"""


class WindowsNativeAlertTests(unittest.TestCase):
    def test_alert(self):
        if sys.platform != 'win32':
            return

        # TODO - We need some way of determining if the tkinter or native message box appeared.

        # test passing True for _tkinter
        t = KeyPresses(['enter'])
        t.start()
        print('Line', inspect.currentframe().f_lineno)
        self.assertEqual(pymsgbox.alert(_tkinter=True), pymsgbox.OK_TEXT)

        # test passing timeout
        t = KeyPresses(['enter'])
        t.start()
        print('Line', inspect.currentframe().f_lineno)
        self.assertEqual(pymsgbox.alert(timeout=300), pymsgbox.OK_TEXT)

        # test non-ok button to check that it falls back to tkinter
        t = KeyPresses(['enter'])
        t.start()
        print('Line', inspect.currentframe().f_lineno)
        self.assertEqual(pymsgbox.alert(button='Test'), 'Test')


class WindowsNativeConfirmTests(unittest.TestCase):
    def test_confirm(self):
        if sys.platform != 'win32':
            return

        # TODO - We need some way of determining if the tkinter or native message box appeared.

        # press enter on OK
        #t = KeyPresses(['enter'])
        #t.start()
        #print('Line', inspect.currentframe().f_lineno)
        #self.assertEqual(pymsgbox.confirm(), pymsgbox.OK_TEXT)


if __name__ == '__main__':
    unittest.main()
