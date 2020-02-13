from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import base64
from bs4 import BeautifulSoup

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'

def main():
   
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))
    
    # Call the Gmail API to fetch INBOX
    results = service.users().messages().list(userId='me',labelIds = ['INBOX']).execute()
    messages = results.get('messages', [])
    screenedMsgs = []
    

    if not messages:
        print ("No messages found.")
    else:
        print ("Scanning Messages...")
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            ''' content = msg["raw"]
            html = base64.urlsafe_b64decode(content)
            soup = BeautifulSoup(html, 'html5lib')
            print(soup)
            '''

            headers = msg["payload"]["headers"]
            
            subject = [i['value'] for i in headers if i["name"]=="Subject"]

            
            try:
                if subject[0] == 'TestBot':
                    print('Added ' + str(subject[0]) + ' email with ID: ' + str(msg['id']))
                    rawMsg = service.users().messages().get(userId='me', id=msg['id'], format='raw').execute()
                    screenedMsgs.append(rawMsg)
                    
            except Exception as err:
                print(str(err))
        
    return screenedMsgs
          

if __name__ == '__main__':
    main()
