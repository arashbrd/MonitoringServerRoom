# from operator import truediv
# from sqlite3 import Time
# from turtle import st
# import requests
# from bs4 import BeautifulSoup
# from SendSMS import SendSMS
# import time,datetime
# from jalaliCal import jalali_to_gregorian,gregorian_to_jalali

# warning_sendSMS_counter=0
# while(True):
#     thereshhold_Degree=22
#     sms_Send_thereshhold=3
#     persons_mobile=['09173303491','09173302957','09173329645']
#     login_url = 'http://192.168.110.37/GETUANDP.HTM'
#     payload = {'USERIME':'admin', 
#             'PASSIME':'admin'
#             }
#     try:
#         now=datetime.datetime.today()
        
#         # jyear,jmonth,jday=now.year,now.month,now.day
#         # print(jyear,jmonth,jday)
#         # if str(jmonth).startswith('0'):
#         #     jmonth=int(str(jmonth).removeprefix('0'))
#         # if str(jday).startswith('0'):
#         #     jday=int(str(jday).removeprefix('0'))

#         MyNumbers=[]
#         with requests.Session() as s:
#             response = s.post(login_url , data=payload)
#             # print(response.text)
#             index_page= s.get('http://192.168.110.37/SENSPAGE.HTM')
#             soup = BeautifulSoup(index_page.text, 'html.parser')
#             list = soup.find_all("td", width=True)
#             MyHtml=str(list[7])
#             # print(MyHtml)
#             MyHtml=MyHtml.split('<br/>')
#             First_Sensor=MyHtml[0].split('   ')[1].removesuffix('C').strip()
#             MyNumbers.append(float(First_Sensor))
#             print(f'First sensor is :{First_Sensor}')
#             Second_Sensor=MyHtml[1].split('   ')[1].removesuffix('C').strip()
#             MyNumbers.append(float(Second_Sensor))
#             print(f'Second sensor is :{Second_Sensor}')
#             Third_Sensor=MyHtml[2].split('   ')[1].removesuffix('C').strip()
#             MyNumbers.append(float(Third_Sensor))
#             print(f'Third sensor is :{Third_Sensor}')
#             print("=============")
            

#     except Exception as e:
#         print(f'Exception Eccured:{e}')
        

#     if warning_sendSMS_counter<=sms_Send_thereshhold:
#         for i in range(len(MyNumbers)):
#             if MyNumbers[i]>=thereshhold_Degree:
#                 print('sendSMS..')
#                 txt=f'هشدار شماره{warning_sendSMS_counter+1}\n'

#                 txt+=f'دمای سنسور {i+1} بالاتر از {thereshhold_Degree} میباشد\n'
#                 txt+='تاریخ:'
#                 txt+=str(gregorian_to_jalali(now.year,now.month,now.day)[0])+'\\'
#                 txt+=str(gregorian_to_jalali(now.year,now.month,now.day)[1])+'\\'
#                 txt+=str(gregorian_to_jalali(now.year,now.month,now.day)[2])
#                 txt+=f'--{now.hour}:{now.minute}:{now.second}'

#                 for j in range(len(persons_mobile)):
#                     SendSMS(persons_mobile[j],txt)       
#                 warning_sendSMS_counter+=1
#                 break
#     time.sleep(1000)    


# Decorator to print function call
# details
