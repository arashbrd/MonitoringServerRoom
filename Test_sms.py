from SendSMS import SendSMS
try:
    #تست ارسال پیامک
    txt='تست ارسال پیام'
    user=['a','b','091712345678']
    res=SendSMS(user,txt)
    if res['messages'][0]['status']==0:
        print('Success!!!')
except Exception as A:
    print(f'Error!!!\n{A}')
