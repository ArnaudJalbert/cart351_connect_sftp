import pysftp
import sched
import time
import json

# 1667760506257

CONNECT_HOST = 'cdaftp.concordia.ca'
CONNECT_USER = 'ar_jalbe'
CONNECT_PWORD = 'Kanasuta27!'
CONNECT_PORT = 222

DATA_DIRECTORY = "./My Home/public_html/html_pages/Asterisque/data"

def connect_and_check():

    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    sftp_connection = None

    sftp = pysftp.Connection(CONNECT_HOST, port=CONNECT_PORT, username=CONNECT_USER, password=CONNECT_PWORD,cnopts=cnopts)
    print("Connected to SFTP server")
    # getting to the data directory
    sftp.cwd(DATA_DIRECTORY)
    
    return sftp
        
def check_request(sftp, sc):

    try:
        # downloading the request file
        sftp.get('request.txt')

        # opening the file to read its content
        with open('request.txt', 'r') as request_file:
            # saving the content in a string
            request = request_file.read().replace('\n','').strip()
            print("Request Content: " + request)

        # check if there is a request
        if(request):

            entry = get_request_data(sftp, request)

            execute_request(entry)
            with open('request.txt', 'w') as overwrite_request:
                overwrite_request.write('')
            sftp.put('request.txt')
        else:
            print('No Request to Process')
    except:
        print("Error when connecting")

    s.enter(10, 0, check_request, (sftp,s,))

# TO BE IMPLEMENTED BY LUCIEN
def execute_request(data):
    print("Executing Request ", data['date'])

def get_request_data(sftp, request):

    sftp.get('data.json')

    with open('data.json', 'r') as data_file:
        data_json = data_file.read()
    
    data = json.loads(data_json)


    for entry in data:
        entry = dict(entry)
        if str(entry['date']) == str(request):
            return entry

if __name__ == "__main__":
    sftp = connect_and_check()
    s = sched.scheduler(time.time, time.sleep)
    s.enter(10, 0, check_request, (sftp,s,))
    s.run()