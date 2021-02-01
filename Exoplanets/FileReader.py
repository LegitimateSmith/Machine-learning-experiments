import pandas as pd #Pandas makes reading csv files happpy again :)
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns #Not 100% sure what this one does

pd.set_option('display.max_columns', None)

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

#I just stole the stuff above off some pandas tutorial so I'm not sure why they're needed but I don't want to break anything by taking them out


df = pd.read_csv("C:/Users/smith/OneDrive/Documents/Python Code/PHYS379/ExoplanetsTable.csv", error_bad_lines=False)

#This creates a data-frame (special pandas thingy) which is essentially the entire table as an array
#The errors thing lets the code skip over any row that is causing an error, so if the size of the data frame isn't the same as the table, then it is triggering

size = df.shape
print(size, size[0])

#size is a list of two values, number of columns and number of rows

print(df.head(2))

#head gets the top n rows, not sure where we'd use that but thought it might help

i = 0

while (i < size[1]):
    print(df.iloc[0,i])
    i+=1

#This just prints every item in the first row, iloc locates a certain box.
#I saw something on a pandas tutorial about using it to find all the empty boxes but I haven't got that here
