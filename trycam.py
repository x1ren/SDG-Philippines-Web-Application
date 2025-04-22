import camelot
import os
import pandas as pd


tables = camelot.read_pdf(r"C:\Users\Iben\PROJECTSSS\sdg project\sdgdata.pdf", pages="1", flavor="lattice")

df = tables[0].df
print(df.head(10))
for index, row in df.iterrows():
    print(row.tolist())