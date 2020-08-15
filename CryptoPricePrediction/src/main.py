import dbController 
import pandas as pd

status = dbController.updateDB()

print(status)

df = dbController.readDB()

print(df.head())

print()

print(df.tail())

print("success")
