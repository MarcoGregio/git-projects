# Control Panel
Standard HMI writed in python
## Configurazione Pannello PANEL
### Specifiche dispositivo
**Tipologia dispositivo:** *Industrial PC*

**Processore:** *Intel(R) Celeron(R) CPU J1900 @ 1.99GHz 1.99GHz*

**RAM installata:** *2,00 GB*

**Sistema operativo:** *Windows 10 Enterprise LTSC*

**Tipo di sistema:** *Sistema operativo a 64 bit, processore basato su x64*

### Configurazione di sistema
**Disabilitare inserimento password all'avvio:**
- Aprire il menù di "START".
- Digitare *netplwiz*
- Cliccare sull'icona del programma per aprirlo.
- Nella nuova schermata individuare la casella con scritto "Per utilizzare questo computer è necessario che l’utente immetta il nome e la password" e deselezionare la spunta.
- Cliccare su "Applica".
- Inserire le credenziali del nostro account, se richiesto.
-  Premere il tasto "OK" per uscire.

**Disabilitare firewall di windows:**
- Aprire il pannello di controllo.
- Cliccare su "Windows Defender Firewall".
- Cliccare sulla voce a sinistra "Attiva/Disattiva Windows Defender Firewall".
- Disattivare il firewall su **TUTTI I TIPI DI RETE**.

**Disabilitare windows update:**
- Dalla barra di ricerca, digitare *services.msc*
- Premere *Invio* per aprire la pagina.
- Tra l'elenco dei servizi, cercare "Windows Update".
- Cliccare con il tasto destro sul nome trovato, quindi andare su "Proprietà".
- Nella scheda "Generale" selezionare dal menù a tendina "Tipo di avvio: Disabilitato"
- Spostarsi nella scheda "Ripristino" e selezionare nei tre menù a tendina ("primo tentativo,secondo tentativo,terzo tentativo") l'opzione "Nessuna azione".
- In basso a destra sulla voce "Azzera il conteggio dei tentativi non riusciti dopo:" impostare il valore "9999".
- Cliccare su "Applica" e poi "OK" per rendere le impostazioni attive.
- Riavviare il sistema.

**Disabilitare il controllo dell'account utente**
- Premi la combinazione "Win + R", quindi digita *regedit* e premi "OK".
- Spostarsi nel percorso *HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\policies\system*
- Sul lato destro, individua "EnableLUA DWORD" e fai doppio clic su di esso.
- Cambia il suo valore in "0" e clicca "OK".
- Riavviare il sistema per rendere effettive le modifiche.

### Accesso tramite desktop remoto
- Aprire il menù **START**.
- Cliccare sul simbolo delle **Impostazioni** e andare nella sezione **Account**.
- Nel menù a sinistra selezionare la scheda **Opzioni di accesso**.
- Nell'elenco che si apre, selezionare la voce **Password**.
- Aggiungere una password per l'account utente utilizzato.
- Riavviare il dispositivo.
- Effettuare l'accesso con la password appena impostata.
- Aprire il menù **START**.
- Cliccare sul simbolo delle **Impostazioni** e andare nella sezione **Sistema**.
- Nel menù a sinistra selezionare la scheda **Desktop remoto**.
- Cliccare sulla casella **Abilita Desktop remoto**. Ora sarà possibile collegarsi da remoto tramite l'app.

### Impostare un indirizzo IP statico in una delle due schede di rete
- Dal menù di START cercare *Pannello di Controllo*.
- Andare nella sezione *Centro connessioni di rete e condivisione*.
- Dal menù a sinistra selezionare la scheda *Modifica impostazioni scheda*.
- Fare click con il tasto destro del mouse sulla scheda di rete che si utilizzerà **SENZA DHCP** e andare su *Proprietà*.
- Doppio click sull'opzione *Protocollo Internet versione 4 (TCP/IPv4)*
- Selezionare la spunta *Utilizza il seguente indirizzo IP:* e inserire i dati di rete come seguono:
    - Indirizzo IP: *192.168.2.10*
    - Subnet mask: *255.255.255.0*
    - Gateway predefinito: Lasciare vuoto.
- Cliccare su *OK* per rendere le effettive le modifiche. 

### Installazione dei servizi
Gli eseguibili dei servizi si trovano in *Dropbox (IDT)\Cartella del team IDT\00_IDT\MATERIALE TECNICO\PANEL.IT\installer*

**Installazione VNC-Server**

**ATTENZIONE: SEGUIRE LA PROCEDURA DIRETTAMENTE DAL PANNELLO E NON UTILIZZANDO DESKTOP REMOTO**.
- Spostare l'eseguibile *VNC-Server-6.7.1-Windows-en-64bit* sul desktop.
- Rinominarlo in *vnc-panel*.
- Aprire il menù **START**.
- Digitare *cmd*, successivamente premere la combinazione di tasti *CTRL + MAIUSC* seguito dal tasto *Invio*. Si aprirà il terminale come amministratore.
- Inserire il seguente comando: *msiexec /i C:\Users\Panel\Desktop\vnc-panel.msi /quiet /qn /norestart*
- Attendere il completamento dell'installazione (in genere si vede il simbolo di VNC tra le icone nascoste).
- Inserire il seguente comando: *"C:\Program Files\RealVNC\VNC Server\vnclicense.exe" -add UQHDK-2BMC3-GGK7Y-GMDWW-ZHBLA*
- Sarà quindi possibile utilizzare VNC con la licenza attiva.

**Installazione MariaDB:**
- Eseguire *mariadb-10.1.48-win64.msi*.
- Spuntare l'opzione in basso a sinistra relativa alle politiche di licenza e cliccare su *Next* per proseguire.
- Cliccare sempre *Next* per proseguire senza modificare nulla.
- Nella nuova scheda, in alto a sinistra, inserire una nuova password di root. Di default inseriamo sempre "root".
- Spuntare la casella subito in basso "Enable access from remote machine for 'root' user".
- Spuntare la casella più in basso "Use UTF8 as default server's character set" per utilizzare la codifica standard UTF-8.
- Cliccare su *Next* per proseguire.
- Proseguire con il pulsante *Next* fino alla fine dell'installazione.

**Installazione Python 3.10:**
- Eseguire *python-3.10.5.exe*.
- Spuntare la casella più in basso "Add Python 3.10 to PATH".
- Cliccare su *Install Now* per far partire l'installazione.
- Al termine cliccare su *Close* per terminare.

**Installazione Visual Studio Code**
- Eseguire *VSCodeUserSetup-ia32-1.69.1.exe*.
- Proseguire fino alla fine dell'installazione senza modificare nulla.
- Al termine dell'installazione cliccate su *Fine*. Si aprirà in automatico Visual Studio.
- Cliccare sulla scheda a sinistra *Exstension*.
- Cercare l'estensione *Python* ed installarla con il bottone *Installa*.
- Al termine dell'operazione chiudere Visual Studio.

**Installazione Team Viewer Host**
- L’applicativo teamviewer Host consente solo la connessione da remoto del pc su cui è installato.
- Aprire il setup *TeamViewer_Host_Setup.exe*.
- Spuntare l’opzione *Show advanced settings* e premere *Next*.
- Selezionare *Company/Commercial use* e premere *Next*.
- Spuntare l’opzione *Use TeamViewer VPN* e premere *Next*.
- Attendere la fine dell’installazione ed accettare termini e condizioni. 
- Aprire l’app dall’icona in basso a destra.
- Configurare l’accesso remoto, premere il tasto *Configure*.
- Inserire i seguenti dati:
    -  Computer name: *numero della commessa*. 
    -  Password: *password account teamwiever*. 
    -  Email: *vostro utente teamviewer*.
- Confermate da mail ricevuta affidabilità del dispositivo.
- Effettuare nuovamente il login sul dispositivo per terminare l’associazione.
- Aprite teamviewer dal vostro computer personale dove siete loggati, trascinate il dispositivo appena aggiunto nella cartella *Macchine IDT*. Se saltate questo passaggio i vostri colleghi non potranno avere accesso alla macchina!.

**Installazione FileZilla Server**
- Tramite esplora risorse creare una cartella con nome *FTP* in *C:\*.
- Aprire il setup *FileZilla_Server-0.9.60.exe*
- Accettare termini e condizioni cliccando su *I Agree*.
- Cliccare su *Next* fino al termine dell'installazione.
- Cliccare su *Close* per terminare. Si aprirà in automatico la pagina di gestione del server.
- Effettuare il login con i seguenti dati:
    - Host: *localhost*.
    - Port: *14147*
    - Password: Lasciare per il momento vuota.
- Dal menù in alto cliccare su *Edit* e poi *Settings*.
- Spostarsi sulla scheda *Miscellaneous* a sinistra.
- Spuntare l'opzione *Start minimized*.
- Spostarsi sulla scheda *Admin Interface settings*.
- Spuntare l'opzione in basso *Change admin password* ed inserire i seguenti dati:
    - New Password:*NUMEROCOMMESSAupload*.
    - Retype new Password:*NUMEROCOMMESSAupload*.
- Cliccare su *OK* a destra per confermare le impostazioni.  
- Dal menù in alto cliccare su *Edit* e poi *Users*.
- Cliccare su *Add* a destra per aggiungere un utente. Rinominare l'utente come *upload*.
- Spuntare l'opzione *Password:* e inserire la password impostata in precedenza(*NUMEROCOMMESSAupload*).
- Spostarsi nella scheda *Shared folders* a sinistra, cliccare sul pulsante *Add* e selezionare la cartella creata all'inizio.
- Spuntare tutte le caselle relative ai permessi infine premere *OK* per salvare le modifiche.
- Dal menù in alto cliccare su *File* e infine su *Disconnect*. Sempre dallo stesso menù riconettersi al server cliccando su *Connect to server...*.
- Effettuare il login con i seguenti dati:
    - Host: *localhost*.
    - Port: *14147*
    - Password: *NUMEROCOMMESSAupload*.
    - Spuntare l'opzione *Always connect to this server* e cliccare su *OK* per connettersi.
- Il server FTP è ora configurato.
 

### Installazione moduli python da terminale
- Digitare nella barra di ricerca il comando *cdm*. Successivamente premere la combinazione di tasti *CTRL + MAIUSC* seguito dal tasto *Invio*. Si aprirà il terminale come amministratore.
- Eseguire i seguenti comandi:
    - *pip install pyqt5*
    - *pip install pymodbus==2.5.3*
    - *pip install logging* built-in
    - *pip install QLed -> Importare quello modificato in C:\Users\Panel\AppData\Local\Programs\Python\Python310\Lib\site-packages*
    - *pip install mysql.connector*
    - *pip install configparser*
    - *pip install pyinstaller*
    - *pip install pynput*
    
### Creare eseguibile in autostart del pannello operatore
- Aprire il terminale come amministratore digitando nella barra di ricerca il comando *cdm*. 
- Premere *Invio* per aprire il terminale.
- Spostarsi nella cartella di lavoro del pannello. Utilizzare il comando *cd C:\Program Files\IDT\HMI\ControlPanel*
- Eseguire il seguente comando: *pyinstaller --onefile --noconsole ControlPanel.py*
- Attendere la fine delle operazioni.
- Nella stessa cartella dello script verranno create altre due cartelle, "dist" e "build". La cartella "build" si può eliminare, nella cartella "dist" invece sarà presente il file .exe appena generato.
- Creare un collegamento del file .exe appena creato.
- Digitare nella barra di cerca *%appdata%*. Digitare *Invio* per aprire la cartella.
- Partendo dalla posizione attuale,spostarsi all'interno del percorso "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp"
- Tagliare ed incollare il collegamento appena creato all'interno della cartella "Startup". L'eseguibile ora si lancerà in automatico ad ogni avvio del sistema.

### Creare eseguibile in autostart del server MODBUS
- Aprire il terminale come amministratore digitando nella barra di ricerca il comando *cdm*. 
- Premere *Invio* per aprire il terminale.
- Spostarsi nella cartella di lavoro del pannello. Utilizzare il comando *cd C:\Program Files\IDT\HMI*
- Eseguire il seguente comando: *pyinstaller --onefile --noconsole pymodbusSERVER.py*
- Attendere la fine delle operazioni.
- Nella stessa cartella dello script verranno create altre due cartelle, "dist" e "build". La cartella "build" si può eliminare, nella cartella "dist" invece sarà presente il file .exe appena generato.
- Creare un collegamento del file .exe appena creato.
- Spostarsi all'interno del percorso "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp"
- Tagliare ed incollare il collegamento appena creato all'interno della cartella "StartUp". L'eseguibile ora si lancerà in automatico ad ogni avvio del sistema.
