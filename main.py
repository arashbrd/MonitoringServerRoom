from ast import And
import sys
import time,datetime
from Utils import read_Sensors,SaveErrorLog
from SendSMS import SendSMS
import sqlite3
import os



try:
    if os.path.exists("smslog.db"):
        os.remove("smslog.db")


    conn=sqlite3.connect('smslog.db')
    cur=conn.cursor()

    cur.execute(""" CREATE TABLE IF NOT EXISTS users(
        userID INT PRIMARY KEY,
        fname TEXT,
        lname TEXT,
        mobile TEXT,
        email_address TEXT);
        """)



    cur.execute(""" CREATE TABLE IF NOT EXISTS TempData(
        TempID INT PRIMARY KEY,
        error_count INT,
        warning_sendSMS_counter INT,
        status INT);
    """)
    # Status=0:Normal-1:Warning-2:Critical
    temp_data = (1,0,0,0)
    cur.execute("INSERT INTO TempData VALUES(?,?,?,?);", temp_data)

    users = [(1, 'Arash', 'Bordbar', '09173303491','arash.bordbar@gmail.com')]#, (2, 'Mohsen', 'Ramezani', '09173302957','mohsen_r122@yahoo.com),(3, 'Amin', 'Fiezi', '09178351575','fums.email@gmail.com')]

    cur.executemany("INSERT INTO users VALUES(?, ?, ?,?,?);", users)
    cur.execute(""" CREATE TABLE IF NOT EXISTS Settings(
    settingID INT PRIMARY KEY,
    warning_sendSMS_counter INT ,
    thereshhold_Degree REAL ,
    sms_Send_thereshhold INT,
    retry_after_error_times INT ,
    seconds_after_error_times INT, 
    seconds_after_ok_times INT );
    """)
    setting = (1,4,26.5,50,10,9,15)# this important Settings of program
    # ==================================
    # settings[0]===SeetingID
    # settings[1]===NotUsed!
    # settings[2]===25.5 :in this degree you enter to warning mode!
    # settings[3]===50 :number of time that system send SMS to Admins in warning mode!
    # settings[4]===10 :number of times that program retry after error connection--after that program exit.
    # settings[5]===900 :seconds of times that program retry after error connection
    # settings[6]===3600 :seconds of times that program check the temperiture when connection is OK!
    # ==============================
    cur.execute("INSERT INTO Settings VALUES(?,?, ?, ?,?,?,?);", setting)
    conn.commit()
    cur.execute("SELECT * FROM users;")
    all_users = cur.fetchall()
    cur.execute("SELECT seconds_after_error_times FROM Settings;")
    sec = cur.fetchone()[0]
    cur.execute("SELECT retry_after_error_times FROM Settings;")
    retry = cur.fetchone()[0]
    cur.execute("SELECT thereshhold_Degree FROM Settings;")
    thereshhold_Degree = cur.fetchone()[0]
    cur.execute("SELECT sms_Send_thereshhold FROM Settings;")
    sms_Send_thereshhold = int(cur.fetchone()[0])
    cur.execute("SELECT seconds_after_ok_times FROM Settings;")
    seconds_after_ok_times = int(cur.fetchone()[0])
    
    ErrorCount=0 
    while(True):
        cur.execute("SELECT error_count FROM TempData;")
        ErrorCount = cur.fetchone()[0]
        cur.execute("SELECT status FROM TempData;")
        status = cur.fetchone()[0]
        SensorDegrees,Error_status=read_Sensors()
        if not Error_status:
            print('Connection is OK...')
            cur.execute("SELECT warning_sendSMS_counter FROM TempData;")
            warning_sendSMS_counter = int(cur.fetchone()[0])
            print(f'sms_Send_thereshhold is {sms_Send_thereshhold}')
            print(f'thereshhold_Degree is {thereshhold_Degree}')
            # for i in range(len(SensorDegrees)):
            print('**********************')
            print(f'sensor number{0} is: {SensorDegrees[0]}')
            print(f'sensor number{1} is: {SensorDegrees[1]}')
            print(f'sensor number{2} is: {SensorDegrees[2]}')
            print('**********************')
                # ++++++++++++++++++++++++++++++Processing Sensor Data
            
            cur.execute('UPDATE TempData SET error_count = 0 WHERE TempID=1')
            conn.commit()
            print('---Setting Error Connection Count to 0...')
            print(f'warning_sendSMS_counter is {warning_sendSMS_counter}')
            if warning_sendSMS_counter<=sms_Send_thereshhold:

                
                print(f'---warning_sendSMS_counter--({warning_sendSMS_counter})-- is little than sms_Send_thereshhold--({sms_Send_thereshhold})--')
                
                if SensorDegrees[0]>=float(thereshhold_Degree) or SensorDegrees[1]>=float(thereshhold_Degree) or SensorDegrees[2]>=float(thereshhold_Degree)  :
                    cur.execute(f'UPDATE TempData SET status = 1 where TempID=1')
                    print('sendSMS..')
                    now=datetime.datetime.today()
                    txt=f'هشدار شماره{warning_sendSMS_counter+1}از{sms_Send_thereshhold}\n'
                    txt+=f'دمای حداقل یکی از سنسورها  بالاتر از {float(thereshhold_Degree)} میباشد\n'
                    # txt+='تاریخ:'
                    # txt+=str(gregorian_to_jalali(now.year,now.month,now.day)[0])+'\\'
                    # txt+=str(gregorian_to_jalali(now.year,now.month,now.day)[1])+'\\'
                    # txt+=str(gregorian_to_jalali(now.year,now.month,now.day)[2])
                    # txt+=f'--{now.hour}:{now.minute}:{now.second}'
                    warning_sendSMS_counter+=1
                    SendSMS(all_users,txt)
                    
                    cur.execute(f'UPDATE TempData SET warning_sendSMS_counter = {warning_sendSMS_counter} WHERE TempID=1')
                    conn.commit()
                    print(f'---Setting warning_sendSMS_counter to {warning_sendSMS_counter}...')
                else:

                    print(f'all sensors are not gt {thereshhold_Degree} so cheking status...')
                    cur.execute("SELECT status FROM TempData;")
                    status = int(cur.fetchone()[0])
                    print(f'status is {status}')
                    conn.commit()
                    if status:
                        txt1='شرایط به وضعیت نرمال بازگشت'
                        txt1+=f'دمای تمام سنسورها پایینتر از {thereshhold_Degree}میباشد'
                        SendSMS(all_users,txt1)
                    cur.execute(f'UPDATE TempData SET status = 0 where TempID=1')

                    cur.execute(f'UPDATE TempData SET warning_sendSMS_counter = 0 where TempID=1')
                    conn.commit()
                    
            
                        
                    
            print(f'---sleep for {seconds_after_ok_times} seconds')
            print('=======================')
            time.sleep(int(seconds_after_ok_times))

            # ++++++++++++++++++++++++++++++end of Processing Sensor Data
            cur.execute('UPDATE TempData SET error_count = 0 WHERE TempID=1')
            conn.commit()
        elif int(ErrorCount)>=int(retry):
            txt="ارتباط سیستم مانیتورینگ اتاق سرور با شبکه یا سنسورهای دما قطع گردیده است.لطفا بعد از برطرف نمودن مشکل برنامه رامجددا اجرا نموده ویا سرور راریستارت نمایید"
            SendSMS(all_users,txt)
            SaveErrorLog(txt)
            sys.exit()
        else:
            ErrorCount+=1
            cur.execute(f'UPDATE TempData SET error_count = {ErrorCount} WHERE TempID=1')
            conn.commit()
            print(f"Connection time out....\nRetry num:{ErrorCount} from {retry}\n=============")
            print(f'---sleep for {sec} seconds')
            SaveErrorLog(f"Connection time out....\nRetry num:{ErrorCount} from {retry}\n=============")
            SaveErrorLog(f'---sleep for {sec} seconds')
            time.sleep(int(sec))
except sqlite3.IntegrityError as err:
    txt='Please backup and DELETE smslog.db first!'
    print(txt)
    SaveErrorLog(txt)

    sys.exit()