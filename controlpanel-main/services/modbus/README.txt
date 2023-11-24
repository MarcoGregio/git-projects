Per prima cosa caricare il file sul pannello (va bene anche il Desktop);
Aprire il terminale e spostarsi nel percorso contenente il file appena caricato (di solito il Desktop appunto);
Eseguire il seguente comando:
    $ sudo mv modbus_server.service /etc/systemd/system/
Il comando sposterà il file nella directory indicata, che contiene i servizi systemd del SO;
Dopodichè eseguire la seguente lista di comandi:
    $ sudo systemctl start modbus_server.service
        -> serve a testare il servizio
    $ systemctl status modbus_server.service
        -> non servono privilegi di root per eseguirlo e serve a verificare che tutto funzioni;
        -> nel caso vada tutto bene dovrebbe comparire qualcosa di simile se non uguale all'immagine allegata;
        -> N.B: quando si esegue questo comando si visualizza lo stato del servizio indicato. Per uscire da questa modalità basterà premere 'q',
            non è necessario premere niente altro dato che non succederà nulla.
    $ sudo systemctl enable modbus_server.service
        -> abilita il servizio all'avvio
    $ sudo systemctl restart modbus_server.service

N.B: il percorso nel quale sarà possibile visualizzare il servizio deve sempre essere il seguente: "/etc/systemd/system/modbus_server.service"
Un'altra cosa importante è che nel file modbus.sh che utilizzavamo ci sia soltanto più il comando:
#! /bin/bash
sudo hwclock --hctosys

Questo script dovrà comunque essere eseguito all'avvio come sempre, da terminale al seguente percorso "$ sudo nano /etc/xdg/lxsession/LXDE-pi/autostart"
inserire le righe seguenti:
@/home/pi/HMI/modbus.sh
@/home/pi/HMI/controlpanel.sh