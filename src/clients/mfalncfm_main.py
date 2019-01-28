#import paramiko
#import sshtunnel
import mysql.connector

import configparser
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
        self.conn = mysql.connector.connect(
            user=config['mfalncfm_main']['username'],
            password=config['mfalncfm_main']['password'],
            database="mfalncfm_main"
        )
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, type, value, traceback):
        self.cursor.close()
        self.conn.close()
