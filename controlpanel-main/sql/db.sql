-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versione server:              10.6.5-MariaDB - mariadb.org binary distribution
-- S.O. server:                  Win64
-- HeidiSQL Versione:            11.3.0.6295
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dump della struttura del database control_panel
DROP DATABASE IF EXISTS `control_panel`;
CREATE DATABASE IF NOT EXISTS `control_panel` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE `control_panel`;

-- Dump della struttura di tabella control_panel.alarms
DROP TABLE IF EXISTS `alarms`;
CREATE TABLE IF NOT EXISTS `alarms` (
  `alarm_id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `description_IT` text NOT NULL,
  `description_EN` text NOT NULL,
  `description_LANG1` text NOT NULL,
  `description_LANG2` text NOT NULL,
  `usergroup_id` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`alarm_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4;

-- Dump dei dati della tabella control_panel.alarms: ~13 rows (circa)
DELETE FROM `alarms`;
/*!40000 ALTER TABLE `alarms` DISABLE KEYS */;
INSERT INTO `alarms` (`alarm_id`, `title`, `description_IT`, `description_EN`, `description_LANG1`, `description_LANG2`, `usergroup_id`) VALUES
	(0, 'PLC COMMUNICATION LOST', 'La comunicazione tra il pannello operatore e il PLC si è interrotta.', 'Communication between Panel PC and PLC lost.', 'Komunikacja między panelem operatora a PLC została przerwana.', '', 'OPERATOR'),
	(1, 'INITIALIZATION FAILED', 'Inizializzazione del processo di produzione fallita. Questo errore potrebbe essere causato dallo scorretto posizionamento della pneumatica o della sensoristica. Accedere ai "Comandi Manuali" e verificare che tutti i cilindri siano in HOME POSITION e il corretto funzionamento della sensoristica.', 'Production initialization process failed. This error could be caused by incorrect pneumatics or sensors positioning. Access to "Manual Commands" to verify sensors and pneumatics proper functioning.', 'Nie udało się zainicjować procesu produkcyjnego. Ten błąd może być spowodowany nieprawidłowym położeniem pneumatyki lub czujników. Wejdź do „Poleceń ręcznych” i sprawdź, czy wszystkie cylindry są w HOME POSITION/POZYCJI WYJŚCIOWEJ i czy czujniki działają prawidłowo.', '', 'ADMINISTRATOR'),
	(2, '{sensor} NOT DETECTED', 'Componente/i {sensor} non rilevato/i dal sistema.', '{sensor} component(s) not detected by the system.', 'System nie wykrył komponentu/ów {sensor}.', '', 'ADMINISTRATOR'),
	(3, '{cylinder} END POSITION TIMEOUT ERROR', 'Errore di timeout posizionamento pneumatica. I cilindri {cylinder} non hanno raggiunto la posizione di lavoro. Accedere ai "Comandi Manuali" e verificare il corretto funzionamento dei sensori di finecorsa.', 'Pneumatics reaching position timeout error. {sensor} cylinders END POSITION not reached.\r\nAccess to "Manual Commands" to verify sensors and pneumatics proper functioning.', 'Błąd przekroczenia limitu czasu pozycjonowania pneumatycznego. Cylindry {sensor} nie osiągnęły pozycji roboczej. Wejdź do „Poleceń ręcznych” i sprawdź poprawność działania czujników wyłączników krańcowych.', '', 'OPERATOR'),
	(4, '{cylinder} HOME POSITION TIMEOUT ERROR', 'Errore di timeout posizionamento pneumatica. I cilindri {cylinder} non hanno raggiunto la posizione di riposo. Accedere ai "Comandi Manuali" e verificare il corretto funzionamento dei sensori di finecorsa.', 'Pneumatics reaching position timeout error. {sensor} cylinders HOME POSITION not reached.\r\nAccess to "Manual Commands" to verify sensors and pneumatics proper functioning.', 'Błąd przekroczenia limitu czasu pozycjonowania pneumatycznego. Cylindry {sensor} spoczynkowej. Wejdź do „Poleceń ręcznych” i sprawdź poprawność działania czujników wyłączników krańcowych.', '', 'OPERATOR'),
	(5, '{cylinder} END POSITION TIMEOUT ERROR', 'Errore di timeout posizionamento pneumatica. I cilindri {cylinder} non hanno raggiunto la posizione di lavoro. Accedere ai "Comandi Manuali" e verificare il corretto funzionamento dei sensori di finecorsa.', 'Pneumatics reaching position timeout error. {sensor} cylinders END POSITION not reached.\r\nAccess to "Manual Commands" to verify sensors and pneumatics proper functioning.', 'Błąd przekroczenia limitu czasu pozycjonowania pneumatycznego. Cylindry {sensor} nie osiągnęły pozycji roboczej. Wejdź do „Poleceń ręcznych” i sprawdź poprawność działania czujników wyłączników krańcowych.', '', 'ADMINISTRATOR'),
	(6, '{cylinder} HOME POSITION TIMEOUT ERROR', 'Errore di timeout posizionamento pneumatica. Il cilindri {cylinder} non hanno raggiunto la posizione di riposo. Accedere ai "Comandi Manuali" e verificare il corretto funzionamento dei sensori di finecorsa.', 'Pneumatics reaching position timeout error. {sensor} cylinders HOME POSITION not reached.\r\nAccess to "Manual Commands" to verify sensors and pneumatics proper functioning.', 'Błąd przekroczenia limitu czasu pozycjonowania pneumatycznego pozycjonowania. Cylindry {sensor} nie osiągnęły pozycji roboczej. Wejdź do „Poleceń ręcznych” i sprawdź poprawność działania czujników wyłączników krańcowych.', '', 'ADMINISTRATOR'),
	(7, 'SCREWDRIVING ERROR', 'Si è verificato un errore durante l\'avvitatura.', 'Tightening error occurred.', 'Wystąpił błąd dokręcania.', '', 'ADMINISTRATOR'),
	(8, 'VACUUM VALVE ERROR', 'Errore durante l\'attivazione del vuoto.', 'Error of the vacuum valve.', 'Błąd zaworu podciśnienia.', '', 'ADMINISTRATOR'),
	(9, 'LABEL ERROR', 'Errore relativo alla stampa o la lettura dell\'etichetta.\n Verificare le condizioni della stampante, ribbon o rotolo di etichette.', 'Error printing or reading the label.\nCheck the condition of the printer, ribbon or label roll.', '', '', 'ADMINISTRATOR'),
	(10, '{sensor} PROCESS ERROR', 'Errore durante l\'assemblaggio del componente indicato, riprovare.', 'Error processing the component, try again.', ' ', ' ', 'ADMINISTRATOR'),
	(11, 'POSITIVE AIRTIGHT TEST ERROR', 'Errore durante il test di tenuta con pressione in ingresso positiva. Sfera assente o non in posizione, oppure saldatura non stagna.', 'Error during airtight test with positive pressure. Sphere absent or not placed correctly, or weld not airtight.', 'Błąd podczas testu szczelności przy dodatnim ciśnieniu. Kula nieobecna lub umieszczona nieprawidłowo lub spaw nieszczelny.', ' ', 'ADMINISTRATOR'),
	(12, 'NEGATIVE AIRTIGHT TEST ERROR', 'Errore durante il test di tenuta con pressione in ingresso negativa. Sfera assente o non in posizione, oppure saldatura non stagna.', 'Error during airtight test with negative pressure. Sphere absent or not placed correctly, or weld not airtight.', 'Błąd podczas próby szczelności z podciśnieniem. Kula nieobecna lub umieszczona nieprawidłowo lub spaw nieszczelny.', ' ', 'ADMINISTRATOR');
/*!40000 ALTER TABLE `alarms` ENABLE KEYS */;

-- Dump della struttura di tabella control_panel.alarm_log
DROP TABLE IF EXISTS `alarm_log`;
CREATE TABLE IF NOT EXISTS `alarm_log` (
  `datetimestamp` datetime NOT NULL,
  `counter_id` varchar(50) NOT NULL,
  `alarm_id` int(11) NOT NULL,
  `title` varchar(100) NOT NULL,
  `description_IT` text NOT NULL,
  `description_EN` text NOT NULL,
  `description_LANG1` text NOT NULL,
  `description_LANG2` text NOT NULL,
  `user_id` varchar(20) NOT NULL,
  PRIMARY KEY (`datetimestamp`,`counter_id`,`alarm_id`,`title`),
  KEY `counter_id` (`counter_id`),
  KEY `alarm_id` (`alarm_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `alarm_log_ibfk_1` FOREIGN KEY (`counter_id`) REFERENCES `counters` (`counter_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dump dei dati della tabella control_panel.alarm_log: ~18 rows (circa)
DELETE FROM `alarm_log`;
/*!40000 ALTER TABLE `alarm_log` DISABLE KEYS */;
INSERT INTO `alarm_log` (`datetimestamp`, `counter_id`, `alarm_id`, `title`, `description_IT`, `description_EN`, `description_LANG1`, `description_LANG2`, `user_id`) VALUES
	('2023-06-07 17:18:01', '9855477880 con Gommoni', 1, 'INITIALIZATION FAILED', 'Inizializzazione del processo di produzione fallita. Questo errore potrebbe essere causato dallo scorretto posizionamento della pneumatica o della sensoristica. Accedere ai "Comandi Manuali" e verificare che tutti i cilindri siano in HOME POSITION e il corretto funzionamento della sensoristica.', 'Production initialization process failed. This error could be caused by incorrect pneumatics or sensors positioning. Access to "Manual Commands" to verify sensors and pneumatics proper functioning.', 'Nie udało się zainicjować procesu produkcyjnego. Ten błąd może być spowodowany nieprawidłowym położeniem pneumatyki lub czujników. Wejdź do „Poleceń ręcznych” i sprawdź, czy wszystkie cylindry są w HOME POSITION/POZYCJI WYJŚCIOWEJ i czy czujniki działają prawidłowo.', '', '0000'),
	('2023-06-07 17:18:31', '9855477880 con Gommoni', 5, 'Cilindro piantaggio 13-14/Cilindro piantaggio 15-16 END POSITION TIMEOUT ERROR', 'Errore di timeout posizionamento pneumatica. I cilindri Cilindro piantaggio 13-14/Cilindro piantaggio 15-16 non hanno raggiunto la posizione di lavoro. Accedere ai "Comandi Manuali" e verificare il corretto funzionamento dei sensori di finecorsa.', 'Pneumatics reaching position timeout error.  cylinders END POSITION not reached.\r\nAccess to "Manual Commands" to verify sensors and pneumatics proper functioning.', 'Błąd przekroczenia limitu czasu pozycjonowania pneumatycznego. Cylindry  nie osiągnęły pozycji roboczej. Wejdź do „Poleceń ręcznych” i sprawdź poprawność działania czujników wyłączników krańcowych.', '', '0000'),
	('2023-06-07 17:21:01', '9855477880 con Gommoni', 2, 'GOM 16 NOT DETECTED', 'Componente/i GOM 16 non rilevato/i dal sistema.', 'GOM 16 component(s) not detected by the system.', 'System nie wykrył komponentu/ów GOM 16.', '', '0000'),
	('2023-06-07 17:35:08', '9855477880 con Gommoni', 2, 'BOCCOLA 16 NOT DETECTED', 'Componente/i BOCCOLA 16 non rilevato/i dal sistema.', 'BOCCOLA 16 component(s) not detected by the system.', 'System nie wykrył komponentu/ów BOCCOLA 16.', '', '0000'),
	('2023-06-07 17:35:44', '9855477880 con Gommoni', 2, 'BOCCOLA 14/GOM 17 NOT DETECTED', 'Componente/i BOCCOLA 14/GOM 17 non rilevato/i dal sistema.', 'BOCCOLA 14/GOM 17 component(s) not detected by the system.', 'System nie wykrył komponentu/ów BOCCOLA 14/GOM 17.', '', '0000'),
	('2023-06-07 17:36:22', '9855477880 con Gommoni', 2, 'BOCCOLA 13/GOM 17 NOT DETECTED', 'Componente/i BOCCOLA 13/GOM 17 non rilevato/i dal sistema.', 'BOCCOLA 13/GOM 17 component(s) not detected by the system.', 'System nie wykrył komponentu/ów BOCCOLA 13/GOM 17.', '', '0000'),
	('2023-06-07 17:36:56', '9855477880 con Gommoni', 2, 'BOCCOLA 15/GOM 17 NOT DETECTED', 'Componente/i BOCCOLA 15/GOM 17 non rilevato/i dal sistema.', 'BOCCOLA 15/GOM 17 component(s) not detected by the system.', 'System nie wykrył komponentu/ów BOCCOLA 15/GOM 17.', '', '0000'),
	('2023-06-07 17:37:32', '9855477880 con Gommoni', 2, 'GOM 12/GOM 17 NOT DETECTED', 'Componente/i GOM 12/GOM 17 non rilevato/i dal sistema.', 'GOM 12/GOM 17 component(s) not detected by the system.', 'System nie wykrył komponentu/ów GOM 12/GOM 17.', '', '0000'),
	('2023-06-07 17:38:06', '9855477880 con Gommoni', 2, 'GOM 11/GOM 17 NOT DETECTED', 'Componente/i GOM 11/GOM 17 non rilevato/i dal sistema.', 'GOM 11/GOM 17 component(s) not detected by the system.', 'System nie wykrył komponentu/ów GOM 11/GOM 17.', '', '0000'),
	('2023-06-07 17:38:36', '9855477880 con Gommoni', 2, 'GOM 17 NOT DETECTED', 'Componente/i GOM 17 non rilevato/i dal sistema.', 'GOM 17 component(s) not detected by the system.', 'System nie wykrył komponentu/ów GOM 17.', '', '0000'),
	('2023-06-07 17:39:10', '9855477880 con Gommoni', 2, 'GOM 17/GOM 18 NOT DETECTED', 'Componente/i GOM 17/GOM 18 non rilevato/i dal sistema.', 'GOM 17/GOM 18 component(s) not detected by the system.', 'System nie wykrył komponentu/ów GOM 17/GOM 18.', '', '0000'),
	('2023-06-07 17:39:37', '9855477880 con Gommoni', 2, 'GOM 17 NOT DETECTED', 'Componente/i GOM 17 non rilevato/i dal sistema.', 'GOM 17 component(s) not detected by the system.', 'System nie wykrył komponentu/ów GOM 17.', '', '0000'),
	('2023-06-07 17:52:00', '9855477880 con Gommoni', 2, 'GOM 17 NOT DETECTED', 'Componente/i GOM 17 non rilevato/i dal sistema.', 'GOM 17 component(s) not detected by the system.', 'System nie wykrył komponentu/ów GOM 17.', '', '0000'),
	('2023-06-07 17:55:50', '9855479280 senza Gommoni', 2, 'GOM 11/GOM 12/GOM 17/GOM 18 NOT DETECTED', 'Componente/i GOM 11/GOM 12/GOM 17/GOM 18 non rilevato/i dal sistema.', 'GOM 11/GOM 12/GOM 17/GOM 18 component(s) not detected by the system.', 'System nie wykrył komponentu/ów GOM 11/GOM 12/GOM 17/GOM 18.', '', '0000'),
	('2023-06-07 17:56:42', '9855477880 con Gommoni', 1, 'INITIALIZATION FAILED', 'Inizializzazione del processo di produzione fallita. Questo errore potrebbe essere causato dallo scorretto posizionamento della pneumatica o della sensoristica. Accedere ai "Comandi Manuali" e verificare che tutti i cilindri siano in HOME POSITION e il corretto funzionamento della sensoristica.', 'Production initialization process failed. This error could be caused by incorrect pneumatics or sensors positioning. Access to "Manual Commands" to verify sensors and pneumatics proper functioning.', 'Nie udało się zainicjować procesu produkcyjnego. Ten błąd może być spowodowany nieprawidłowym położeniem pneumatyki lub czujników. Wejdź do „Poleceń ręcznych” i sprawdź, czy wszystkie cylindry są w HOME POSITION/POZYCJI WYJŚCIOWEJ i czy czujniki działają prawidłowo.', '', '0000'),
	('2023-09-18 12:05:18', '9855479280 senza Gommoni', 3, '{cylinder} END POSITION TIMEOUT ERROR', 'Errore di timeout posizionamento pneumatica. I cilindri {cylinder} non hanno raggiunto la posizione di lavoro. Accedere ai "Comandi Manuali" e verificare il corretto funzionamento dei sensori di finecorsa.', 'Pneumatics reaching position timeout error. {sensor} cylinders END POSITION not reached.\r\nAccess to "Manual Commands" to verify sensors and pneumatics proper functioning.', 'Błąd przekroczenia limitu czasu pozycjonowania pneumatycznego. Cylindry {sensor} nie osiągnęły pozycji roboczej. Wejdź do „Poleceń ręcznych” i sprawdź poprawność działania czujników wyłączników krańcowych.', '', '0000'),
	('2023-09-18 12:06:32', '9855479280 senza Gommoni', 3, 'Cilindro blocco END POSITION TIMEOUT ERROR', 'Errore di timeout posizionamento pneumatica. I cilindri Cilindro blocco non hanno raggiunto la posizione di lavoro. Accedere ai "Comandi Manuali" e verificare il corretto funzionamento dei sensori di finecorsa.', 'Pneumatics reaching position timeout error.  cylinders END POSITION not reached.\r\nAccess to "Manual Commands" to verify sensors and pneumatics proper functioning.', 'Błąd przekroczenia limitu czasu pozycjonowania pneumatycznego. Cylindry  nie osiągnęły pozycji roboczej. Wejdź do „Poleceń ręcznych” i sprawdź poprawność działania czujników wyłączników krańcowych.', '', '0000'),
	('2023-09-18 12:46:57', '9855479280 senza Gommoni', 6, '{cylinder} HOME POSITION TIMEOUT ERROR', 'Errore di timeout posizionamento pneumatica. Il cilindri {cylinder} non hanno raggiunto la posizione di riposo. Accedere ai "Comandi Manuali" e verificare il corretto funzionamento dei sensori di finecorsa.', 'Pneumatics reaching position timeout error. {sensor} cylinders HOME POSITION not reached.\r\nAccess to "Manual Commands" to verify sensors and pneumatics proper functioning.', 'Błąd przekroczenia limitu czasu pozycjonowania pneumatycznego pozycjonowania. Cylindry {sensor} nie osiągnęły pozycji roboczej. Wejdź do „Poleceń ręcznych” i sprawdź poprawność działania czujników wyłączników krańcowych.', '', 'op'),
	('2023-09-18 12:47:29', '9855479280 senza Gommoni', 6, '{cylinder} HOME POSITION TIMEOUT ERROR', 'Errore di timeout posizionamento pneumatica. Il cilindri {cylinder} non hanno raggiunto la posizione di riposo. Accedere ai "Comandi Manuali" e verificare il corretto funzionamento dei sensori di finecorsa.', 'Pneumatics reaching position timeout error. {sensor} cylinders HOME POSITION not reached.\r\nAccess to "Manual Commands" to verify sensors and pneumatics proper functioning.', 'Błąd przekroczenia limitu czasu pozycjonowania pneumatycznego pozycjonowania. Cylindry {sensor} nie osiągnęły pozycji roboczej. Wejdź do „Poleceń ręcznych” i sprawdź poprawność działania czujników wyłączników krańcowych.', '', 'op'),
	('2023-09-22 12:38:30', '9855479280 senza Gommoni', 0, 'PLC COMMUNICATION LOST', 'La comunicazione tra il pannello operatore e il PLC si è interrotta.', 'Communication between Panel PC and PLC lost.', 'Komunikacja między panelem operatora a PLC została przerwana.', '', '0000'),
	('2023-09-22 12:38:41', '9855479280 senza Gommoni', 0, 'PLC COMMUNICATION LOST', 'La comunicazione tra il pannello operatore e il PLC si è interrotta.', 'Communication between Panel PC and PLC lost.', 'Komunikacja między panelem operatora a PLC została przerwana.', '', '0000');
/*!40000 ALTER TABLE `alarm_log` ENABLE KEYS */;

-- Dump della struttura di tabella control_panel.bitmap
DROP TABLE IF EXISTS `bitmap`;
CREATE TABLE IF NOT EXISTS `bitmap` (
  `bitmap_id` int(11) NOT NULL,
  `bitmap_label` varchar(50) NOT NULL,
  `label` varchar(20) NOT NULL,
  PRIMARY KEY (`bitmap_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dump dei dati della tabella control_panel.bitmap: ~17 rows (circa)
DELETE FROM `bitmap`;
/*!40000 ALTER TABLE `bitmap` DISABLE KEYS */;
INSERT INTO `bitmap` (`bitmap_id`, `bitmap_label`, `label`) VALUES
	(0, 'Approach Cylinder', 'cylinder'),
	(1, 'Cilindro blocco', 'cylinder'),
	(2, 'Cilindro piantaggio 11-12', 'cylinder'),
	(3, 'Cilindro piantaggio 13-14', 'cylinder'),
	(4, 'Cilindro piantaggio 15-16', 'cylinder'),
	(5, 'Cilindro piantaggio 17-18', 'cylinder'),
	(6, 'Oggettivazione', 'cylinder'),
	(7, 'PP', 'sensor'),
	(8, 'GOM 11', 'sensor'),
	(9, 'GOM 12', 'sensor'),
	(10, 'BOCCOLA 13', 'sensor'),
	(11, 'BOCCOLA 14', 'sensor'),
	(12, 'BOCCOLA 15', 'sensor'),
	(13, 'BOCCOLA 16', 'sensor'),
	(14, 'GOM 17', 'sensor'),
	(15, 'GOM 18', 'sensor'),
	(16, 'Blocco Struttura', 'cylinder');
/*!40000 ALTER TABLE `bitmap` ENABLE KEYS */;

-- Dump della struttura di tabella control_panel.configuration
DROP TABLE IF EXISTS `configuration`;
CREATE TABLE IF NOT EXISTS `configuration` (
  `configuration_id` varchar(20) CHARACTER SET utf8mb4 NOT NULL,
  `value` int(11) NOT NULL DEFAULT 1,
  PRIMARY KEY (`configuration_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dump dei dati della tabella control_panel.configuration: ~6 rows (circa)
DELETE FROM `configuration`;
/*!40000 ALTER TABLE `configuration` DISABLE KEYS */;
INSERT INTO `configuration` (`configuration_id`, `value`) VALUES
	('default_lang', 1),
	('enable_manconf', 0),
	('enable_printer', 0),
	('tempo_II_pt_laterale', 1000),
	('tempo_pressione', 3),
	('tempo_pt_centrale', 1500),
	('tempo_pt_laterale', 2500);
/*!40000 ALTER TABLE `configuration` ENABLE KEYS */;

-- Dump della struttura di tabella control_panel.counters
DROP TABLE IF EXISTS `counters`;
CREATE TABLE IF NOT EXISTS `counters` (
  `counter_selected` varchar(5) NOT NULL DEFAULT 'False',
  `counter_num` int(11) NOT NULL,
  `counter_id` varchar(50) NOT NULL,
  `internal_code_sx` varchar(50) NOT NULL,
  `customer_code_sx` varchar(50) NOT NULL,
  `internal_code_dx` varchar(50) NOT NULL,
  `customer_code_dx` varchar(50) NOT NULL,
  `counter_photo_sx` varchar(50) NOT NULL,
  `counter_photo_dx` varchar(50) NOT NULL,
  `partialPSX` bigint(20) NOT NULL,
  `partialrefusePSX` bigint(20) NOT NULL,
  `totalrefusePSX` bigint(20) NOT NULL,
  `totalPSX` bigint(20) NOT NULL,
  `partialPDX` bigint(20) NOT NULL,
  `partialrefusePDX` bigint(20) NOT NULL,
  `totalrefusePDX` bigint(20) NOT NULL,
  `totalPDX` bigint(20) NOT NULL,
  `isEnabled` int(5) NOT NULL DEFAULT 0,
  PRIMARY KEY (`counter_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dump dei dati della tabella control_panel.counters: ~2 rows (circa)
DELETE FROM `counters`;
/*!40000 ALTER TABLE `counters` DISABLE KEYS */;
INSERT INTO `counters` (`counter_selected`, `counter_num`, `counter_id`, `internal_code_sx`, `customer_code_sx`, `internal_code_dx`, `customer_code_dx`, `counter_photo_sx`, `counter_photo_dx`, `partialPSX`, `partialrefusePSX`, `totalrefusePSX`, `totalPSX`, `partialPDX`, `partialrefusePDX`, `totalrefusePDX`, `totalPDX`, `isEnabled`) VALUES
	('False', 1, '9855477880 con Gommoni', '9855477880', ' ', ' ', ' ', 'production.png', 'production.png', 0, 0, 0, 2, 0, 0, 0, 0, 1),
	('True', 2, '9855479280 senza Gommoni', '9855479280', '  ', ' ', ' ', 'production.png', 'production.png', 0, 0, 1, 1, 0, 0, 0, 0, 1);
/*!40000 ALTER TABLE `counters` ENABLE KEYS */;

-- Dump della struttura di tabella control_panel.hid
DROP TABLE IF EXISTS `hid`;
CREATE TABLE IF NOT EXISTS `hid` (
  `hid_id` varchar(100) NOT NULL DEFAULT '',
  PRIMARY KEY (`hid_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dump dei dati della tabella control_panel.hid: ~0 rows (circa)
DELETE FROM `hid`;
/*!40000 ALTER TABLE `hid` DISABLE KEYS */;
INSERT INTO `hid` (`hid_id`) VALUES
	('HID 0801:0001');
/*!40000 ALTER TABLE `hid` ENABLE KEYS */;

-- Dump della struttura di tabella control_panel.international
DROP TABLE IF EXISTS `international`;
CREATE TABLE IF NOT EXISTS `international` (
  `international_id` varchar(50) NOT NULL,
  `phase` int(11) NOT NULL,
  `it` text NOT NULL,
  `en` text NOT NULL,
  `LANG1` text NOT NULL,
  `LANG2` text NOT NULL,
  PRIMARY KEY (`international_id`,`phase`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dump dei dati della tabella control_panel.international: ~222 rows (circa)
DELETE FROM `international`;
/*!40000 ALTER TABLE `international` DISABLE KEYS */;
INSERT INTO `international` (`international_id`, `phase`, `it`, `en`, `LANG1`, `LANG2`) VALUES
	('airpressure', 5, 'Stato Pressostato', 'Pressure Switch Status', 'Stan Presostatu', ''),
	('button_advanced', 3, 'Config.\nAvanzata', 'Advanced\nConfig.', 'Konfig.\nZaawansowana', ''),
	('button_alarmunlock', 0, 'SBLOCCA', 'UNLOCK', 'ODBLOKOWAĆ', ''),
	('button_auto', 1, 'MODALITA\' AUTOMATICA', 'AUTOMATIC MODE', 'TRYB AUTOMATYCZNY', ''),
	('button_configuration', 1, 'CONFIGURAZIONE', 'CONFIGURATION', 'KONFIGURACJA', ''),
	('button_counters', 1, 'CONTATORI', 'COUNTERS', 'LICZNIKI', ''),
	('button_hf_reset', 5, 'HOT FOIL reset anomalia', 'HOT FOIL reset error', '', ''),
	('button_hf_start', 5, 'HOT FOILT stampa', 'HOT FOIL print', '', ''),
	('button_lc', 5, 'Cilindro Bloccaggio', 'Locking Cylinder\nValve', 'ZAW. Cylindra\nBlokada', ''),
	('button_log', 1, 'LOG E ALLARMI', 'LOG AND ALARMS', 'DZIENNIK LOG I ALARMY', ''),
	('button_manual', 1, 'MODALITA\' MANUALE', 'MANUAL MODE', 'TRYB RĘCZNY', ''),
	('button_manualcommands', 1, 'COMANDI MANUALI', 'MANUAL COMMANDS', 'POLECENIA RĘCZNE ', ''),
	('button_objectivation', 5, 'Cilindro\nOggettivazione', 'Objectivation \nCylinder Valve', 'VALV Cylinder \nWalidacja', ''),
	('button_oc', 5, 'VALV Cilindro\nOggettivazione', 'Objectivation\nCylinder Valve', 'ZAW. Cylindra\nCel', ''),
	('button_piantaggio', 5, 'Cilindro Piantaggio', 'Insertion Cylinder', 'Siłownik wstawiania', ' '),
	('button_print', 6, 'STAMPA', 'PRINT', 'WYDRUK', ''),
	('button_reprocess', 0, 'PROCESSA\r\nNUOVAMENTE', 'RETRY', '', ''),
	('button_resetpartial', 4, 'RESET PARZIALI', 'RESET PARTIALS', 'RESET CZĘŚCIOWY', ''),
	('button_select', 3, 'Seleziona configurazione', 'Update configuration', 'Aktualizacja na DB', ' '),
	('button_stopproduction', 2, 'TERMINA PRODUZIONE', 'END PRODUCTION', 'ZAKOŃCZYĆ PRODUKCJĘ', ''),
	('check_conf', 3, 'ABILITA CONFIG.\r\nMANUALE', 'ENABLE MANUAL\r\nCONFIGURATION', 'WŁĄCZ KONFIGURACJA RĘCZNA', ''),
	('cil_avv', 5, 'Cilindro avvicinamento', 'Approach cylinder', ' ', ' '),
	('circolare_pieno', 5, 'VIBRATORE CIRCOLARE pieno', 'CIRCULAR FEEDER full', '', ''),
	('c_fi', 5, 'CARTESIANO fuori ingombro', 'CARTESIANO out of work area', '', ''),
	('c_ins_prelevati', 5, 'CARTESIANO inserti prelevati', 'CARTESIANO parts picked', '', ''),
	('c_pp_dep', 5, 'CARTESIANO pezzo depositato', 'CARTESIANO deposited part', '', ''),
	('descriptionBadgeLabel', 0, 'Sbloccare utilizzando il badge', 'Unlock with card', 'Odblokować za pomocą identyfikatora', ''),
	('descriptionBadgeLabel_alarm', 0, 'Sbloccare allarme utilizzando un badge ADMINISTRATOR', 'Unlock alarm with ADMINISTRATOR card', 'Odblokować alarm za pomocą identyfikatora ADMINISTRATORA', ''),
	('descriptionBadgeLabel_alarmtitle', 0, 'SBLOCCO ALLARME BADGE', 'BADGE ALARM UNLOCK', 'ODBLOKOWANIE ALARMU IDENTYFIKATORA', ''),
	('descriptionSuperLabel', 0, 'Sbloccare inserendo le credenziali', 'Logging by entering your credentials', 'Odblokować wprowadzając dane uprawnienia', ''),
	('descriptionSuperLabel_alarm', 0, 'Sbloccare allarme utilizzando credenziali ADMINISTRATOR', 'Unlock alarm with ADMINISTRATOR user credentials', 'Odblokować alarm za pomocą uprawnień ADMINISTRATORA', ''),
	('descriptionSuperLabel_alarmtitle', 0, 'SBLOCCO ALLARME CREDENZIALI', 'USER ALARM UNLOCK', 'ODBLOKOWANIE ALARMU UPRAWNIEŃ', ''),
	('descriptionSuperLabel_label', 0, 'Sbloccare allarme inserendo le credenziali ADMINISTRATOR', 'Unlock alarm by entering ADMINISTRATOR credentials', 'Odblokować alarm wprowadzając dane uprawnienia ADMINISTRATORA', ''),
	('descriptionSuperLabel_labeltitle', 0, 'SBLOCCO ALLARME CREDENZIALI', 'ALARM CREDENTIALS LOGIN', 'ODBLOKOWANIE ALARMU UPRAWNIEŃ', ''),
	('handle', 5, 'Maniglia', 'Handle', '', ''),
	('header_customer', 6, 'COD. CLIENTE', 'CUSTOMER CODE', 'KOD. KLIENTA', ''),
	('header_datetime', 6, 'DATA/ORA', 'DATETIME', 'DATA/GODZINA', ''),
	('header_int', 6, 'COD. INTERNO', 'INTERNAL CODE', 'KOD. WEWNĘTRZNY', ''),
	('header_message', 6, 'MESSAGGIO ALLARME', 'WARNING BODY', 'KOMUNIKAT ALARMU', ''),
	('header_n', 6, 'PROGRESSIVO', 'PROGRESSION', 'NARASTAJĄCO', ''),
	('header_name', 7, 'NOME', 'NAME', 'NAZWISKO', ''),
	('header_permission', 7, 'USERGROUP', 'USERGROUP', 'USERGROUP', ''),
	('header_product', 6, 'PRODOTTO', 'PRODUCT', 'PRODUKT', ''),
	('header_scancode', 7, 'SCANCODE', 'SCANCODE', 'SCANCODE', ''),
	('header_side', 6, 'STAZIONE', 'SIDE', 'STACJA', ''),
	('header_status', 6, 'ESITO', 'STATUS', 'WYNIK', ''),
	('header_surname', 7, 'COGNOME', 'SURNAME', 'NAZWISKO', ''),
	('header_user', 6, 'USER ID', 'USER ID', 'USER ID', ''),
	('header_userid', 7, 'USER ID', 'USER ID', 'USER ID', ''),
	('header_warning', 6, 'TITOLO ALLARME', 'WARNING TITLE', 'TYTUŁ ALARMU', ''),
	('hf_anomalia', 5, 'HOT FOIL anomalia', 'HOT FOIL failure', '', ''),
	('hf_cic_run', 5, 'HOT FOIL ciclo in corso', 'HOT FOIL cycle running', '', ''),
	('hf_pp1_dep', 5, 'PEZZO 1 depositato su HOT FOIL', 'Part 1 deposited on HOT FOIL', '', ''),
	('hf_pp2_dep', 5, 'PEZZO 2 depositato su HOT FOIL', 'Part 2 deposited on HOT FOIL', '', ''),
	('hf_pronta', 5, 'HOT FOIL pronta', 'HOT FOIL ready', '', ''),
	('label_airpressure', 2, 'Rilevata assenza aria.', 'Air pressure drop detected.', 'Stwierdzono brak powietrza.', ''),
	('label_alarms', 6, 'Riepilogo Allarmi:', 'Alarms Overview:', 'Zestawienie Alarmów:', ''),
	('label_alarm_robot', 2, 'Robot in allarme', 'Alarm robot', '', ''),
	('label_buoni', 4, 'BUONI', 'GOOD', '', ''),
	('label_cl_blocco_sicurezza', 5, 'Sblocco Sicurezza', 'Unlock Security culinder', ' ', ' '),
	('label_codifica', 5, 'Codifica', 'Coding', ' ', ' '),
	('label_codifica_stampo', 5, 'Codifica stampo', 'Mould coding', ' ', ' '),
	('label_componentpresence', 5, 'Presenza Componente', 'Component Presence', '', ''),
	('label_currentprod', 1, 'Prodotto corrente:', 'Current product:', 'Bieżący produkt:', ''),
	('label_customercode', 2, 'Codice Cliente', 'Customer Code', 'Kod Klienta', ''),
	('label_customercode', 3, 'Codice Cliente', 'Customer Code', 'Kod Klienta', ''),
	('label_customercodedx', 3, 'Codice Cliente DX', 'Customer Code DX', 'Kod Klienta Prawo', ''),
	('label_customercodesx', 3, 'Codice Cliente SX', 'Customer Code SX', 'Kod Klienta Lewo', ''),
	('label_day', 10, 'GIORNO', 'DAY', 'DZIEŃ', ''),
	('label_description', 3, 'Configurazione Prodotto Corrente', 'Current Product Configuration', 'Bieżąca Konfiguracja Produktu', ''),
	('label_description', 4, 'Contatori Prodotto:', 'Product Counters:', 'Licznik Produktu:', ''),
	('label_description', 17, 'Abilita/Disabilita Prodotti', 'Enable / Disable Products', 'Włącz / Wyłącz Produkty', ''),
	('label_device', 6, 'Selezionare device di salvataggio:', 'Select storage device:', 'Wybrać urządzeniu do zapisu:', ''),
	('label_emergency', 2, 'Ripristinare Fungo di Emergenza/Barriere', 'Reset Emergency Stop/Security Barriers.', '', ''),
	('label_enable_printer', 3, 'ABILITAZIONE\r\nSTAMPANTE', 'ENABLE\r\nPRINTER', 'WŁĄCZANIE\r\nDRUKARKI', ''),
	('label_gom', 5, 'Presenza Gommino', 'Rubbermaid presence', ' ', ' '),
	('label_hours', 10, 'ORE', 'HOURS', 'GODZINY', ''),
	('label_info', 6, 'Selezionare un elemento per procedere alla ristampa dell\'etichetta corrispondente.', 'Select an element in order to print again its own label.', 'Wybrać element, aby ponownie wydrukować odpowiednią etykietę.', ''),
	('label_intcode', 2, 'Codice Interno', 'Internal Code', 'Kod Wewnętrzny', ''),
	('label_internalcode', 3, 'Codice Interno', 'Internal Code', 'Kod Wewnętrzny: ', ''),
	('label_internalcodedx', 3, 'Codice Interno DX', 'Internal Code DX', 'Kod Wewnętrzny Prawo', ''),
	('label_internalcodesx', 3, 'Codice Interno SX', 'Internal Code SX', 'Kod Wewnętrzny Lewo', ''),
	('label_label', 6, 'Etichetta selezionata:', 'Selected label:', 'Wybrana etykieta:', ''),
	('label_lavoro', 5, 'Posizione lavoro', 'End position', 'Pozycji końcowej', ''),
	('label_machine', 4, 'Macchina', 'Machine', 'Maszyna', ''),
	('label_minutes', 10, 'MINUTI', 'MINUTES', 'MINUTY', ''),
	('label_model', 3, 'MODELLO', 'MODEL', 'MODEL', ''),
	('label_model', 17, 'MODELLO', 'MODEL', 'MODEL', ''),
	('label_modify', 10, 'MODIFICA', 'SET', 'MODYFIKACJA', ''),
	('label_month', 10, 'MESE', 'MONTH', 'MIESIĄC', ''),
	('label_name', 1, 'Utente', 'User', 'Użytkownik', ''),
	('label_name', 9, 'Nome:', 'Name:', 'Nazwisko:', ''),
	('label_partial', 2, 'PARZIALI:', 'PARTIAL:', 'Częściowe:', ''),
	('label_partial', 4, 'PARZIALI', 'PARTIAL COUNTERS', 'CZĘŚCIOWE', ''),
	('label_partialrefuse', 4, 'SCARTI PARZIALI', 'PARTIAL SCRAPS', 'CZĘŚCIOWO WYBRAKOWANE KOMPONENTY', ''),
	('label_partpresence', 5, 'Presenza Pezzo', 'Part Presence', '', ''),
	('label_pf', 5, 'Presenza Fonoassorbente', 'Soundproof Presence', 'Czujnik Obecności Dźwiękochłonny', ''),
	('label_pm', 5, 'Presenza Molletta', 'Clip Presence', 'Czujnik Obecności Clip', ''),
	('label_pp', 5, 'Presenza Pezzo', 'Part Presence', 'Czujnik Obecności', ''),
	('label_presence', 5, 'Sensore di presenza', 'Presence sensor', '', ''),
	('label_presence_sensor', 5, 'Sensore di presenza', 'Presence sensor', ' ', ' '),
	('label_presenza_tappo', 5, 'Presenza Tappo', 'Cap Presence', '', ''),
	('label_productionlog', 6, 'Riepilogo Produzione:', 'Production Overview:', 'Zestawienie Produkcji:', ''),
	('label_reset', 10, 'RESET', 'RESET', 'RESET', ''),
	('label_riposo', 5, 'Posizione riposo', 'Home position', 'Pozycji wyjściowej', ''),
	('label_robot_manual', 2, 'Robot in modalità manuale. Riportarlo in automatico.', 'Robot in manual mode.', '', ''),
	('label_scarti', 4, 'SCARTI', 'BAD', 'WYBRAKOWANE', ''),
	('label_screwingok', 5, 'Avvitatura OK', 'Screwing OK', 'Wkręcanie OK', ''),
	('label_st', 5, 'Presenza Starlock', 'Starlock Presence', '', ''),
	('label_stationstat', 2, 'Stato stazione', 'Station status', '', ''),
	('label_status', 5, 'Status', 'Status', '', ''),
	('label_status_vuoto', 5, 'Stato vuoto', 'Vacuum Valve status', '', ''),
	('label_surname', 9, 'Cognome:', 'Surname:', 'Nazwisko:', ''),
	('label_tempoPressione', 3, 'Tempo pressione', 'Pressure time', ' ', ' '),
	('label_title', 2, 'Modalità automatica prodotto:', 'Automatic Mode component:', 'Tryb automatyczny produktu:', ''),
	('label_title', 5, 'Comandi Manuali:', 'Manual Commands:', 'Polecenia ręczne:', ''),
	('label_title', 7, 'Panoramica Utenti:', 'Users Overview:', 'Przegląd Użytkowników:', ''),
	('label_title', 9, 'Registrazione nuovo utente:', 'Adding new users:', 'Rejestracja nowego użytkownika:', ''),
	('label_title', 10, 'Impostazioni Data e Ora:', 'Datetime Settings:', 'Ustawienie Daty i Godziny:', ''),
	('label_titlephotodx', 2, 'Panoramica Grafica:', 'Graphic Overview', 'Przegląd Grafiki:', ''),
	('label_titlephotosx', 2, 'Panoramica Pneumatica', 'Pneumatic Overview', 'Przegląd Pneumatyki', ''),
	('label_total', 2, 'TOTALI:', 'TOTAL:', 'Całkowity:', ''),
	('label_total', 4, 'TOTALI', 'TOTAL COUNTERS', 'RAZEM', ''),
	('label_totalrefuse', 4, 'SCARTI TOTALI', 'TOTAL SCRAPS', 'RAZEM WYBRAKOWANE KOMPONENTY', ''),
	('label_vuoto', 5, 'Valvola Vuoto', 'Vacuum Valve', '', ''),
	('label_warning', 1, 'Attenzione', 'Warning', 'Ostrzeżenie', ''),
	('label_warninvalidconf', 1, 'Configurazione automatica non valida. E\' possibile che sia stata impostata una produzione non idonea per questa macchina.', 'Invalid automatic configuration. This error occurs when a not suitable production for this machine is configured.', '', ''),
	('label_year', 10, 'ANNO', 'YEAR', 'ROK', ''),
	('lineare_pieno', 5, 'VIBRATORE LINEARE pieno', 'LINEAR FEEDER full', '', ''),
	('permission_denied_label', 0, 'Permessi insufficienti per eseguire l\'operazione.', 'Insufficient permissions to perform the operation.', 'Niewystarczające uprawnienia do wykonania operacji.', ''),
	('permission_denied_title', 0, 'Privilegi insufficienti', 'Permission denied.', 'Niewystarczające uprawnienia', ''),
	('pp_singolarizzatore', 5, 'SINGOLARIZZATORE presenza pezzo', 'SINGOLARIZZATORE presence sensor', '', ''),
	('presenza_biadesivo', 5, 'Presenza Biadesivo', 'Double coated presence', 'Dwustronny', ' '),
	('presenza_inserto', 5, 'Presenza Inserto', 'Insert presence', 'Wstaw obecność', ' '),
	('presenza_tampone', 5, 'Presenza Tampone', 'Tampon Presence', ' ', ' '),
	('prod_comp_dx', 5, 'CARTESIANO produzione destra', 'CARTESIANO right production', '', ''),
	('prod_comp_sx', 5, 'CARTESIANO produzione sinistra', 'CARTESIANO left production', '', ''),
	('qmessagebox_configuration', 3, 'Configurazione', 'Configuration', 'Konfiguracja', ''),
	('qmessagebox_configuration', 17, 'Configurazione', 'Configuration', 'Konfiguracja', ''),
	('qmessagebox_configuration_error', 3, 'Errore Configurazione', 'Configuration Error', 'Błąd Konfiguracji', ''),
	('qmessagebox_counter_update_error', 2, 'Errore aggiornamento contatori', 'Error during the update of the counters', '', ''),
	('qmessagebox_counter_update_error_title', 2, 'Errore aggiornamento contatori', 'Error during the update of the counters', '', ''),
	('qmessagebox_empty_text', 3, 'Campi vuoti!', 'Empty Fields!', 'Pola puste!', ''),
	('qmessagebox_error_accessdenied', 1, 'Permessi insufficienti per eseguire l\'operazione.', 'Insufficient permissions to perform the operation.', 'Niewystarczające uprawnienia do wykonania operacji.', ''),
	('qmessagebox_error_accessdenied_title', 1, 'Accesso negato', 'Access denied', 'Brak dostępu', ''),
	('qmessagebox_error_badge', 0, 'Scannerizzare il badge', 'Scan the timecard', 'Zeskanować identyfikator', ''),
	('qmessagebox_error_badprintrequest', 0, 'La stampa di etichette di componenti scarto non è consentita!', 'Printing "NOK" components label is forbidden!', 'Niedozwolony wydruk etykiet wybrakowanych komponentów!', ''),
	('qmessagebox_error_badprintrequest', 6, 'La stampa di etichette di componenti scarto non è consentita!', 'Printing "NOK" components label is forbidden!', 'Niedozwolony wydruk etykiet wybrakowanych komponentów!', ''),
	('qmessagebox_error_credentials', 0, 'Credenziali di accesso non valide.', 'Invalid login credentials.', 'Nieprawidłowe dane logowania.', ''),
	('qmessagebox_error_credentials_notfound', 0, 'Errore durante il login, utente non trovato. Riprovare.', 'Error during login, user not found. Try again.', '', ''),
	('qmessagebox_error_exit', 5, 'Per uscire dalla modalità \'Comandi Manuali\' è necessario riportare tutti gli assi e i cilindri in posizione Riposo.', 'You need to disable valves before exit.', 'Aby wyjść z trybu „Polecenia ręczne”, konieczne jest przywrócenie wszystkich osi i cylindrów do pozycji spoczynkowej.', ''),
	('qmessagebox_error_ftp', 6, 'Non è stato possibile effettuare il salvataggio del Log.', 'Log download failed.', 'Nie można było zapisać dziennika.', ''),
	('qmessagebox_error_idnumber', 0, 'Campo badge vuoto.', 'Empty card field.', 'Pole identyfikatora puste.', ''),
	('qmessagebox_error_manualmodedisabled', 1, 'Modalità manuale disattivata.', 'Manual mode disabled.', 'Tryb ręczny wyłączony.', ''),
	('qmessagebox_error_nameempty', 9, 'Il campo "Nome" è vuoto.', '"Name" field si empty.', 'Pole "Nazwisko" puste.', ''),
	('qmessagebox_error_newuser', 9, 'Impossibile aggiungere un utente già esistente.', 'Unable to add an existing user.', 'Nie można dodać istniejącego użytkownika.', ''),
	('qmessagebox_error_nolabel', 6, 'Nessuna etichetta selezionata per la stampa!', 'No label selected for printing!', 'Nie wybrano etykiety do wydruku!', ''),
	('qmessagebox_error_nouserselected', 7, 'Nessun utente selezionato per la rimozione.', 'No user to remove.', 'Nie wybrano użytkowników do usunięcia.', ''),
	('qmessagebox_error_password', 0, 'Campo "Password" vuoto.', 'Empty "Password" field.', 'Pole "Password/Hasło" puste.', ''),
	('qmessagebox_error_permissiondenied', 0, 'Permesso negato', 'Permission denied', 'Odmowa zezwolenia', ''),
	('qmessagebox_error_plclost', 5, 'Comunicazione PLC interrotta!', 'PLC communication lost!', 'Komunikacja z PLC przerwana!', ''),
	('qmessagebox_error_productionnotconfigured', 1, 'Nessun componente è stato configurato per la produzione. Assicurarsi di disporre dei privilegi necessari e selezionare un componente dal menu della modalità "Configurazione", altrimenti contattare un addetto alla manutenzione.', 'No component has been configured for production. Make sure you have the necessary privileges and select a component from the "Configuration" mode menu, otherwise contact a maintenance person.', 'Żaden komponent nie został skonfigurowany do produkcji. Upewnić się, czy posiada się niezbędne uprawnienia i wybrać komponent z menu trybu „Konfiguracji”, w przeciwnym razie skontaktować się z konserwatorem.', ''),
	('qmessagebox_error_productionnotconfigured_title', 1, 'Nessun componente in coda di produzione', 'No components in production queue', 'Brak komponentów w kolejce produkcyjnej', ''),
	('qmessagebox_error_scancodeempty', 9, 'Il campo "Scancode" è vuoto.', '"Scancode" field is empty.', 'Pole „Scancode” jest puste.', ''),
	('qmessagebox_error_surnameempty', 9, 'Il campo "Cognome" è vuoto.', '"Surname" field is empty.', 'Pole „Nazwisko” jest puste.', ''),
	('qmessagebox_error_title', 0, 'Errore', 'Error', 'Błąd', ''),
	('qmessagebox_error_title', 1, 'Errore', 'Error', 'Błąd', ''),
	('qmessagebox_error_title', 2, 'Errore modalità automatica', 'Automatic mode error.', 'Błąd trybu automatycznego', ''),
	('qmessagebox_error_title', 5, 'Errore', 'Error', 'Błąd', ''),
	('qmessagebox_error_title', 6, 'Errore Log e Allarmi', 'Log and Alarms error', 'Dziennik błędów i Alarmów', ''),
	('qmessagebox_error_title', 7, 'Errore', 'Error', 'Błąd', ''),
	('qmessagebox_error_usb', 6, 'Nessun drive di salvataggio selezionato!', 'No storage drive selected!', 'Nie wybrano dysku do zapisywania!', ''),
	('qmessagebox_error_userid', 0, 'Campo "User ID" vuoto.', 'Empty "User ID" field.', 'Puste pole  "User ID".', ''),
	('qmessagebox_error_useridempty', 9, 'Il campo "User ID" è vuoto.', '"User ID" field is empty.', 'Puste pole "User ID".', ''),
	('qmessagebox_information_addnewuser', 9, 'Sei sicuro/a di voler aggiungere un nuovo utente?', 'Are you sure you want to add a new user?\r\n', 'Czy na pewno chcesz dodać nowego użytkownika?', ''),
	('qmessagebox_information_completed', 3, 'Operazione completata con successo!', 'Success!', 'Operacja zakończona pomyślnie!', ''),
	('qmessagebox_information_ftp_alarmslog', 6, '"alarms_log.csv" è stato salvato con successo nel server. Accedere al server con un client FTP per visualizzarne il contenuto.', '"alarms_log.csv" has successfully been saved on the server. Access the server with an FTP client to download it.\r\n', 'Plik „users_log.csv” został pomyślnie zapisany na serwerze. Zaloguj się do serwera za pomocą klienta FTP, aby wyświetlić jego zawartość.', ''),
	('qmessagebox_information_ftp_prodlog', 6, '"production_log.csv" è stato salvato con successo nel server. Accedere al server con un client FTP per visualizzarne il contenuto.', '"production_log.csv" has successfully been saved on the server. Access the server with an FTP client to download it.', 'Plik "production_log.csv" Ã¨ został pomyślnie zapisany na serwerze. Zaloguj się do serwera za pomocą klienta FTP, aby wyświetlić jego  zawartość.', ''),
	('qmessagebox_information_ftp_title', 6, 'Salvataggio Log FTP', 'Log FTP Download', 'Zapisywanie Log FTP', ''),
	('qmessagebox_information_ftp_userslog', 6, '"users_log.csv" è stato salvato con successo nel server. Accedere al server con un client FTP per visualizzarne il contenuto.', '"users_log.csv" has successfully been saved on the server. Access the server with an FTP client to download it.', 'Plik „users_log.csv” został pomyślnie zapisany na serwerze. Zaloguj się do serwera za pomocą klienta FTP, aby wyświetlić jego zawartość.', ''),
	('qmessagebox_information_logout', 1, 'Sei sicuro/a di voler effettuare il logout?', 'Are you sure you want to log out?', 'Czy na pewno chcesz się wylogować?', ''),
	('qmessagebox_information_newuser_title', 9, 'Nuovo utente', 'New user', 'Nowy użytkownik', ''),
	('qmessagebox_information_reboot', 8, 'Sei sicuro/a di voler effettuare il riavvio del dispositivo?', 'Are you sure you want to restart the device?', 'Czy na pewno chcesz ponownie uruchomić urządzenie?', ''),
	('qmessagebox_information_reboot_title', 8, 'Riavvio', 'Reboot', 'Restart', ''),
	('qmessagebox_information_removal', 7, 'Utente rimosso con successo', 'User successfully removed', 'Usunięto użytkownika', ''),
	('qmessagebox_information_removal_title', 7, 'Rimozione utente', 'User removal', 'Usunięcie użytkownika', ''),
	('qmessagebox_information_shutdown', 8, 'Sei sicuro/a di voler effettuare lo spegnimento del dispositivo?', 'Are you sure you want to shutdown the device?', 'Czy na pewno chcesz wyłączyć urządzenie?', ''),
	('qmessagebox_information_shutdown_title', 8, 'Spegnimento', 'Shutdown', 'Wyłączenie', ''),
	('qmessagebox_information_useradded', 9, 'Utente aggiunto con successo.', 'User successfully added.', 'Użytkownik został dodany pomyślnie.', ''),
	('qmessagebox_information_userremovalquestion', 7, 'Sei sicuro/a di voler procedere alla rimozione dell\'utente selezionato? [USER ID : ', 'Are you sure you want to remove the selected user? [USER ID: ', 'Czy na pewno chcesz usunąć wybranego użytkownika? [USER ID : ', ''),
	('qmessagebox_info_emergency', 5, 'Le elettrovalvole attive sono state disabilitate. Ripristinare aria isola.', 'Active valves have been disabled. Restore air failure.', 'Aktywne zawory elektromagnetyczne zostały wyłączone. Przywrócić powietrze na wyspie.', ''),
	('qmessagebox_info_emergency_title', 5, 'Stato di Emergenza', 'Emergency Status', 'Stan Awaryjny', ''),
	('qmessagebox_info_title', 6, 'Info Log e Allarmi', 'Log and Alarms Info', 'Info Log i Alarmy', ''),
	('qmessagebox_printer_error', 2, 'Impossibile stampare etichetta!', 'An error occurred while label printing.', 'Nie można wydrukować etykiety!', ''),
	('qmessagebox_printer_error', 6, 'Impossibile stampare etichetta!', 'An error occurred while label printing.', 'Nie można wydrukować etykiety!', ''),
	('qmessagebox_printer_question', 6, 'L\'etichetta selezionata verrà stampata. Procedere?', 'Selected label will be printed. Do you really want to proceed?', 'Wybrana etykieta zostanie wydrukowana. Kontynuować?', ''),
	('qmessagebox_query_error', 3, 'Errore durante la generazione della query.', 'Exception raised during query generation.', 'Błąd podczas generowania zapytania.', ''),
	('qmessagebox_question_configuration', 3, 'Aggiornare le impostazioni di Configurazione Produzione?', 'Do you really want to update Production Configuration settings?', 'Zaktualizować ustawienia Konfiguracji produkcji?', ''),
	('qmessagebox_question_configuration', 17, 'Aggiornare le impostazioni di Configurazione Produzione?', 'Do you really want to update Production Configuration settings?', 'Zaktualizować ustawienia Konfiguracji produkcji?', ''),
	('qmessagebox_warning_passwordempty', 9, 'Il campo "Password" è vuoto.', '"Password" field is empty.', 'Pole "Password/Hasło" jest puste.', ''),
	('rob_error', 5, 'ROBOT in errore', 'ROBOT error', '', ''),
	('rob_fi', 5, 'ROBOT fuori ingombro', 'ROBOT out of work area', '', ''),
	('rob_home', 5, 'ROBOT in posizione home', 'ROBOT home position', '', ''),
	('rob_motor_en', 5, 'ROBOT motor enabled', 'ROBOT motor enabled', '', ''),
	('rob_remote_m', 5, 'ROBOT in remote mode', 'ROBOT in remote mode', '', ''),
	('rob_running', 5, 'ROBOT running', 'ROBOT running', '', ''),
	('rst_anomalia', 5, 'Reset amomalia impianto', 'Reset general error', '', ''),
	('r_ins_posizionati', 5, 'ROBOT inserti posizionati', 'ROBOT parts placed', '', ''),
	('r_ins_prelevati', 5, 'ROBOT inserti prelevati', 'ROBOT parts picked', '', ''),
	('singolarizzatore_lav', 5, 'SINGOLARIZZATORE posizione di lavoro', 'SINGOLARIZZATORE end position', '', ''),
	('singolarizzatore_rip', 5, 'SINGOLARIZZATORE posizione di riposo', 'SINGOLARIZZATORE home position', '', ''),
	('status_vuoto', 5, 'Stato del vuoto', 'Vacuum state', ' ', ' '),
	('stop_impianto', 5, 'STOP impianto', 'STOP machine', '', ''),
	('st_impianto', 5, 'START impianto', 'START machine', '', ''),
	('subtitle_station', 2, 'Processo:', 'Process:', 'Proces:', ''),
	('title_label', 11, 'Selezionare lingua di sistema:', 'Select System Language:', 'Wybrać język systemu:', ''),
	('title_pressure_stat', 5, 'Stato Pneumatica:', 'Pneumatics Status:', '', ''),
	('title_sensor_stat', 5, 'Stato Sensoristica:', 'Sensors Status:', '', ''),
	('valv', 5, 'Cilindro', 'Cylinder Valve', 'Zaw Cylindra', ' '),
	('valvc', 5, 'VALV Cilindri\r\nPiantaggio Starlock', 'Starlock\nInsertion\nValve', 'ZAWÓR Cylindrów\r\nOsadzenie Starlock', ''),
	('valv_lc', 5, 'Valvola Cilindro\r\nBloccaggio', 'Locking Cylinder\r\nValve', 'ZAW. Cylindra\r\nBlokada', ''),
	('valv_screwdriver', 5, 'Avvitatore ON/OFF', 'Screwdriver ON/OFF', 'Silnik Wkrętarki ON/OFF', '');
/*!40000 ALTER TABLE `international` ENABLE KEYS */;

-- Dump della struttura di tabella control_panel.machine_status
DROP TABLE IF EXISTS `machine_status`;
CREATE TABLE IF NOT EXISTS `machine_status` (
  `index` int(11) NOT NULL,
  `machine` text NOT NULL,
  `description_IT` text NOT NULL,
  `description_EN` text NOT NULL,
  `description_LANG1` text NOT NULL,
  `description_LANG2` text NOT NULL,
  PRIMARY KEY (`index`,`machine`(100)) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dump dei dati della tabella control_panel.machine_status: ~27 rows (circa)
DELETE FROM `machine_status`;
/*!40000 ALTER TABLE `machine_status` DISABLE KEYS */;
INSERT INTO `machine_status` (`index`, `machine`, `description_IT`, `description_EN`, `description_LANG1`, `description_LANG2`) VALUES
	(0, 'cartesiano', '', '', '', ''),
	(0, 'estun', '', '', '', ''),
	(0, 'hotfoil', '', '', '', ''),
	(1, 'cartesiano', 'Cartesiano fuori ingombro', '', '', ''),
	(1, 'estun', 'Robot fuori ingombro', '', '', ''),
	(1, 'hotfoil', 'Hot Foil pronta', '', '', ''),
	(1, 'rinco', 'Indice 1: Mancano le condizioni per avviare la saldatrice.', '', '', ''),
	(1, 'tavola', 'Indice 1: Mancano le condizioni per far ruotare la tavola.', '', '', ''),
	(1, 'vibratore', 'Vibratore lineare pieno', '', '', ''),
	(2, 'cartesiano', 'Cartesiano all\'interno dell\'area di ingombro/di lavoro', '', '', ''),
	(2, 'estun', 'Robot all\'interno dell\'area di ingombro/di lavoro', '', '', ''),
	(2, 'hotfoil', 'Hot Foil: ciclo in corso', '', '', ''),
	(2, 'rinco', 'Indice 2:Impossibile avviare la saldatrice, verificare errore sul generatore.', '', '', ''),
	(2, 'tavola', 'Indice 2: Induttivi di codifica da controllare.', '', '', ''),
	(2, 'vibratore', 'Vibratore lineare vuoto', '', '', ''),
	(3, 'cartesiano', 'Cartesiano: deposito effettuato', '', '', ''),
	(3, 'estun', 'Robot in posizione di home', '', '', ''),
	(3, 'hotfoil', 'Hot Foil anomalia', '', '', ''),
	(3, 'rinco', 'Indice 3: Timeout avviamento saldatrice.', '', '', ''),
	(3, 'tavola', 'Indice 3: Timeout partenza tavola.', '', '', ''),
	(3, 'vibratore', 'Vibratore circolare pieno', '', '', ''),
	(4, 'rinco', 'Indice 4: Errore del generatore durante la saldatura.', '', '', ''),
	(4, 'tavola', 'Indice 4: Timeout arrivo tavola.', '', '', ''),
	(4, 'vibratore', 'Vibratore circolare vuoto', '', '', ''),
	(5, 'rinco', 'Indice 5: Timeout saldatura.', '', '', ''),
	(5, 'tavola', 'Indice 5: Rotazione interrotta.', '', '', ''),
	(6, 'tavola', 'Indice 6: Perso il segnale di riposo del sonotrodo durante la rotazione della tavola.', '', '', '');
/*!40000 ALTER TABLE `machine_status` ENABLE KEYS */;

-- Dump della struttura di tabella control_panel.prod_log
DROP TABLE IF EXISTS `prod_log`;
CREATE TABLE IF NOT EXISTS `prod_log` (
  `serial` varchar(7) NOT NULL,
  `datetimestamp` datetime NOT NULL,
  `counter_id` varchar(50) NOT NULL,
  `internal_code` varchar(50) NOT NULL,
  `customer_code` varchar(50) NOT NULL,
  `side` varchar(10) NOT NULL,
  `status_id` varchar(20) NOT NULL,
  `user_id` varchar(20) NOT NULL,
  PRIMARY KEY (`datetimestamp`,`counter_id`),
  KEY `counter_id` (`counter_id`),
  KEY `status_id` (`status_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `prod_log_ibfk_1` FOREIGN KEY (`counter_id`) REFERENCES `counters` (`counter_id`),
  CONSTRAINT `prod_log_ibfk_2` FOREIGN KEY (`status_id`) REFERENCES `status` (`status_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dump dei dati della tabella control_panel.prod_log: ~4 rows (circa)
DELETE FROM `prod_log`;
/*!40000 ALTER TABLE `prod_log` DISABLE KEYS */;
INSERT INTO `prod_log` (`serial`, `datetimestamp`, `counter_id`, `internal_code`, `customer_code`, `side`, `status_id`, `user_id`) VALUES
	('0000001', '2023-06-07 17:20:36', '9855477880 con Gommoni', '9855477880', ' ', 'LEFT', 'OK', '0000'),
	('0000002', '2023-06-07 17:31:42', '9855477880 con Gommoni', '9855477880', ' ', 'LEFT', 'OK', '0000'),
	('0000003', '2023-09-18 12:04:08', '9855479280 senza Gommoni', '9855479280', '  ', 'LEFT', 'OK', '0000'),
	('0000000', '2023-09-18 12:04:12', '9855479280 senza Gommoni', '9855479280', '  ', 'LEFT', 'NOK', '0000');
/*!40000 ALTER TABLE `prod_log` ENABLE KEYS */;

-- Dump della struttura di tabella control_panel.status
DROP TABLE IF EXISTS `status`;
CREATE TABLE IF NOT EXISTS `status` (
  `status_id` varchar(20) NOT NULL,
  PRIMARY KEY (`status_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dump dei dati della tabella control_panel.status: ~4 rows (circa)
DELETE FROM `status`;
/*!40000 ALTER TABLE `status` DISABLE KEYS */;
INSERT INTO `status` (`status_id`) VALUES
	('LOGIN'),
	('LOGOUT'),
	('NOK'),
	('OK');
/*!40000 ALTER TABLE `status` ENABLE KEYS */;

-- Dump della struttura di tabella control_panel.synoptic
DROP TABLE IF EXISTS `synoptic`;
CREATE TABLE IF NOT EXISTS `synoptic` (
  `synoptic_id` int(11) NOT NULL,
  `it` text NOT NULL,
  `en` text NOT NULL,
  `LANG1` text NOT NULL,
  `LANG2` text NOT NULL,
  PRIMARY KEY (`synoptic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dump dei dati della tabella control_panel.synoptic: ~13 rows (circa)
DELETE FROM `synoptic`;
/*!40000 ALTER TABLE `synoptic` DISABLE KEYS */;
INSERT INTO `synoptic` (`synoptic_id`, `it`, `en`, `LANG1`, `LANG2`) VALUES
	(0, '', '', '', ''),
	(1, 'Ripristinare emergenza macchina.', 'Reset machine emergency status.', 'Przywrócić  alarmy maszyny.', ''),
	(2, 'Rilevata assenza aria.', 'Air pressure drop detected.', 'Stwierdzono brak powietrza.', ''),
	(3, 'Ripristinare Fungo di Emergenza/Barriere', 'Reset Emergency Stop/Security Barriers.', 'Przywrócić działanie Grzybka Awaryjnego/Barier', ''),
	(4, 'Caricare componenti.', 'Load new components.', 'Załadować nowe detale.\n', ''),
	(5, 'Produzione in corso...', 'Production in progress...', 'Produkcja w toku...', ''),
	(6, 'Completato con esito positivo. Scaricare componente.\n', 'Completed with Good Response. Unload components.', 'Ukończono pomyślnie. Usuń komponent.', ''),
	(7, 'Completato con esito negativo. Rimuovere Componente Scarto.', 'Completed with Bad Response. Unload bad components.', 'Nie udało się ukończyć. Usunąć wybrakowany detal.', ''),
	(8, 'Premere START per avviare il ciclo.', 'Push START Button to start the cycle.', 'Nacisnąć PRZYCISK START, aby rozpocząć cykl.', ''),
	(9, 'Premera START per chiudere il bloccaggio centrale.', 'Press START to close the central lock.', '', ''),
	(10, 'Procedere con l’avvitatura.', 'Start screw process.', '', ''),
	(11, 'Assemblare componenti.', 'Assembling parts.', '', ''),
	(12, 'Premere il bimanuale per procedere.', 'Press the two-hand control to proceed.', 'Nacisnąć przycisk sterowania dwoma rękami, aby kontynuować.', ' ');
/*!40000 ALTER TABLE `synoptic` ENABLE KEYS */;

-- Dump della struttura di tabella control_panel.users
DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `user_id` varchar(20) NOT NULL,
  `scancode` varchar(100) NOT NULL,
  `name` varchar(20) NOT NULL,
  `surname` varchar(20) NOT NULL,
  `usergroup_id` varchar(20) NOT NULL,
  `password` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`user_id`,`scancode`),
  KEY `usergroup_id` (`usergroup_id`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`usergroup_id`) REFERENCES `usersgroup` (`usergroup_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dump dei dati della tabella control_panel.users: ~3 rows (circa)
DELETE FROM `users`;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` (`user_id`, `scancode`, `name`, `surname`, `usergroup_id`, `password`) VALUES
	('0000', '', 'IDT', 'IDT', 'ADMINISTRATOR', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918'),
	('8162', 'ò0000000000000081620000008162_', 'Francesco', 'Benente', 'SUPER', '0e29976f06d01cc69c9fa45d7b608a7ecb20f851c85e5883a69b367dceaa9686'),
	('op', '', 'op', 'op', 'OPERATOR', '037aeaeaf4bbf26ddabe7256a8294dc52da48d575a1247b5c2598c47de7aebab');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;

-- Dump della struttura di tabella control_panel.usersgroup
DROP TABLE IF EXISTS `usersgroup`;
CREATE TABLE IF NOT EXISTS `usersgroup` (
  `usergroup_id` varchar(20) NOT NULL,
  `productionMode` varchar(10) NOT NULL,
  `manualMode` varchar(10) NOT NULL,
  `configuration` varchar(10) NOT NULL,
  `counters` varchar(10) NOT NULL,
  `manualCommands` varchar(10) NOT NULL,
  `log` varchar(10) NOT NULL,
  `users` varchar(10) NOT NULL,
  `superLogin` varchar(10) NOT NULL,
  PRIMARY KEY (`usergroup_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dump dei dati della tabella control_panel.usersgroup: ~4 rows (circa)
DELETE FROM `usersgroup`;
/*!40000 ALTER TABLE `usersgroup` DISABLE KEYS */;
INSERT INTO `usersgroup` (`usergroup_id`, `productionMode`, `manualMode`, `configuration`, `counters`, `manualCommands`, `log`, `users`, `superLogin`) VALUES
	('ADMINISTRATOR', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'no'),
	('MAINTAINER', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'no', 'no'),
	('OPERATOR', 'yes', 'no', 'no', 'yes', 'no', 'no', 'no', 'no'),
	('SUPER', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes');
/*!40000 ALTER TABLE `usersgroup` ENABLE KEYS */;

-- Dump della struttura di tabella control_panel.users_log
DROP TABLE IF EXISTS `users_log`;
CREATE TABLE IF NOT EXISTS `users_log` (
  `datetimestamp` datetime NOT NULL DEFAULT current_timestamp(),
  `status_id` varchar(20) NOT NULL,
  `user_id` varchar(20) NOT NULL,
  PRIMARY KEY (`datetimestamp`),
  KEY `status_id` (`status_id`),
  CONSTRAINT `users_log_ibfk_1` FOREIGN KEY (`status_id`) REFERENCES `status` (`status_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dump dei dati della tabella control_panel.users_log: ~130 rows (circa)
DELETE FROM `users_log`;
/*!40000 ALTER TABLE `users_log` DISABLE KEYS */;
INSERT INTO `users_log` (`datetimestamp`, `status_id`, `user_id`) VALUES
	('2023-05-29 14:36:45', 'LOGIN', '0000'),
	('2023-05-29 14:38:34', 'LOGIN', '0000'),
	('2023-05-29 14:40:23', 'LOGIN', '0000'),
	('2023-05-29 14:43:13', 'LOGIN', '0000'),
	('2023-05-29 14:49:51', 'LOGIN', '0000'),
	('2023-05-29 14:54:53', 'LOGIN', '0000'),
	('2023-05-29 14:55:25', 'LOGIN', '0000'),
	('2023-05-29 14:58:39', 'LOGIN', '0000'),
	('2023-05-29 14:59:52', 'LOGIN', '0000'),
	('2023-05-29 15:03:11', 'LOGIN', '0000'),
	('2023-05-29 15:06:16', 'LOGIN', '0000'),
	('2023-05-29 15:09:00', 'LOGIN', '0000'),
	('2023-05-29 16:19:05', 'LOGIN', '0000'),
	('2023-05-29 16:24:44', 'LOGIN', '0000'),
	('2023-05-31 12:05:54', 'LOGIN', '0000'),
	('2023-05-31 14:13:51', 'LOGIN', '0000'),
	('2023-05-31 17:52:10', 'LOGIN', '0000'),
	('2023-05-31 19:17:41', 'LOGIN', '0000'),
	('2023-05-31 19:37:39', 'LOGIN', '0000'),
	('2023-05-31 19:46:18', 'LOGIN', '0000'),
	('2023-05-31 19:53:07', 'LOGIN', '0000'),
	('2023-05-31 19:56:09', 'LOGIN', '0000'),
	('2023-05-31 20:02:48', 'LOGIN', '0000'),
	('2023-05-31 20:08:06', 'LOGIN', '0000'),
	('2023-05-31 20:10:12', 'LOGIN', '0000'),
	('2023-05-31 20:12:39', 'LOGIN', '0000'),
	('2023-05-31 20:13:30', 'LOGIN', '0000'),
	('2023-06-01 09:26:48', 'LOGIN', '0000'),
	('2023-06-01 10:17:53', 'LOGIN', '0000'),
	('2023-06-01 10:32:01', 'LOGIN', '0000'),
	('2023-06-01 12:42:19', 'LOGIN', '0000'),
	('2023-06-01 12:44:52', 'LOGIN', '0000'),
	('2023-06-01 12:47:34', 'LOGIN', '0000'),
	('2023-06-01 12:48:28', 'LOGIN', '0000'),
	('2023-06-01 12:49:39', 'LOGIN', '0000'),
	('2023-06-01 12:52:10', 'LOGIN', '0000'),
	('2023-06-01 14:02:39', 'LOGIN', '0000'),
	('2023-06-01 14:05:22', 'LOGIN', '0000'),
	('2023-06-01 14:06:22', 'LOGIN', '0000'),
	('2023-06-01 14:22:09', 'LOGIN', '0000'),
	('2023-06-01 14:29:36', 'LOGIN', '0000'),
	('2023-06-01 14:32:14', 'LOGIN', '0000'),
	('2023-06-01 14:54:02', 'LOGIN', '0000'),
	('2023-06-01 14:55:01', 'LOGIN', '0000'),
	('2023-06-01 14:55:49', 'LOGIN', '0000'),
	('2023-06-01 14:56:49', 'LOGIN', '0000'),
	('2023-06-01 14:58:06', 'LOGIN', '0000'),
	('2023-06-01 14:59:28', 'LOGIN', '0000'),
	('2023-06-01 15:00:26', 'LOGIN', '0000'),
	('2023-06-01 15:01:06', 'LOGIN', '0000'),
	('2023-06-01 15:23:21', 'LOGIN', '0000'),
	('2023-06-01 16:01:59', 'LOGIN', '0000'),
	('2023-06-01 16:58:09', 'LOGIN', '0000'),
	('2023-06-02 08:44:30', 'LOGIN', '0000'),
	('2023-06-03 08:59:10', 'LOGIN', '0000'),
	('2023-06-03 14:36:48', 'LOGIN', '0000'),
	('2023-06-04 09:08:19', 'LOGIN', '0000'),
	('2023-06-05 09:59:09', 'LOGIN', '0000'),
	('2023-06-06 08:40:03', 'LOGIN', '0000'),
	('2023-06-06 14:11:50', 'LOGIN', '0000'),
	('2023-06-06 14:13:12', 'LOGIN', '0000'),
	('2023-06-06 14:14:21', 'LOGIN', '0000'),
	('2023-06-06 14:15:23', 'LOGIN', '0000'),
	('2023-06-06 14:16:46', 'LOGIN', '0000'),
	('2023-06-06 14:18:29', 'LOGIN', '0000'),
	('2023-06-06 14:19:11', 'LOGIN', '0000'),
	('2023-06-06 14:36:13', 'LOGIN', '0000'),
	('2023-06-06 14:37:03', 'LOGIN', '0000'),
	('2023-06-06 14:37:51', 'LOGIN', '0000'),
	('2023-06-06 14:38:26', 'LOGIN', '0000'),
	('2023-06-06 14:42:00', 'LOGIN', '0000'),
	('2023-06-06 14:45:56', 'LOGIN', '0000'),
	('2023-06-06 14:46:54', 'LOGIN', '0000'),
	('2023-06-06 15:13:17', 'LOGIN', '0000'),
	('2023-06-06 15:14:45', 'LOGIN', '0000'),
	('2023-06-06 17:26:30', 'LOGIN', '0000'),
	('2023-06-06 17:43:06', 'LOGIN', '0000'),
	('2023-06-06 17:43:51', 'LOGIN', '0000'),
	('2023-06-06 17:46:45', 'LOGIN', '0000'),
	('2023-06-06 17:52:45', 'LOGIN', '0000'),
	('2023-06-06 17:54:02', 'LOGIN', '0000'),
	('2023-06-06 17:54:37', 'LOGIN', '0000'),
	('2023-06-06 18:12:29', 'LOGIN', '0000'),
	('2023-06-06 18:21:51', 'LOGIN', '0000'),
	('2023-06-06 18:24:44', 'LOGIN', '0000'),
	('2023-06-06 18:34:34', 'LOGIN', '0000'),
	('2023-06-06 18:35:31', 'LOGIN', '0000'),
	('2023-06-06 18:41:09', 'LOGIN', '0000'),
	('2023-06-06 18:48:20', 'LOGIN', '0000'),
	('2023-06-07 12:03:42', 'LOGOUT', '0000'),
	('2023-06-07 12:03:47', 'LOGIN', 'op'),
	('2023-06-07 12:05:22', 'LOGOUT', 'op'),
	('2023-06-07 12:05:33', 'LOGIN', '0000'),
	('2023-06-07 12:27:59', 'LOGOUT', '0000'),
	('2023-06-07 12:28:05', 'LOGIN', '0000'),
	('2023-06-07 12:29:24', 'LOGIN', '0000'),
	('2023-06-07 12:31:42', 'LOGIN', '0000'),
	('2023-06-07 12:33:41', 'LOGIN', '0000'),
	('2023-06-07 12:35:28', 'LOGIN', '0000'),
	('2023-06-07 12:37:37', 'LOGIN', '0000'),
	('2023-06-07 12:40:45', 'LOGIN', '0000'),
	('2023-06-07 12:47:35', 'LOGIN', '0000'),
	('2023-06-07 12:49:13', 'LOGIN', '0000'),
	('2023-06-07 12:51:09', 'LOGIN', '0000'),
	('2023-06-07 12:57:31', 'LOGIN', '0000'),
	('2023-06-07 13:01:14', 'LOGIN', '0000'),
	('2023-06-07 13:02:42', 'LOGIN', '0000'),
	('2023-06-07 13:03:12', 'LOGIN', '0000'),
	('2023-06-07 13:03:53', 'LOGIN', '0000'),
	('2023-06-07 13:07:48', 'LOGIN', '0000'),
	('2023-06-07 13:08:45', 'LOGIN', '0000'),
	('2023-06-07 13:09:34', 'LOGIN', '0000'),
	('2023-06-07 13:11:38', 'LOGIN', '0000'),
	('2023-06-07 13:18:54', 'LOGIN', '0000'),
	('2023-06-07 13:23:08', 'LOGIN', '0000'),
	('2023-06-07 13:24:00', 'LOGIN', '0000'),
	('2023-06-07 13:25:18', 'LOGIN', '0000'),
	('2023-06-07 13:28:02', 'LOGIN', '0000'),
	('2023-06-07 13:30:11', 'LOGIN', '0000'),
	('2023-06-07 13:33:07', 'LOGIN', '0000'),
	('2023-06-07 13:33:49', 'LOGIN', '0000'),
	('2023-06-07 13:34:21', 'LOGIN', '0000'),
	('2023-06-07 13:35:08', 'LOGIN', '0000'),
	('2023-06-07 13:37:35', 'LOGIN', '0000'),
	('2023-06-07 13:38:29', 'LOGIN', '0000'),
	('2023-06-07 15:30:39', 'LOGIN', '0000'),
	('2023-06-07 16:32:16', 'LOGIN', '0000'),
	('2023-06-07 16:39:19', 'LOGIN', '0000'),
	('2023-06-07 17:17:27', 'LOGIN', '0000'),
	('2023-06-07 17:29:52', 'LOGIN', '0000'),
	('2023-09-18 11:58:37', 'LOGIN', '0000'),
	('2023-09-18 12:36:13', 'LOGOUT', '0000'),
	('2023-09-18 12:37:30', 'LOGIN', '8162'),
	('2023-09-18 12:41:51', 'LOGIN', '0000'),
	('2023-09-18 12:45:40', 'LOGOUT', '0000'),
	('2023-09-18 12:45:49', 'LOGIN', 'op'),
	('2023-09-18 12:48:38', 'LOGOUT', 'op'),
	('2023-09-18 12:48:44', 'LOGIN', '0000'),
	('2023-09-18 13:10:08', 'LOGIN', '0000'),
	('2023-09-22 12:32:41', 'LOGIN', '0000'),
	('2023-09-22 12:34:52', 'LOGIN', '0000'),
	('2023-09-22 12:35:28', 'LOGIN', '0000'),
	('2023-09-22 12:36:01', 'LOGIN', '0000'),
	('2023-09-22 12:38:18', 'LOGIN', '0000');
/*!40000 ALTER TABLE `users_log` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
