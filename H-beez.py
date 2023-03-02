import paramiko
import threading

# Define the host and port for the honeypot
HOST_KEY = paramiko.RSAKey.generate(2048)
HOST = '0.0.0.0'
PORT = 2222

# Define the handler for SSH client connections
class SSHHandler(paramiko.ServerInterface):

    def __init__(self):
        self.event = threading.Event()

    def check_auth_password(self, username, password):
        print(f'Attempted login with username {username} and password {password}')
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return 'password'

    def check_channel_request(self, kind, chanid):
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_shell_request(self, channel):
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

# Create the SSH server
server = paramiko.Transport((HOST, PORT))
server.add_server_key(HOST_KEY)
server.start_server(server=SSHHandler())

# Listen for incoming connections
while True:
    client, addr = server.accept()
    print(f'Connection from {addr[0]}:{addr[1]}')
    client.close()