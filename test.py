from functions import *
import pandas as pd

# Creating a dictionary with the misspelled and corrected words and stroing into dataframe
data = {
    'Misspelled Words': ['մամուշակագույն', 'ֆանաչ', 'թորցարկել', 'ապիտակ', 'աքթիվ'],
    'Correct Words': ['մանուշակագույն', 'կանաչ', 'փորձարկել', 'սպիտակ', 'ակտիվ']
}

df = pd.DataFrame(data)
print(df)


df['Expected_Corrections'] = df['Misspelled Words'].apply(lambda x: correction_automated(x))  # Apllying correction function over misspeled words

# Getting number of expected corrected words and dividing by the number total words to get the accuracy
num_correct = (df['Expected_Corrections'] == df['Correct Words']).sum()
accuracy = num_correct / len(df)

print("Accuracy: {:.2%}".format(accuracy)) 


