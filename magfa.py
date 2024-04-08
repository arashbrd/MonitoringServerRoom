

# -*- coding: utf-8 -*-
#
# Python samples are made with
#
# Requests: HTTP for Humans - https://pypi.org/project/requests/
# Zeep: Python SOAP client - https://pypi.org/project/zeep/
#
from requests import Session
from requests.auth import HTTPBasicAuth # or HTTPDigestAuth, or OAuth1, etc.
from zeep import Client
from zeep.transports import Transport
def MagfaSendSMS(unicode_string,mob_num):
    # credentials
    username = "itfasa_41625"
    password = "UtQ4MoVsGEKbHAEP"
    domain = "fums"

    # session
    session = Session()
    # basic auth
    session.auth = HTTPBasicAuth(username + '/' + domain, password)

    # soap
    wsdl = 'https://sms.magfa.com/api/soap/sms/v2/server?wsdl'
    client = Client(wsdl=wsdl, transport=Transport(session=session))
    # data
    messages = client.get_type('ns1:stringArray');
    senders = client.get_type('ns1:stringArray');
    recipients = client.get_type('ns1:stringArray');
    uids = client.get_type('ns1:longArray');
    encodings = client.get_type('ns1:intArray');
    udhs = client.get_type('ns1:stringArray');
    priorities = client.get_type('ns1:intArray');

    # data
    # plain_string = "Hi!"
    Unicode_string=unicode_string

    # call
    return client.service.send( messages(item=[Unicode_string]),     senders(item=["300041625"]),     recipients(item=[mob_num]),     uids(item=[1989812]),     encodings(item=[]),     udhs(item=[]),     priorities(item=[]))    