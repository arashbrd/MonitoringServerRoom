from datetime import datetime
from email import message
import sys
from magfa import MagfaSendSMS
from jalaliCal import jalali_to_gregorian,gregorian_to_jalali
from SendEmail import SendEmail
from Utils import SaveErrorLog
def SendSMS(usersNum,Txt):
    Txt2= '.به نظر میرسد در عملکرد پنل پیامکی اختلالی به وجود آمده'
    try:
        for i in range(len(usersNum)):
            now=datetime.today()
            
            Txt1=Txt
            Txt1+='\n'
            Txt1+=str(gregorian_to_jalali(now.year,now.month,now.day)[0])+'/'
            Txt1+=str(gregorian_to_jalali(now.year,now.month,now.day)[1])+'/'
            Txt1+=str(gregorian_to_jalali(now.year,now.month,now.day)[2])
            Txt1+=f'-{now.strftime("%H")}:{now.strftime("%M")}:{now.strftime("%S")}'
            res=MagfaSendSMS(Txt1,usersNum[i][3])
            print(f'SMS was sent...{Txt1} for {usersNum[i][1]} {usersNum[i][2]} ')
            SaveErrorLog(f'SMS was sent...{Txt1} for {usersNum[i][1]} {usersNum[i][2]})->({usersNum[i][3]}) ')

            
            if res['messages'][0]['status']==1:
                subject='اتاق سرور دانشگاه'
                Txt2+=Txt1
                print('Sending Email due to (Func Problem)...')
                SaveErrorLog('Sending Email due to (Func Problem)...')
                SendEmail(usersNum[i][4],subject,Txt2)
                

                

    except Exception as e:
        print(f'An Error occured while Sending SMS...\n.')
        SaveErrorLog(f'An Error occured while Sending SMS...\n===============')
        SaveErrorLog(f'{e}')
        
        subject='اتاق سرور دانشگاه'
        Txt2+=Txt1
        print('Sending Email(Exception)...')
        SaveErrorLog(SaveErrorLog)
        SendEmail(usersNum[i][4],subject,Txt2)
        SaveErrorLog('Program Terminated!!!')
        sys.exit()
        
        
        
   