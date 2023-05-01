import pandas as pd
import numpy as np 
df = pd.read_json('wine.json',encoding='utf-8')
df.info()
pd.DataFrame.to_csv(df,'wine.csv')