
from setuptools import setup


# Dynamically calculate the version based on pyautogui.VERSION.
version = __import__('pymsgbox').__version__


setup(
    name='PyMsgBox',
    version=version,
    url='https://github.com/asweigart/PyMsgBox',
    author='Al Sweigart',
    author_email='al@inventwithpython.com',
    description=('A simple, cross-platform, pure Python module for JavaScript-like message boxes.'),
    license='BSD',
    packages=['pymsgbox'],
    test_suite='tests',
    keywords="gui msgbox message box dialog confirmation confirm password alert",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Environment :: MacOS X',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)