import pandas as pd

def getColumn(df, columnName):
  return df.loc[:,[columnName]]