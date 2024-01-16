import mariadb,datetime,os,json,hashlib
from dotenv import load_dotenv
load_dotenv()


def dbconn(db):
    creds = {
            'password':os.environ['dbpassword'],
            'host':os.environ['dbhost'],
            'port':int(os.environ['dbport']),
            'user':os.environ['dbuser'],
    }
    if db=='work':
        creds.update({
            'database':os.environ['dbname'],
        })
    elif db=='obf':
        creds.update({
            'database':os.environ['mldbname'],
        })        
    try:
        conn = mariadb.connect(**creds)
        return(conn)
    except mariadb.Error as e:
        print("Coudn't connect to mariadb",e)   
        return(False) 

def executequery(conn,query,data):
    cur = conn.cursor(dictionary=True)
    if data!=False:
        cur.execute(query,data)
    else:
        cur.execute(query)
    return(cur.fetchall())

def writemany(conn,query,data):
    cur = conn.cursor()
    cur.executemany(query,data)
    conn.commit()

def writequery(conn,query,data):
    cur = conn.cursor()
    cur.execute(query,data)
    conn.commit()

def writerecord(vars):
    conn = dbconn('work')
    try:
        ismi = executequery(conn,'SELECT ismi FROM devices WHERE imei = %s',[vars['imei']])[0]['ismi']
    except IndexError:
        ismi = 0
    data = [
        str(ismi),                                           # ismi
        vars['lon'],                                    # longitude
        vars['lat'],                                    # latitude
        vars['io_data']['External Voltage'],            # vehiclebattery
        vars['io_data']['Battery Voltage'],             # devicebattery,
        datetime.datetime.utcfromtimestamp(vars['d_time_unix']/1000), # eventdate
        str(vars['imei'])                                    # imei
    ]
    # Any appended items after this are not included in the recordid hash
    recordid = str(hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()) 
    data.append('auxilliaryserver')                      # origin 
    try:                                   
        data.append(vars['io_data']['Total Mileage'])   # canodometer 
    except KeyError:
        data.append(0)
    data.append(recordid)                               # record id
    query = 'INSERT INTO records (ismi,longitude,latitude,vehiclebattery,devicebattery,eventdate,imei,origin,canodometer,recordid) VALUES (?,?,?,?,?,?,?,?,?,?) on duplicate key update origin=VALUES(origin), imei=VALUES(imei),recordid=VALUES(recordid),ismi=VALUES(ismi),latitude=VALUES(latitude),longitude=VALUES(longitude),vehiclebattery=VALUES(vehiclebattery),devicebattery=VALUES(devicebattery),canodometer=VALUES(canodometer),eventdate=VALUES(eventdate)'
    writequery(conn,query,data)
    print('Record written')


conn = dbconn('work')
#test = executequery(conn,'SELECT * FROM records WHERE imei = %s',['866258049260125'])
#print(test)
a = '-104.9914566'
#print(a)
test = executequery(conn,'SELECT unique(ismi) from records',0)
print(len(test))