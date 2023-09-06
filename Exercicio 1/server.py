import socket
import database as db

# Set host and port
HOST = '0.0.0.0'
PORT = 5001

def server_connect(local_host, port):
    # Get server socket instance and bind host and port to it as a tuple
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((local_host, port))

    # Configure simultaneous connections
    server_socket.listen(1)
    connection, address = server_socket.accept() # Blocking function
    print("Cliente conectado com endereço", str(address))

    return connection, address

def server_communicate(connection: socket.socket, database, address):
    # Initialize answer list
    answer_list = []

    # Get database questions
    question_data = db.get_database_data(database)

    # Get answer from client. Close connection in case of exception
    try:
        # Iterate over the questions and send them to client
        for data in question_data:
            question_options = f'''{data[0]}\nAlternativas:\n{data[1]}\n{data[2]}\n{data[3]}\n{data[4]}\n'''

            # Get the correct answer
            answer = data[5]

            # Send question and alternatives to the client
            connection.sendto(question_options.encode(), address)
            
            # Compare the answer and fill the answer sheet
            client_answer = connection.recv(1024).decode()
            if client_answer == answer:
                answer_list.append(True)
            else:
                answer_list.append(False)

        # Check answers and send results to client
        correct_answers = 0
        question_number = 1
        client_result = "\nAlternativas corretas: \n"

        for result in answer_list:
            if result:
                correct_answers += 1
                client_result += f"Questão {question_number}\n"
            
            question_number += 1

        # Append a message that the client expects to receive in order to close the connection
        client_result += f"Pontos: {correct_answers}\nObrigado por jogar!"
        connection.sendto(client_result.encode(), address)

        # Close the connection
        print("Encerrando conexão com o cliente.")
        connection.close()

    except Exception as e:
        # Print error and close the connection
        print(e)
        connection.close()

if __name__ == '__main__':
    # Initialize database
    print("Inicializando banco de dados...")
    database = db.connect_to_database()
    print("Banco de dados inicializado.")

    # Get socket connection from client
    connection, address = server_connect(HOST, PORT)

    # Start the quiz
    if connection and address:
        server_communicate(connection, database, address)
        