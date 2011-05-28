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
        
    def testUnknownCommand(self):
        """Unknown commands are ignored and the client informed."""
        
        client = Telnet('localhost', 1025)
        client.read_some()
        client.write('EHLO')
        self.assertEqual(client.read_some(), 
                         '502 Error: command "EHLO" not implemented\r\n')
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
        
    def testMultipleHelo(self):
        """Only a single HELO command is allowed per connection."""
        
        client = Telnet('localhost', 1025)
        client.read_some()
        client.write('HELO localhost')
        self.assertEqual(client.read_some(), '250 test Hello 127.0.0.1\r\n')
        client.write('HELO localhost')
        self.assertEqual(client.read_some(), '503 Duplicate HELO/EHLO\r\n')
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
        client.close()
        
    def testIllegalRset(self):
        """The RSET command fails if any argument is passed."""
        
        client = Telnet('localhost', 1025)
        client.read_some()
        client.write('RSET now')
        self.assertEqual(client.read_some(), '501 Syntax: RSET\r\n')
        client.close()
        
    def testLegalRset(self):
        """The RSET command takes no arguments."""
        
        client = Telnet('localhost', 1025)
        client.read_some()
        client.write('RSET')
        self.assertEqual(client.read_some(), '250 Ok\r\n')
        client.close()
        
    def testMailNoFrom(self):
        """The MAIL command requires FROM: to follow it."""
        
        client = Telnet('localhost', 1025)
        client.read_some()
        client.write('MAIL')
        self.assertEqual(client.read_some(),
                         '501 Syntax: MAIL FROM:<address>\r\n')
        client.close()
    
    def testMailInvalidFrom(self):
        """The MAIL command requires FROM: to contain an email address."""
        
        client = Telnet('localhost', 1025)
        client.read_some()
        client.write('MAIL FROM:')
        self.assertEqual(client.read_some(),
                         '501 Syntax: MAIL FROM:<address>\r\n')
        client.close()
    
    def testMailFromParse(self):
        """The MAIL command will extract the email address from the FROM:."""
    
        client = Telnet('localhost', 1025)
        client.read_some()
        client.write('MAIL FROM:<person@example.com>')
        self.assertEqual(client.read_some(), '250 Ok\r\n')
        client.close()
        
    def testMailFromParse(self):
        """The MAIL command handles empty addresses"""
    
        client = Telnet('localhost', 1025)
        client.read_some()
        client.write('MAIL FROM:<>')
        self.assertEqual(client.read_some(), '250 Ok\r\n')
        client.close()
    
    def testDuplicateMailCommand(self):
        """Nested MAIL commands are not allowed."""
        
        client = Telnet('localhost', 1025)
        client.read_some()
        client.write('MAIL FROM:<me@example.com>')
        self.assertEqual(client.read_some(), '250 Ok\r\n')
        client.write('MAIL FROM:<me@example.com>')
        self.assertEqual(client.read_some(), '503 Error: nested MAIL command\r\n')
        client.close()
        
    def testRcptWithoutMail(self):
        """The RCPT command must be preceded by the MAIL command."""
        
        client = Telnet('localhost', 1025)
        client.read_some()
        client.write('RCPT TO:<me@example.com>')
        self.assertEqual(client.read_some(), '503 Error: need MAIL command\r\n')
        client.close()
        
    def testRcptWithoutTo(self):
        """The RCPT command must contain TO:<address> as the argument."""
        
        client = Telnet('localhost', 1025)
        client.read_some()
        client.write('MAIL FROM:<you@example.com>')
        self.assertEqual(client.read_some(), '250 Ok\r\n')
        client.write('RCPT')
        self.assertEqual(client.read_some(), '501 Syntax: RCPT TO: <address>\r\n')
        client.close()
    
    def testRcptEmptyTo(self):
        """The RCPT command cannot have an empty TO:."""
        
        client = Telnet('localhost', 1025)
        client.read_some()
        client.write('MAIL FROM:<you@example.com>')
        self.assertEqual(client.read_some(), '250 Ok\r\n')
        client.write('RCPT TO:')
        self.assertEqual(client.read_some(), '501 Syntax: RCPT TO: <address>\r\n')
        client.close()
        
    def testMultipleRcpts(self):
        """Multiple RCPT commands can be issued to add recipients."""
        
        client = Telnet('localhost', 1025)
        client.read_some()
        client.write('MAIL FROM:<you@example.com>')
        self.assertEqual(client.read_some(), '250 Ok\r\n')
        
        for rcpt in self.addrs:
            client.write('RCPT TO:<%s>' % rcpt)
            self.assertEqual(client.read_some(), '250 Ok\r\n')
        client.close()
    
    def testDataWithoutRcpt(self):
        """The DATA command must be preceded by the RCPT TO: command."""
        
        client = Telnet('localhost', 1025)
        client.read_some()
        client.write('DATA')
        self.assertEqual(client.read_some(), '503 Error: need RCPT command\r\n')
        client.close()
    
    def testDataResponse(self):
        """The DATA instructs the client to end the message with <CR><LF>.<CR><LF>."""
        
        client = Telnet('localhost', 1025)
        client.read_some()
        client.write('MAIL FROM:<you@example.com>')
        self.assertEqual(client.read_some(), '250 Ok\r\n')
        client.write('RCPT TO:<me@example.com>')
        self.assertEqual(client.read_some(), '250 Ok\r\n')
        client.write('DATA')
        self.assertEqual(client.read_some(),
                         '354 End data with <CR><LF>.<CR><LF>\r\n')
        client.close()
    
    def testDataArgument(self):
        """The DATA command does not take any arguments."""
        
        client = Telnet('localhost', 1025)
        client.read_some()
        client.write('MAIL FROM:<you@example.com>')
        self.assertEqual(client.read_some(), '250 Ok\r\n')
        client.write('RCPT TO:<me@example.com>')
        self.assertEqual(client.read_some(), '250 Ok\r\n')
        client.write('DATA some data here')
        self.assertEqual(client.read_some(), '501 Syntax: DATA\r\n')
        client.close()
        
if __name__ == "__main__":
    unittest.main()