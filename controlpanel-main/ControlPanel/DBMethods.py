import mysql.connector
from mysql.connector.errors import Error
from mysql.connector import Error
from PyQt5.QtCore import QDate, QTime, Qt
from IO_Constants import *

##
# EVA SQL NON SONO STATE RITOCCATE, MANCANO ANCHE I COMMENTI
def eva_new_select_query_method(db, sql, value):
    err = False
    records = []
    try:
        connection = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database=db
        )

        cursor = connection.cursor()
        cursor.execute(sql,value)
        records = cursor.fetchall()
        print(records)
        if cursor.rowcount == 0:
            err = True
            
    except Error as e:
        print("Error reading data from MySQL table", e)
        err = True
        
    finally:
        if (connection.is_connected()):
            connection.close()
            cursor.close()
            print("MySQL connection is closed")
        return err, records

def eva_update_waypoint_query_method(db, value, label):
    error = False
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database=db
    )
    
    cur = db.cursor()
    sql = "UPDATE waypoints SET axis1 = %s, axis2 = %s, axis3 = %s, axis4 = %s, axis5 = %s, axis6 = %s WHERE label = %s"
    val = (value[0], value[1], value[2], value[3], value[4], value[5], label)
    try:
        cur.execute(sql, val)
        db.commit()
    except mysql.connector.Error as err:
        print(format(err))    
        error = True
    finally:
        db.close()
    return error

##
# PANEL SQL
'''
    Get the current date and time in format: AAAA-MM-GG HH:mm
'''
def getCurrentDateTime():
    d = QDate.currentDate().toString(Qt.ISODate)
    t = QTime.currentTime().toString("hh:mm:ss")
    timestamp = d + " " + t

    return timestamp

'''
    Get the current date and time in format: HH:mm:ss DD-MM-YYYY HH:mm:ss
'''
def getCurrentDateTimePrinter():
    d = QDate.currentDate().toString("dd/MM/yyyy")
    t = QTime.currentTime().toString("hh:mm:ss")
    timestamp = t + " " + d

    return timestamp

'''
    Imposta il campo counter_selected a True per il prodotto selezionato
'''
def update_counter_selected_query_method(counter_id, log):
    err = False
    sql = "UPDATE counters SET counter_selected = 'True' WHERE counter_id=%s"
    val = (counter_id,)
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASSWORD,
            port=DB_PORT,
            database=DB
        )
        cursor = connection.cursor()
        cursor.execute(sql, val)
        connection.commit()
    except mysql.connector.errors.DatabaseError as de:
        # print(format(de))
        log.error("update_counter_selected_query_method: "+format(de))
        err = True
    except mysql.connector.errors.InterfaceError as ie:
        # print(format(ie))
        log.error("update_counter_selected_query_method: "+format(ie))
        err = True
    finally:
        try:
            connection.close()
            cursor.close()
        except UnboundLocalError as ule:
            # print(format(ule))
            log.error("update_counter_selected_query_method: "+format(ule))
            err = True
        except NameError as ne:
            # print(format(ne))
            log.error("update_counter_selected_query_method: "+format(ne))
            err = True

'''
    Modifica i codici del prodotto selezionato (lato SX)
'''
def update_customer_code_sx_query_method(counter_id, internal_code_sx, customer_code_sx, log):
    err = False
    sql = "UPDATE counters SET internal_code_sx = %s, customer_code_sx = %s WHERE counter_id = %s"
    val = (internal_code_sx, customer_code_sx, counter_id)
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASSWORD,
            port=DB_PORT,
            database=DB
        )
        cursor = connection.cursor()
        cursor.execute(sql, val)
        connection.commit()
    except mysql.connector.errors.DatabaseError as de:
        # print(format(de))
        log.error("update_customer_code_sx_query_method: "+format(de))
        err = True
    except mysql.connector.errors.InterfaceError as ie:
        # print(format(ie))
        log.error("update_customer_code_sx_query_method: "+format(ie))
        err = True
    finally:
        try:
            connection.close()
            cursor.close()
        except UnboundLocalError as ule:
            # print(format(ule))
            log.error("update_customer_code_sx_query_method: "+format(ule))
            err = True
        except NameError as ne:
            # print(format(ne))
            log.error("update_customer_code_sx_query_method: "+format(ne))
            err = True
        return err

'''
    Modifica i codici del prodotto selezionato (lato DX)
'''
def update_customer_code_dx_query_method(counter_id, internal_code_dx, customer_code_dx, log):
    err = False
    sql = "UPDATE counters SET internal_code_dx = %s, customer_code_dx = %s WHERE counter_id = %s"
    val = (internal_code_dx, customer_code_dx, counter_id)
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASSWORD,
            port=DB_PORT,
            database=DB
        )
        cursor = connection.cursor()
        cursor.execute(sql, val)
        connection.commit()
    except mysql.connector.errors.DatabaseError as de:
        # print(format(de))
        log.error("update_customer_code_dx_query_method: "+format(de))
        err = True
    except mysql.connector.errors.InterfaceError as ie:
        # print(format(ie))
        log.error("update_customer_code_dx_query_method: "+format(ie))
        err = True
    finally:
        try:
            connection.close()
            cursor.close()
        except UnboundLocalError as ule:
            # print(format(ule))
            log.error("update_customer_code_dx_query_method: "+format(ule))
            err = True
        except NameError as ne:
            # print(format(ne))
            log.error("update_customer_code_dx_query_method: "+format(ne))
            err = True
        return err

'''
    Resetta il campo counter_selected di tutti i prodotti
'''
def reset_counter_selected_query_method(log):
    err = False
    sql = "UPDATE counters SET counter_selected = 'False'"
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASSWORD,
            port=DB_PORT,
            database=DB
        )
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
    except mysql.connector.errors.DatabaseError as de:
        # print(format(de))
        log.error("reset_counter_selected_query_method: "+format(de))
        err = True
    except mysql.connector.errors.InterfaceError as ie:
        # print(format(ie))
        log.error("reset_counter_selected_query_method: "+format(ie))
        err = True
    finally:
        try:
            connection.close()
            cursor.close()
        except UnboundLocalError as ule:
            # print(format(ule))
            log.error("reset_counter_selected_query_method: "+format(ule))
            err = True
        except NameError as ne:
            # print(format(ne))
            log.error("reset_counter_selected_query_method: "+format(ne))
            err = True

def update_counters_query_method(partialPSX, partialrefusePSX, totalrefusePSX, totalPSX, partialPDX, partialrefusePDX, totalrefusePDX, totalPDX, counter_id, log):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database=DB
    )
    
    cur = db.cursor()
    sql = "UPDATE counters SET partialPSX=%s, partialrefusePSX=%s, totalrefusePSX=%s, totalPSX=%s, partialPDX=%s, partialrefusePDX=%s, totalrefusePDX=%s, totalPDX=%s WHERE counter_id=%s"
    val = (partialPSX, partialrefusePSX, totalrefusePSX, totalPSX, partialPDX, partialrefusePDX, totalrefusePDX, totalPDX, counter_id)
    try:
        cur.execute(sql, val)
        db.commit()
    except mysql.connector.Error as err:
        log.error("update_counters_query_method: "+format(err))
        #print(format(err))
    db.close()

'''
    Esegue l'update dei parziali e dei totali del componente sinistro
'''
def update_counters_psx_query_method(partialPSX, partialrefusePSX, totalrefusePSX, totalPSX, counter_id, log):
    err = False
    sql = "UPDATE counters SET partialPSX=%s, partialrefusePSX=%s, totalrefusePSX=%s, totalPSX=%s WHERE counter_id=%s"
    val = (partialPSX, partialrefusePSX, totalrefusePSX, totalPSX, counter_id)
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASSWORD,
            port=DB_PORT,
            database=DB
        )
        cursor = connection.cursor()
        cursor.execute(sql, val)
        connection.commit()
    except mysql.connector.errors.DatabaseError as de:
        # print(format(de))
        log.error("update_counters_psx_query_method: "+format(de))
        err = True
    except mysql.connector.errors.InterfaceError as ie:
        # print(format(ie))
        log.error("update_counters_psx_query_method: "+format(ie))
        err = True
    finally:
        try:
            connection.close()
            cursor.close()
        except UnboundLocalError as ule:
            # print(format(ule))
            log.error("update_counters_psx_query_method: "+format(ule))
            err = True
        except NameError as ne:
            # print(format(ne))
            log.error("update_counters_psx_query_method: "+format(ne))
            err = True

'''
    Esegue l'update dei parziali e dei totali del componente destro
'''
def update_counters_pdx_query_method(partialPDX, partialrefusePDX, totalrefusePDX, totalPDX, counter_id, log):
    err = False
    sql = "UPDATE counters SET partialPDX=%s, partialrefusePDX=%s, totalrefusePDX=%s, totalPDX=%s WHERE counter_id=%s"
    val = (partialPDX, partialrefusePDX, totalrefusePDX, totalPDX, counter_id)
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASSWORD,
            port=DB_PORT,
            database=DB
        )
        cursor = connection.cursor()
        cursor.execute(sql, val)
        connection.commit()
    except mysql.connector.errors.DatabaseError as de:
        # print(format(de))
        log.error("update_counters_pdx_query_method: "+format(de))
        err = True
    except mysql.connector.errors.InterfaceError as ie:
        # print(format(ie))
        log.error("update_counters_pdx_query_method: "+format(ie))
        err = True
    finally:
        try:
            connection.close()
            cursor.close()
        except UnboundLocalError as ule:
            # print(format(ule))
            log.error("update_counters_pdx_query_method: "+format(ule))
            err = True
        except NameError as ne:
            # print(format(ne))
            log.error("update_counters_pdx_query_method: "+format(ne))
            err = True

'''
    Esegue l'update dei parziali del componente sinistro e destro
'''
def update_partial_counters_query_method(partialPSX, partialrefusePSX, partialPDX, partialrefusePDX, counter_id, log):
    err = False
    sql = "UPDATE counters SET partialPSX=%s, partialrefusePSX=%s, partialPDX=%s, partialrefusePDX=%s WHERE counter_id=%s"
    val = (partialPSX, partialrefusePSX, partialPDX, partialrefusePDX, counter_id)
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASSWORD,
            port=DB_PORT,
            database=DB
        )
        cursor = connection.cursor()
        cursor.execute(sql, val)
        connection.commit()
    except mysql.connector.errors.DatabaseError as de:
        # print(format(de))
        log.error("update_partial_counters_query_method: "+format(de))
        err = True
    except mysql.connector.errors.InterfaceError as ie:
        # print(format(ie))
        log.error("update_partial_counters_query_method: "+format(ie))
        err = True
    finally:
        try:
            connection.close()
            cursor.close()
        except UnboundLocalError as ule:
            # print(format(ule))
            log.error("update_partial_counters_query_method: "+format(ule))
            err = True
        except NameError as ne:
            # print(format(ne))
            log.error("update_partial_counters_query_method: "+format(ne))
            err = True

'''
    Esegue l'update della configurazione specificata nel parametro @configuration_id
'''
def update_configuration_query_method(configuration_id, value, log):
    err = False
    sql = "UPDATE configuration SET value=%s WHERE configuration_id=%s"
    val = (value, configuration_id)
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASSWORD,
            port=DB_PORT,
            database=DB
        )
        cursor = connection.cursor()
        cursor.execute(sql, val)
        connection.commit()
    except mysql.connector.errors.DatabaseError as de:
        # print(format(de))
        log.error("update_configuration_query_method: "+format(de))
        err = True
    except mysql.connector.errors.InterfaceError as ie:
        # print(format(ie))
        log.error("update_configuration_query_method: "+format(ie))
        err = True
    finally:
        try:
            connection.close()
            cursor.close()
        except UnboundLocalError as ule:
            # print(format(ule))
            log.error("update_configuration_query_method: "+format(ule))
            err = True
        except NameError as ne:
            # print(format(ne))
            log.error("update_configuration_query_method: "+format(ne))
            err = True

# OBSOLETA
def update_hid_query_method(hid_device):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database=DB
    )
    
    cur = db.cursor()
    sql = "UPDATE hid SET hid_id = %s"
    val = (hid_device,)
    try:
        cur.execute(sql, val)
        db.commit()
    except mysql.connector.Error as err:
        print(format(err))    
    db.close()

'''
    Inserisce log di produzione
'''
def insert_prodlog_query_method(n, counter_id, internal_code, customer_code, side, status_id, user_id, log):
    err = False
    datetimestamp = getCurrentDateTime()
    sql = "INSERT INTO prod_log (datetimestamp, serial, counter_id, internal_code, customer_code, side, status_id, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    params = (datetimestamp, n, counter_id, internal_code, customer_code, side, status_id, user_id)

    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASSWORD,
            port=DB_PORT,
            database=DB
        )
        cursor = connection.cursor()
        cursor.execute(sql, params)
        connection.commit()
    except mysql.connector.errors.DatabaseError as de:
        # print(format(de))
        log.error("insert_prodlog_query_method: "+format(de))
        err = True
    except mysql.connector.errors.InterfaceError as ie:
        # print(format(ie))
        log.error("insert_prodlog_query_method: "+format(ie))
        err = True
    finally:
        try:
            connection.close()
            cursor.close()
        except UnboundLocalError as ule:
            # print(format(ule))
            log.error("insert_prodlog_query_method: "+format(ule))
            err = True
        except NameError as ne:
            # print(format(ne))
            log.error("insert_prodlog_query_method: "+format(ne))
            err = True

'''
    Inserisce l'utente loggato nella tabella che tiene conto dei log degli utenti.
    Si può valutare se tenere conto dei totali buoni o scarto di ogni utente a seconda del proprio user_id
'''
def insert_userslog_query_method(status_id, user_id, counter_id, log):
    datetimestamp = getCurrentDateTime()
    err = False
    '''sql = "SELECT value FROM configuration WHERE configuration_id = %(conf_id)s"
    value = {'conf_id': "totalGood"}
    records, n_row, err = selectMethod(sql, value, log)
    if not err:
        total = records[0][0]
    else:
        total = 0
    value = {'conf_id': "totalRefuse"}
    records, n_row, err = selectMethod(sql, value, log)
    if not err:
        totalrefuse = records[0][0]
    else: 
        totalrefuse = 0'''
    
    sql = "INSERT INTO users_log (datetimestamp, status_id, user_id) VALUES (%s, %s, %s)"
    params = (datetimestamp, status_id, user_id)

    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASSWORD,
            port=DB_PORT,
            database=DB
        )
        cursor = connection.cursor()
        cursor.execute(sql, params)
        connection.commit()
    except mysql.connector.errors.DatabaseError as de:
        # print(format(de))
        log.error("insert_userslog_query_method: "+format(de))
        err = True
    except mysql.connector.errors.InterfaceError as ie:
        # print(format(ie))
        log.error("insert_userslog_query_method: "+format(ie))
        err = True
    finally:
        try:
            connection.close()
            cursor.close()
        except UnboundLocalError as ule:
            # print(format(ule))
            log.error("insert_userslog_query_method: "+format(ule))
            err = True
        except NameError as ne:
            # print(format(ne))
            log.error("insert_userslog_query_method: "+format(ne))
            err = True

'''
    Inserimento log allarmi
'''
def insert_alarmlog_query_method(counter_id, alarm_id, title, description_IT, description_EN, description_LANG1, description_LANG2, user_id, log):
    err = False
    current_datetime = getCurrentDateTime()
    sql = "INSERT INTO alarm_log (datetimestamp, counter_id, alarm_id, title, description_IT, description_EN, description_LANG1, description_LANG2, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    params = (current_datetime, counter_id, alarm_id, title, description_IT, description_EN, description_LANG1, description_LANG2, user_id)
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASSWORD,
            port=DB_PORT,
            database=DB
        )
        cursor = connection.cursor()
        cursor.execute(sql, params)
        connection.commit()
    except mysql.connector.errors.DatabaseError as de:
        # print(format(de))
        log.error("insert_alarmlog_query_method: "+format(de))
        err = True
    except mysql.connector.errors.InterfaceError as ie:
        # print(format(ie))
        log.error("insert_alarmlog_query_method: "+format(ie))
        err = True
    finally:
        try:
            connection.close()
            cursor.close()
        except UnboundLocalError as ule:
            # print(format(ule))
            log.error("insert_alarmlog_query_method: "+format(ule))
            err = True
        except NameError as ne:
            # print(format(ne))
            log.error("insert_alarmlog_query_method: "+format(ne))
            err = True

'''
    Inserisce un nuovo utente
'''
def insert_user_query_method(user_id, scancode, name, surname, usergroup_id, password, log):  
    err = False
    user_id = user_id.strip()
    scancode = scancode.strip()
    name = name.strip()
    surname = surname.strip()
    usergroup_id = usergroup_id.strip()

    sql = "INSERT INTO users (user_id, scancode, name, surname, usergroup_id, password) VALUES (%s, %s, %s, %s, %s, %s)"
    params = (user_id, scancode, name, surname, usergroup_id, password)

    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASSWORD,
            port=DB_PORT,
            database=DB
        )
        cursor = connection.cursor()
        cursor.execute(sql, params)
        connection.commit()
    except mysql.connector.errors.DatabaseError as de:
        # print(format(de))
        log.error("insert_user_query_method: "+format(de))
        err = True
    except mysql.connector.errors.InterfaceError as ie:
        # print(format(ie))
        log.error("insert_user_query_method: "+format(ie))
        err = True
    finally:
        try:
            connection.close()
            cursor.close()
        except UnboundLocalError as ule:
            # print(format(ule))
            log.error("insert_user_query_method: "+format(ule))
            err = True
        except NameError as ne:
            # print(format(ne))
            log.error("insert_user_query_method: "+format(ne))
            err = True
        return err

'''
    Rimuove l'utente specificato dal parametro @user_id
'''
def delete_user_query_method(user_id, log):
    err = False
    sql = "DELETE FROM users WHERE user_id=%s"
    val = (user_id,)
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASSWORD,
            port=DB_PORT,
            database=DB
        )
        cursor = connection.cursor()
        cursor.execute(sql, val)
        connection.commit()
    except mysql.connector.errors.DatabaseError as de:
        # print(format(de))
        log.error("delete_user_query_method: "+format(de))
        err = True
    except mysql.connector.errors.InterfaceError as ie:
        # print(format(ie))
        log.error("delete_user_query_method: "+format(ie))
        err = True
    finally:
        try:
            connection.close()
            cursor.close()
        except UnboundLocalError as ule:
            # print(format(ule))
            log.error("delete_user_query_method: "+format(ule))
            err = True
        except NameError as ne:
            # print(format(ne))
            log.error("delete_user_query_method: "+format(ne))
            err = True

'''
    Svuota la tabella indicata nel parametro @table
'''
def truncate_query_method(table, log):
    sql = "TRUNCATE TABLE " + table
    err = False
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASSWORD,
            port=DB_PORT,
            database=DB
        )
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
    except mysql.connector.errors.DatabaseError as de:
        # print(format(de))
        log.error("truncate_query_method: "+format(de))
        err = True
    except mysql.connector.errors.InterfaceError as ie:
        # print(format(ie))
        log.error("truncate_query_method: "+format(ie))
        err = True
    finally:
        try:
            connection.close()
            cursor.close()
        except UnboundLocalError as ule:
            # print(format(ule))
            log.error("truncate_query_method: "+format(ule))
            err = True
        except NameError as ne:
            # print(format(ne))
            log.error("truncate_query_method: "+format(ne))
            err = True

'''
    Perform the query specified in @sql parameter (MUST to be parameterized), with @params parameter passed. 
    Log into a file log any errors that may occurs
'''
def selectMethod(sql, params, log):
    err = False
    global connection, cursor
    records = []
    err = False
    n_row = 0
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASSWORD,
            port=DB_PORT,
            database=DB
        )
        cursor = connection.cursor()
        cursor.execute(sql, params)
        records = cursor.fetchall()
        n_row = cursor.rowcount
    except mysql.connector.errors.DatabaseError as de:
        # print(format(de))
        log.error(format(de)+". Query attempted: "+sql)
        err = True
    except mysql.connector.errors.InterfaceError as ie:
        # print(format(ie))
        log.error(format(ie)+". Query attempted: "+sql)
        err = True
    finally:
        try:
            connection.close()
            cursor.close()
        except UnboundLocalError as ule:
            # print(format(ule))
            log.error(format(ule)+". Query attempted: "+sql)
            err = True
        except NameError as ne:
            # print(format(ne))
            log.error(format(ne)+". Query attempted: "+sql)
            err = True

        return records, n_row, err

'''
Esegue la query molteplici volte scorrendo per tutta la lunghezza della tupla passata per parametro.
@val deve essere una TUPLA!.
@return err, restituisce l'esito di eventuali errori della query.
'''
def executeMultipleQuery(sql, val,log):
    err = False
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASSWORD,
            port=DB_PORT,
            database=DB
        )
        cursor = connection.cursor()
        cursor.executemany(sql, val)
        connection.commit()
    except mysql.connector.errors.DatabaseError as de:
        log.error("Exception catched in executeMultipleQuery: {}".format(de))
        connection.rollback()
        err = True
    except mysql.connector.errors.InterfaceError as ie:
        log.error("Exception catched in executeMultipleQuery: {}".format(ie))
        connection.rollback()
        err = True
    finally:
        try:
            connection.close()
            cursor.close()
        except UnboundLocalError as ule:
            log.error("Exception catched in executeMultipleQuery: {}".format(ule))
            connection.rollback()
            err = True
        except NameError as ne:
            log.error("Exception catched in executeMultipleQuery: {}".format(ne))
            connection.rollback()
            err = True
        return err