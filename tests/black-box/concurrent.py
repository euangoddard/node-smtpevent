from os import path
from smtplib import SMTP
from threading import Thread

MESSAGE_PATH = path.abspath(path.join(path.dirname(__file__), 'message.txt'))

class SendMessageThread(Thread):
    
    message = open(MESSAGE_PATH).read()
    
    def __init__(self, client_number, *args, **kwargs):
        super(SendMessageThread, self).__init__(*args, **kwargs)
        self._client_number = client_number
    
    def run(self):
        print 'Starting client: %d' % self._client_number
        server = SMTP('localhost', 1025)
        response = server.sendmail(
            'me@example.com', 'you@example.com', self.message
            )
        
        assert response == {}
        
        server.quit()
        
        print 'Finished message from client: %d' % self._client_number


def main():
    thread_count = 300
    print "Starting %d threads..." % thread_count
    
    for i in xrange(thread_count):
        message_thread = SendMessageThread(i)
        message_thread.start()

    
if __name__ == "__main__":
    main()
