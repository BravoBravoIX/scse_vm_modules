import socket
import logging
import time

class CommModule:
    def __init__(self, protocol, port, server_ip):
        """
        Initialize the communication module with the specified protocol, port, and server IP.
        """
        self.protocol = protocol
        self.port = port
        self.server_ip = server_ip
        self.sock = None
        self.setup_logging()
    
    def setup_logging(self):
        """
        Set up the logging configuration for the module.
        """
        logging.basicConfig(filename='comm_module.log', level=logging.INFO,
                            format='%(asctime)s %(levelname)s %(message)s')
    
    def create_socket(self):
        """
        Create a socket based on the specified protocol (TCP/UDP) and connect to the server.
        """
        try:
            if self.protocol == 'TCP':
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((self.server_ip, self.port))
            elif self.protocol == 'UDP':
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            logging.info(f'Socket created using {self.protocol} protocol')
        except Exception as e:
            logging.error(f'Error creating socket: {e}')
            self.sock = None
    
    def send_data(self, data):
        """
        Send data to the server through the created socket.
        """
        try:
            if self.sock:
                if self.protocol == 'TCP':
                    self.sock.sendall(data.encode())
                elif self.protocol == 'UDP':
                    self.sock.sendto(data.encode(), (self.server_ip, self.port))
                logging.info(f'Data sent: {data}')
            else:
                logging.error('Socket not created')
        except Exception as e:
            logging.error(f'Error sending data: {e}')
    
    def receive_data(self):
        """
        Receive data from the server through the created socket.
        """
        try:
            if self.sock:
                if self.protocol == 'TCP':
                    data = self.sock.recv(1024).decode()
                elif self.protocol == 'UDP':
                    data, _ = self.sock.recvfrom(1024)
                    data = data.decode()
                logging.info(f'Data received: {data}')
                return data
            else:
                logging.error('Socket not created')
                return None
        except Exception as e:
            logging.error(f'Error receiving data: {e}')
            return None
    
    def close_socket(self):
        """
        Close the socket connection.
        """
        if self.sock:
            self.sock.close()
            logging.info('Socket closed')

# Example usage:
if __name__ == "__main__":
    # Create an instance of the communication module with specified settings
    comm_module = CommModule(protocol='TCP', port=8080, server_ip='192.168.1.1')
    
    # Create a socket connection
    comm_module.create_socket()
    
    # Send test data to the server
    comm_module.send_data('Test data')
    
    # Receive data from the server
    received_data = comm_module.receive_data()
    print(f'Received data: {received_data}')
    
    # Close the socket connection
    comm_module.close_socket()
