::Comandi mancanti
:: il comando per disabilitare il servizio di windows update dovrebbe funzionare

:: Next step
:: eliminare gli installer al riavvio/una volta terminata l'installazione
:: ARCHIVIO AUTO ESTRAENTE (da estrarre sempre in utils)

echo off

echo ---
echo The automatic procedure starts in 15 sec. to cancel it press: CTRL+C

timeout 15

echo ---
echo Disable windows update service
sc config wuauserv start= disabled
reg add HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU /v NoAutoRebootWithLoggedOnUsers /f /t REG_DWORD /d "1"

echo ---
echo Change network adapter name
netsh interface set interface name="Ethernet" newname="Local"
netsh interface set interface name="Ethernet 2" newname="Service"

timeout 5

echo ---
echo Change network ip address for network local
netsh interface ip set address name= "Local" static 192.168.2.10 255.255.255.0

echo ---
echo Change Firewall Rules: Enable Ping
netsh advfirewall firewall add rule name="ICMP Allow incoming V4 echo request" protocol=icmpv4:8,any dir=in action=allow

echo ---
echo Change Firewall Rules: Enable port 502, 5020 for Modbus TCP
netsh advfirewall firewall add rule name="Modbus TCP in port" dir=in action=allow protocol=TCP localport=502,5020

echo ---
echo Enable windows routing
reg  add HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters /v IPEnableRouter /f /t REG_DWORD /d  "1"

echo ---
echo Disable user account check
reg add HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\policies\system /v EnableLUA /f /t REG_DWORD /d "0"

echo ---
echo Disable password on startup
netplwiz

timeout 8

echo ---
echo Install VNC server
IF NOT exist "C:\Program Files\RealVNC" (
	msiexec /i C:\Users\Panel\Desktop\installer\VNC-Server-6.7.1-Windows-en-64bit.msi /quiet /qn /norestart
)ELSE (
	echo VNC server already installed, SKIPPED
)

echo ---
echo Licensing VNCserver
"C:\Program Files\RealVNC\VNC Server\vnclicense.exe" -add UQHDK-2BMC3-GGK7Y-GMDWW-ZHBLA

echo ---
echo Install MariaDB
IF NOT exist "C:\Program Files\MariaDB" (
	msiexec /i C:\Users\Panel\Desktop\installer\mariadb-10.1.48-win32.msi
)ELSE (
	echo MariaDB already installed, SKIPPED
)
::versione quiet
::echo MariaDB installation
::msiexec /i C:\Users\Panel\Desktop\installer\mariadb-10.1.48-win32.msi SERVICENAME=MySQL DATADIR=C:\mariadb5.2\data PASSWORD=root /qn

echo Teamviewer Host silent install
"C:\Users\Panel\Desktop\installer\TeamViewer_Host_Setup.exe" /S

echo Waiting for Teamviewer installation finish
timeout 35

echo Teamviewer VPN driver install
"C:\Program Files (x86)\TeamViewer\tv_x64.exe" --action install --inf "C:\Program Files (x86)\TeamViewer\x64\teamviewervpn.inf" --id TEAMVIEWERVPN

echo Waiting for Teamviewer VPN driver installation finish
timeout 10

echo Python installation
"C:\Users\Panel\Desktop\installer\python-3.10.9-amd64.exe"
::/quiet InstallAllUsers=1 PrependPath=1 Include_test=0 provare se funziona la versione quiet un giorno
::echo Waiting for Python installation finish
::timeout 35

timeout 10
echo Install python required packages
::non funziona, utilizzare .bat per installare i pacchetti
::pip install pyqt5
::pip install pymodbus==2.5.3
::pip install QLed
::pip install mysql.connector
::pip install configparser
::pip install pyinstaller
::pip install pynput

echo VSCode installation
"C:\Users\Panel\Desktop\installer\VSCodeUserSetup-x64-1.78.2.exe"

echo FileZilla installation
"C:\Users\Panel\Desktop\installer\FileZilla_Server-0_9_60_2.exe"
