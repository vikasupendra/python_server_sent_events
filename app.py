import sys 
import argparse
import requests
import pandas as pd
from requests.exceptions import HTTPError
import pprint
import sseclient
import json
import threading
import time
from queue import Queue

print_lock = threading.Lock()

class APIClient(threading.Thread):
    def __init__(self, queue, args=(), kwargs=None):
        threading.Thread.__init__(self, args=(), kwargs=None)
        self.queue = queue
        #self.daemon = True
        #self.receive_messages = args[0]

    def run(self):

        try:
            url = 'https://live-test-scores.herokuapp.com/scores'

            headers = {'Accept': 'text/event-stream'}
            resp = requests.get(url, stream=True, headers=headers)
            client = sseclient.SSEClient(resp)

            rows = 0
            for event in client.events():
                #pprint.pprint(json.loads(event.data))
                rows += 1
                #print('event data: {} | type(json.loads(event.data)) - {} | type(event.data) - {} | rows: {}'.format(json.loads(event.data), type(json.loads(event.data)), type(event.data), rows))
                self.queue.put(json.loads(event.data))
                #print('queue size - {}'.format(self.queue.qsize()))
                sys.stdout.flush()                                                          # without this call, the output is buffered and may NOT show up on stdout

            print('status code - {}'.format(resp.status_code))
            print(resp.json())

            # If the response was successful, no Exception will be raised
            resp.raise_for_status()

        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            print('Success!')

class ResponseDataProcessor(threading.Thread):
    def __init__(self, queue, args=(), kwargs=None):
        threading.Thread.__init__(self, args=(), kwargs=None)
        self.queue = queue
        self.df = pd.DataFrame()

    def run(self):

        while True:
            if not self.queue.empty():
                msg = self.queue.get()
                #print('thread {} received msg - {}'.format(threading.currentThread().getName(), msg))

                self.process_message(msg)

    def process_message(self, message):

        print ('Thread {} received msg - {}'.format(threading.currentThread().getName(), message))          # type(msg) - <class dict>
        dftmp = pd.DataFrame([message])
        self.df = pd.concat([self.df, dftmp])
        self.min_exam = self.df['exam'].min()
                     
        #self.query_1()
        self.query_2()
        self.query_3()
        self.query_4(self.min_exam)
        #with print_lock:
            #print(self.df)
            #print('dataframe size - {} | schema - {}'.format(self.df.count(), self.df.dtypes))
            #print('dataframe size - {}'.format(self.df.count()))
            #sys.stdout.flush()
            
    def query_1(self):
        # List all users that have received at least one test score
        print('{}'.format(self.df.filter(items = ['studentId']).drop_duplicates()))  

    def query_2(self, student = 'Logan_Harber74'):
        # List the test results for a specified student, and provides the student's average score across all exams
        #print('{}'.format(self.df.query('studentId == \'{}\''.format(student))))

        dftmp = self.df['studentId'] == student
        print('{}'.format(self.df.loc[dftmp]))        
        avg_scores = self.df.loc[dftmp, 'score'].mean() 
        print('avg score for student {} - {}'.format(student, avg_scores))       

    def query_3(self):
        # List all the exams that have been recorded
        print('{}'.format(self.df.filter(items = ['exam']).drop_duplicates()))  

    def query_4(self, exam = 1559):        
        # List all the results for the specified exam, and provides the average score across all students
        
        dftmp = self.df['exam'] == exam
        print('{}'.format(self.df.loc[dftmp]))        
        avg_scores = self.df.loc[dftmp, 'score'].mean() 
        print('avg score for exam {} - {}'.format(exam, avg_scores))            


class KeyboardInput(threading.Thread):

    def __init__(self, queue, args=(), kwargs=None):
        threading.Thread.__init__(self, args=(), kwargs=None)
        self.queue = queue

    def run(self):

        while True:
            value = input("Please enter a value for the type of query:\n")
            print(f'You entered {value}')

            value = input("Please enter an integer:\n")
            print(f'You entered {value} and its type is {type(value)}')

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Process exam scores data ...')
    parser.add_argument('--student_name', help = 'Student Name')
    parser.add_argument('--exam_id', help = 'exam id')

    args = parser.parse_args()
    student_name = args.student_name
    exam_id = args.exam_id

    #for t in range(2):
    msg_q = Queue()
    kb_input_q = Queue()
    apiclient_thread = APIClient(msg_q)
    apiresp_processor_thread = ResponseDataProcessor(msg_q, kb_input_q)
    apiclient_thread.start()
    time.sleep(3)
    apiresp_processor_thread.start()    
    time.sleep(0.1)

    apiclient_thread.join()
    apiresp_processor_thread.join()
