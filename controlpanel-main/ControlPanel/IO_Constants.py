from QLed import QLed
import configparser
import os

LINUX = False
abspath_beginstr = r"C:\\Users\\FrancescoBenente\\git-projects\\controlpanel"

'''
    Apre il file di configurazione "config.ini" in lettura e salva le informazioni al suo interno nelle costanti sottostanti
'''


def readConfig():
    parser = configparser.SafeConfigParser()
    if not LINUX:
        parser.read(os.path.abspath(os.path.join(
            abspath_beginstr, "ControlPanel//configdata//config.ini")))

    else:
        parser.read('/home/pi/HMI/ControlPanel4/ControlPanel/config.ini')

    return parser


p = readConfig()

##
# Manual Commands Input
INPUT_MAN_S_END = ["200", 0]
INPUT_MAN_S_HOME = ["200", 1]
INPUT_MAN_B00_END = ["200", 2]
INPUT_MAN_B1SX_END = ["200", 3]
INPUT_MAN_B2_END = ["200", 4]
INPUT_MAN_B3_END = ["200", 5]
INPUT_MAN_B4_END = ["200", 6]
INPUT_MAN_B1DX_END = ["200", 7]
INPUT_MAN_B22_END = ["200", 8]
INPUT_MAN_B33_END = ["200", 9]
INPUT_MAN_B44_END = ["200", 10]
INPUT_MAN_B00_PRES = ["200", 11]
INPUT_MAN_B1SX_PRES = ["200", 12]
INPUT_MAN_B2_PRES = ["200", 13]
INPUT_MAN_B3_PRES = ["200", 14]
INPUT_MAN_B4_PRES = ["200", 15]
INPUT_MAN_B1DX_PRES = ["201", 0]
INPUT_MAN_B22_PRES = ["201", 1]
INPUT_MAN_B33_PRES = ["201", 2]
INPUT_MAN_B44_PRES = ["201", 3]
INPUT_MAN_PP1 = ["201", 4]
INPUT_MAN_PP2 = ["201", 5]
INPUT_MAN_OGG_END = ["201", 6]
INPUT_MAN_ERR_AV = ["201", 7]
INPUT_MAN_ONOFF_AV = ["201", 8]
INPUT_MAN_OK_AV = ["201", 9]


INPUT_MAN_AIRPRESSURE = "250"

##
# Manual Commands Output
OUTPUT_MAN_VALV_B1SX = ["150", 0]
OUTPUT_MAN_VALV_B1DX = ["150", 1]
OUTPUT_MAN_VALV_B00_B44 = ["150", 2]
OUTPUT_MAN_S = ["150", 3]
OUTPUT_MAN_OGG = ["150", 4]
OUTPUT_MAN_STOP_MOTOR = ["150", 5]

##
# General CONSTANTS
# [(REGISTRO DI PARTENZA),(NUMERO DI REGISTRI DA LEGGERE), ...]
OUTPUT_INFO_HMI = (0, 20)
INPUT_SYNOPTIC = (60, 50)
INPUT_PHRASES = (110, 20)
# Customizzazioni banner e frasi del pannello varie
INPUT_CUSTOMIZATION = (130, 20)
INPUT_MANUAL = (150, 50)
OUTPUT_MANUAL = (200, 51)
INPUT_PRODUCTION = (250, 50)
OUTPUT_PRODUCTION = (300, 50)
INPUT_HEARTBIT = (350, 1)
HEARTBIT_COUNTER_ERROR = 100
INPUT_ALARMS = (351, 100)
INPUT_ROBOT_INFO = (451, 100)
INPUT_CONFIGURATION = [(20, 40)]
# PRODUCTION_REGISTERS = [(0, 150), (250,301)]
PRODUCTION_REGISTERS = [OUTPUT_INFO_HMI, INPUT_SYNOPTIC, INPUT_PHRASES,
                        INPUT_CUSTOMIZATION, INPUT_PRODUCTION, OUTPUT_PRODUCTION, INPUT_ALARMS, INPUT_ROBOT_INFO]
MANUAL_REGISTERS = [INPUT_MANUAL, OUTPUT_MANUAL]

##
# Frasi HMI
INPUT_PANEL_PHRASE1 = "110"

##
# Banner customization
INPUT_CUSTOMIZATION_BANNER = "130"

##
# Production Input
# BITMAP/LED
INPUT_PROD_YELLOWA = "251"
INPUT_PROD_REDA = "252"
INPUT_PROD_GREENA = "253"
INPUT_PROD_YELLOWB = "254"
INPUT_PROD_REDB = "255"
INPUT_PROD_GREENB = "256"

INPUT_STOP_PROD_BUTTON = ["274", 0]
INPUT_INCREASE_COUNTER = ["282", 0]
INPUT_INCREASE_COUNTER_GOOD = ["282", 1]
INPUT_INCREASE_COUNTER_BAD = ["282", 2]
INPUT_PRINT_LABEL1 = ["283", 0]
INPUT_NUMER_SCREW_REG = "290"

##
# Allarmi
INPUT_SHOW_ALARM = ["351", 0]
# OUTPUT_ALARM_SHOWN = ["354", 0]
OUTPUT_ALARM_SHOWN = 354
OUTPUT_ALARM_ACCEPTED = [357, 0]
INPUT_ALARM_INDEXES = "361"
# Registro che interviene nel momento in cui viene premuto il pulsante di riesecuzione del ciclo
OUTPUT_ALARM_RETRY = 370

##
# Production Output
OUTPUT_PHASE = 0
OUTPUT_ALARM_PRINTER_1 = 300
OUTPUT_PRINT_LABEL1_ACK = 301

##
# Control Panel Pages
PHASE_LOGIN = 0
PHASE_HOME = 1
PHASE_PRODUCTION = 2
PHASE_CONFIGURATION = 3
PHASE_COUNTERS = 4
PHASE_MANUAL = 5
PHASE_LOG = 6
PHASE_USERS = 7
PHASE_SHUTDOWN = 8
PHASE_ADD_USER = 9
PHASE_DATETIME = 10
PHASE_LANG = 11
PHASE_IT = 12
PHASE_EN = 13
PHASE_LANG1 = 14
PHASE_LANG2 = 15
PHASE_IDT = 16
PHASE_ADVANCED_CONF = 17
PHASE_TOOLPATH_MANAGER = 18

##
# Alarm Indexes
PLC_LOST_ALARM_INDEX = 0
INITIALIZATION_FAILED = 1
NOT_DETECTED = 2
END_POSITION_TIMEOUT_OPERATOR = 3
HOME_POSITION_TIMEOUT_OPERATOR = 4
END_POSITION_TIMEOUT_ADMINISTRATOR = 5
HOME_POSITION_TIMEOUT_ADMINISTRATOR = 6

# OUTPUT CONFIGURATION
OUTPUT_COUNTER_NUM = 20


##
# CONSTANTS
GRAY = 0
RED = 1
YELLOW = 2
GREEN = 3
LED_COLOUR = {0: QLed.Yellow, 1: QLed.Red, 2: QLed.Yellow, 3: QLed.Green}
LED_STATUS = {0: False, 1: True, 2: True, 3: True}

MODBUS_TIMER = 0.1
COVER_WIDTH = 700
COVER_HEIGHT = 343

TITLE = "Control Panel"

'''
La lingua di default viene ora salvata su db nella tabella configuration con un valore intero:
- 1 => IT
- 2 => ENG
- 3 => LANG_1
- 4 => LANG_2
'''
DEFAULT_LANGUAGE = "EN"
DEFAULT_DESCRIPTION_LANGUAGE = "description_EN"
DEFAULT_NONE_PRODUCT = 0

##
# Peripherals addresses

DB_HOST = p.get('DEFAULT', 'db_host')
DB = p.get('DEFAULT', 'db_name')
DB_USER = p.get('DEFAULT', 'db_user')
DB_PASSWORD = p.get('DEFAULT', 'db_password')
DB_PORT = int(p.get('DEFAULT', 'db_port'))
CONTROL_PANEL_IP = p.get('DEFAULT', 'control_panel_ip')
SERVER_MODBUS_PORT = p.get('DEFAULT', 'server_modbus_port')
PRINTER_IP = p.get('DEFAULT', 'printer_ip')
PRINTER_PORT = int(p.get('DEFAULT', 'printer_port'))
PLC_IP = p.get('DEFAULT', 'plc_ip')
ROBOT_IP = p.get('DEFAULT', 'robot_ip')
ROBOT_TOKEN = p.get('DEFAULT', 'robot_token')
FTP_LOCAL_HOST = p.get('DEFAULT', 'local_ftp_host')
FTP_LOCAL_USER = p.get('DEFAULT', 'local_ftp_user')
FTP_LOCAL_PASSWORD = p.get('DEFAULT', 'local_ftp_password')
IMG_LINUX_PATH = os.path.abspath(os.path.join(
    abspath_beginstr, p.get('DEFAULT', 'img_linux_path')))
IMG_WIN_PATH = os.path.abspath(os.path.join(
    abspath_beginstr, p.get('DEFAULT', 'img_win_path')))
LABEL_LINUX_PATH = os.path.abspath(os.path.join(
    abspath_beginstr, p.get('DEFAULT', 'label_linux_path')))
LABEL_WIN_PATH = os.path.abspath(os.path.join(
    abspath_beginstr, p.get('DEFAULT', 'label_win_path')))
FTP_USERLOG_LINUX_PATH = os.path.abspath(os.path.join(
    abspath_beginstr, p.get('DEFAULT', 'ftp_userlog_linux_path')))
FTP_USERLOG_WIN_PATH = os.path.abspath(os.path.join(
    abspath_beginstr, p.get('DEFAULT', 'ftp_userlog_win_path')))
FTP_PRODLOG_LINUX_PATH = os.path.abspath(os.path.join(
    abspath_beginstr, p.get('DEFAULT', 'ftp_prodlog_linux_path')))
FTP_PRODLOG_WIN_PATH = os.path.abspath(os.path.join(
    abspath_beginstr, p.get('DEFAULT', 'ftp_prodlog_win_path')))
FTP_ALARMS_LINUX_PATH = os.path.abspath(os.path.join(
    abspath_beginstr, p.get('DEFAULT', 'ftp_alarmslog_linux_path')))
FTP_ALARMS_WIN_PATH = os.path.abspath(os.path.join(
    abspath_beginstr, p.get('DEFAULT', 'ftp_alarmslog_win_path')))
