import re
import pandas as pd

def extract_numbers(file_name):
    data = []

    with open("sample2.txt", 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            # Finding all numbers including negative numbers
            numbers = re.findall(r'-?\d+\.?\d*', line)
            # Converting all found strings to floats or integers
            numbers = [float(num) if '.' in num else int(num) for num in numbers]
            data.append(numbers)

    return data

# Replace with your text file name
file_name = 'your_text_file.txt'
data = extract_numbers(file_name)

# Creating a pandas DataFrame from the list of lists
df = pd.DataFrame(data)

# Writing the DataFrame to an Excel file
df.to_excel('output2.xlsx', index=False, header=False)