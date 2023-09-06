import sqlite3

def connect_to_database():
    # Connect to database. If it doesn't exist, sqlite3 automatically creates it
    database = sqlite3.connect("database.db")

    # Create database cursor
    cursor = database.cursor()

    # Check if the table exists. If it doesn't, create and populate it
    table_query = "SELECT name FROM sqlite_master WHERE type='table' AND name='questions'"

    output = cursor.execute(table_query).fetchall()

    if output == []:
        __populate_database(database)
    
    return database

def __populate_database(database: sqlite3.Connection):
    # Create database cursor
    cursor = database.cursor()

    # Create questions table
    cursor.execute("CREATE TABLE questions (question TEXT, option1 TEXT, option2 TEXT, option3 TEXT, option4 TEXT, answer TEXT)")
    database.commit()

    # Populate questions table
    cursor.execute("INSERT INTO questions (question, option1, option2, option3, option4, answer) VALUES ('Qual é a capital do Brasil?', 'São Paulo', 'Rio de Janeiro', 'Brasília', 'Manaus', 'Brasília')")
    cursor.execute("INSERT INTO questions (question, option1, option2, option3, option4, answer) VALUES ('Qual é a capital da Itália?', 'Roma', 'Paris', 'Lisboa', 'Londres', 'Roma')")
    cursor.execute("INSERT INTO questions (question, option1, option2, option3, option4, answer) VALUES ('Qual é a capital da Papua Nova Guiné?', 'Mount Hagen', 'Madang', 'Arawa', 'Port Moresby', 'Port Moresby')")
    database.commit()
    
def get_database_data(database: sqlite3.Connection):
    # Create database cursor
    cursor = database.cursor()

    # Define the queries
    questions_query = "SELECT * FROM questions"

    # Return the questions, options and answers
    question_data = cursor.execute(questions_query).fetchall()

    return question_data


