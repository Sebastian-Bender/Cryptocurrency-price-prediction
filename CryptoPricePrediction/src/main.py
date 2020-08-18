import dbController 
import pandas as pd


def update_database():
    status = dbController.updateDB()
    print(status)

    status = dbController.updateDB_forex()
    print(status)

def read_database():
    df = dbController.readDB()
    print(df)
    
    forex = dbController.readDB_forex()
    print(forex)

if __name__ == '__main__':
    print('1: Update Database')
    print('2: Read Database')
    print('3: Update and Read Database')

    userInput = input('Enter: ')
    if userInput == '1':
        update_database()
    elif userInput == '2':
        read_database()
    elif userInput == '3':
        update_database()
        read_database()




