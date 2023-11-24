### Install and run win32 service, using python
To install the service type the following command on the cmd (as administrator):
_$ python ".pyfilepath" install_
The above command install the server, that can be managed directly in service manager of windows.

If some errors occured look at _administration service_ in the control panel of windows (_event viewer_)

#### Setup python environment
Launch the command to install pywin32 lib for python: _$ pip3 install pywin32_

In the directory PythonXX\Lib\site-packages\win32 must be the following file:
* pythonXX.dll -> this file are stored at the path: _C:\AppData\Local\Programs\Python\Python310-32_
* pywintypesXX.dll

