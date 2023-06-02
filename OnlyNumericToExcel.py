import streamlit as st
import pandas as pd
import re
import os

def extract_numbers(file):
    data = []

    for line in file:
        # Converting bytes to string
        line = line.decode('utf-8')
        # Finding all numbers including negative numbers
        numbers = re.findall(r'-?\d+\.?\d*', line)
        # Converting all found strings to floats or integers
        numbers = [float(num) if '.' in num else int(num) for num in numbers]
        data.append(numbers)

    return data

# Streamlit code
st.title('Number Extractor')

uploaded_file = st.file_uploader("Choose a TXT file", type="txt")
if uploaded_file is not None:
    file_details = {"FileName":uploaded_file.name,"FileType":uploaded_file.type,"FileSize":uploaded_file.size}
    st.write(file_details)

    data = extract_numbers(uploaded_file)
    df = pd.DataFrame(data)

    st.dataframe(df)

    if st.button('Save to Excel'):
        output_path = st.text_input('Enter output path', '')
        excel_file = st.text_input('Enter Excel file name', 'output.xlsx')
        full_path = os.path.join(output_path, excel_file)
        df.to_excel(full_path, index=False, header=False)
        st.success(f'Excel file saved as {full_path}')
