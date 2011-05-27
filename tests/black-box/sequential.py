#!/usr/bin/python
# -*- coding: utf-8 -*-

from smtplib import SMTP
from telnetlib import Telnet
import unittest

class SequentialTests(unittest.TestCase):
    
    addrs = [
        'bob@example.com', 'sheila@example.com', 'kurt@example.com',
        'wendy@example.com', 'tim@example.com'
        ]
    
    def testFiveSequentialMessages(self):
        """5 sequential messages can be sent in the same connection."""
        
        server = SMTP('localhost', 1025)
        
        for from_addr, to_addr in zip(self.addrs, reversed(self.addrs)):
        
            response = server.sendmail(
                from_addr, [to_addr],
                'This is a test message\nSecond line.\nFinal line here.'
                )
            
            self.assertEqual(response, {})
        
        server.quit()
    
    def testFiveSequentialConnections(self):
        """5 sequential connections can be used to send messages."""
        
        for from_addr, to_addr in zip(self.addrs, reversed(self.addrs)):
            server = SMTP('localhost', 1025)

            response = server.sendmail(
                from_addr, [to_addr],
                'This is a test message\nSecond line.\nFinal line here.'
                )
            
            self.assertEqual(response, {})
        
            server.quit()
        
    def testUnicode(self):
        """Unicode characters are correctly received"""
        
        server = SMTP('localhost', 1025)
        
        response = server.sendmail(
            'ryu@example.jp', 'akira@example.jp',
            u'こんにちは彰、どのようにして、今日ですか？リュ'.encode('utf8')
            )
        
        self.assertEqual(response, {})
        
    def testWelcomeMessage(self):
        """On connecting the server sends a 220 response with a welcome message."""
        client = Telnet('localhost', 1025)
        self.assertEqual(client.read_some(), '220 test node.js SMTP server\r\n')
        client.close()
        
    def testIllegalHelo(self):
        """HELO takes a single argument."""
        
        client = Telnet('localhost', 1025)
        client.read_some()
        client.write('HELO')
        self.assertEqual(client.read_some(), '501 Syntax: HELO hostname\r\n')
        client.close()
    
    def testLegalHelo(self):
        """The server responds to a valid HELO command."""
        
        client = Telnet('localhost', 1025)
        client.read_some()
        client.write('HELO localhost')
        self.assertEqual(client.read_some(), '250 test Hello 127.0.0.1\r\n')
        client.close()
    
    def testIllegalNoop(self):
        """The NOOP command fails if any argument is passed."""
        
        client = Telnet('localhost', 1025)
        client.read_some()
        client.write('NOOP something else here')
        self.assertEqual(client.read_some(), '501 Syntax: NOOP\r\n')
        client.close()
    
    def testLegalNoop(self):
        """The NOOP command takes no arguments."""
        
        client = Telnet('localhost', 1025)
        client.read_some()
        client.write('NOOP')
        self.assertEqual(client.read_some(), '250 Ok\r\n')
        client.close()
        
    def testQuit(self):
        """The QUIT command doesn't care about arguments - the connection is
        closed regardless."""
        
        client = Telnet('localhost', 1025)
        client.read_some()
        client.write('QUIT')
        self.assertEqual(client.read_some(), '221 test closing connection\r\n')
        
        client = Telnet('localhost', 1025)
        client.read_some()
        client.write('QUIT See you later')
        self.assertEqual(client.read_some(), '221 test closing connection\r\n')
        
        
if __name__ == "__main__":
    unittest.main()