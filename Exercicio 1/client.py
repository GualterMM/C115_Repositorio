import socket

# Set host and port
HOST = '0.0.0.0'
PORT = 5001

def client_connect(host, port):

    # Create client socket and connect to server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"Conectado com o servidor no endereço {host}:{port}")

    try:
        # Receive questions from the server
        while True:
            question = client_socket.recv(1024).decode()
            print(question)
            
            # Break the loop if the message signals a game over  
            if "Obrigado por jogar!" in question:
                break

            # Send answer back to the server
            answer = input("Resposta: ")
            client_socket.sendto(answer.encode(), (host, port))

    # Close connection in case of forced interruption or exception
    except KeyboardInterrupt:
        client_socket.close()
        print("Conexão encerrada pelo cliente.")
    except Exception as e:
        client_socket.close()
        print("Erro:", e)
        
    # Close connection normally after loop
    client_socket.close()
    print("Conexão encerrada pelo servidor.")

if __name__ == "__main__":
    print(socket.gethostbyaddr(socket.gethostname()))
    # Connect to server and start the game
    client_connect(HOST, PORT)
