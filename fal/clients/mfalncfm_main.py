# import paramiko
# import sshtunnel
import mysql.connector

import configparser
import sys
from contextlib import closing

config = configparser.ConfigParser()
config.read("config-secret.ini")


class Client:

    # TODO: tunneling from here does not work and I can't figure out why!
    #      workaround for now is set up the port forwarding manually with PuTTY
    #      https://www.namecheap.com/support/knowledgebase/article.aspx/1249/89/how-to-remotely-connect-to-a-mysql-database-located-on-our-shared-server
    '''
    with sshtunnel.SSHTunnelForwarder(
        (config['namecheap-ssh']['hostname'],
         int(config['namecheap-ssh']['port'])),
        ssh_username=config['namecheap-ssh']['username'],
        ssh_pkey='generic.key',
        ssh_private_key_password=config['namecheap-ssh']['password'],
        remote_bind_address=('127.0.0.1', 3306),
        local_bind_address=('0.0.0.0', 3306)
    ) as tunnel:
        conn = mysql.connector.connect(
            user=config['mfalncfm_main']['username'],
            password=config['mfalncfm_main']['password'],
            database="mfalncfm_main",
            port=tunnel.local_bind_port,
        )
    '''

    def __enter__(self):
        try:
            self.conn = mysql.connector.connect(
                user=config['mfalncfm_main']['username'],
                password=config['mfalncfm_main']['password'],
                database="mfalncfm_main"
            )
        except mysql.connector.errors.DatabaseError as identifier:
            print('Error connecting to MySQL. Did you forget to set up port forwarding? \n'
                  'https: // www.namecheap.com/support/knowledgebase/article.aspx/1249/89/how-to-remotely-connect-to-a-mysql-database-located-on-our-shared-server\n'
                  f'{identifier}')
            sys.exit(1)

        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, type, value, traceback):
        self.cursor.close()
        self.conn.close()
