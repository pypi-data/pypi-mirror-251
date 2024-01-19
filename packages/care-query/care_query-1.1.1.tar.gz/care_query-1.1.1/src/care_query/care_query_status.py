# COPYRIGHT 2022 MONOOCLE INSIGHTS
# ALL RIGHTS RESERVED
# UNAUTHORIZED USE, REPRODUCTION, OR
# DISTRIBUTION STRICTLY PROHIBITED
#
# AUTHOR: Raymond Deiotte
# CREATION DATE: 2024/01/12 10:11:20
# LAST UPDATED: 2024/01/12 10:11:26


import hashlib
import redshift_connector
import time
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

class CQStatus:

    def __init__(self):
        '''
        Method to intialize the class
        '''
        self.aws_access_key_id = 'AKIAZCVCN636FGQSELUX'
        self.aws_secret_access_key = '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'
        self.bucket = 'cq-bulk-output'
        self.iam_role = 'arn:aws:iam::624184653564:role/service-role/AmazonRedshift-CommandsAccessRole-20230710T084824'

    def _getConnection(self):
        '''
        Method to get a connection to redshift
        @return:
        '''
        conn = redshift_connector.connect(
            # host='default.624184653564.us-east-2.redshift-serverless.amazonaws.com', #Redshift endpoint
            host = 'cq-redshift-cluster-2.c5urajdsuzll.us-east-2.redshift.amazonaws.com', #Redshift cluster endpoint
            port=5439,
            database='care_support',
            # user='rsuser',
            user='awsuser',
            password='Monocle1!',
            ssl='',
            sslmode='allow',
            access_key_id=self.aws_access_key_id,
            secret_access_key=self.aws_secret_access_key)

        return conn

    def doIt(self):
        '''
        Method to control the class
        '''

    def writeStatus(self, user, query, status):
        '''
        Method to write the status of a query to the database
        @param user:
        @param query:
        @param status:
        @return:
        '''
        ###TODO: Check and see if the query has already been written to the database
        existing_status = self.getStatus(user, query)
        if existing_status == 'no status':
            conn = self._getConnection()
            cur = conn.cursor()
            cur.execute(f'''insert into cq_status (user_token, query, status) values ('{user}', '{query}', '{status}');''')
            conn.commit()
            cur.close()
            conn.close()
            return True
        else:
            #Return the existing status for the query
            return existing_status

    def getStatus(self, user, query):
        '''
        Method to get the status of a query
        @param user:
        @param query:
        @return:
        '''
        conn = self._getConnection()
        cur = conn.cursor()
        cur.execute(f'''select status from cq_status where user_token = '{user}' and query = '{query}';''')
        df = cur.fetch_dataframe()
        cur.close()
        conn.close()
        if len(df) > 0:
            return df.iloc[0]['status']
        else:
            return 'no status'

    def updateStatus(self, user, query, status):
        '''
        Method to update the status of a query
        @param user:
        @param query:
        @param status:
        @return:
        '''
        conn = self._getConnection()
        cur = conn.cursor()
        cur.execute(f'''update cq_status set status = '{status}' where user_token = '{user}' and query = '{query}';''')
        conn.commit()
        cur.close()
        conn.close()
        return True

    def send_email(self, recipient, subject, body, status):
        """Sends an email with status-specific content."""

        sender_email = "cq_status@monocleinsights.com"  # Replace with your email address
        password = "CQMonocle1!"  # Replace with your email password

        message = MIMEText(body)
        message['Subject'] = f"{subject} - {status}"  # Include status in subject
        message['From'] = sender_email
        message['To'] = recipient

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:  # Use secure SMTP
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient, message.as_string())

    def notify_process_status(self, recipient, process_name, status):
        """Sends an email notification for a specific process status."""

        subject = f"Process Update: {process_name}"
        body = f"The process '{process_name}' currently has the status: {status}"
        self.send_email(recipient, subject, body, status)


if __name__ == '__main__':
    c = CQStatus()

    user = 'e69a66044d093ea67858784a99303ef7'
    now = datetime.now().strftime('%Y%m%d_%H%M%S')
    query = f'select * from care_support.cq_status;_{now}'
    hasher = hashlib.sha256()
    hasher.update(query.encode())
    query = hasher.hexdigest()
    email = 'rdeiotte@monocleinsights.com'

    #write status, update status, get status
    c.writeStatus(user, query, 'RUNNING')
    c.notify_process_status(email, query, 'RUNNING')
    time.sleep(10)
    status = c.getStatus(user, query)
    print(status)
    time.sleep(10)
    c.updateStatus(user, query, 'SUCCESS')
    c.notify_process_status(email, query, 'SUCCESS')
    time.sleep(10)
    status = c.getStatus(user, query)
    print(status)
