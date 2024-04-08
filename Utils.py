
import datetime
from sys import exc_info
import requests
from bs4 import BeautifulSoup
import logging
def SaveErrorLog(txt):
    FORMAT = '%(asctime)s --%(levelname)s---%(message)s'


    logging.basicConfig( filename='msg.log', filemode='a' ,format=FORMAT)
    logging.error(txt)
    


def read_Sensors():

    error_status=False
    
    login_url = 'http://192.168.110.37/GETUANDP.HTM'
    payload = {'USERIME':'admin', 
            'PASSIME':'admin'
            }
    try:
        MyNumbers=[]
        with requests.Session() as s:
            response = s.post(login_url , data=payload)
            
            index_page= s.get('http://192.168.110.37/SENSPAGE.HTM')
            soup = BeautifulSoup(index_page.text, 'html.parser')
            list = soup.find_all("td", width=True)
            MyHtml=str(list[7])
            
            MyHtml=MyHtml.split('<br/>')
            First_Sensor=MyHtml[0].split('   ')[1].removesuffix('C').strip()
            MyNumbers.append(float(First_Sensor))
            Second_Sensor=MyHtml[1].split('   ')[1].removesuffix('C').strip()
            MyNumbers.append(float(Second_Sensor))
            Third_Sensor=MyHtml[2].split('   ')[1].removesuffix('C').strip()
            MyNumbers.append(float(Third_Sensor))

    #
    except requests.Timeout as e:
        # print("OOPS!! Timeout Error1")
        # print(str(e))
        error_status=True
        
    except requests.RequestException as e:
        error_status=True
        # print("OOPS!! General Error2")
        # print(str(e))
        
    except IndexError:
        error_status=True
    #     print("Someone closed the program")

    except Exception as e:
        error_status=True

    return MyNumbers,error_status




        

        


    
   