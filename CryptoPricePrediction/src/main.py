import dbController 
import pandas as pd

status = dbController.updateDB()

print(status)

df = dbController.readDB()
print(df.head())

print()

print(df.tail())

status = dbController.updateDB_forex()
print(status)
forex = dbController.readDB_forex()

print(forex)


print('success')

