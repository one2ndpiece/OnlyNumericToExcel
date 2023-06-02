import streamlit as st
import pandas as pd
import re
import os
import logging

logging.basicConfig(level=logging.DEBUG)

# Then, in your functions or any part of the code you suspect is causing the issue:
logging.debug('Starting to run this part of the code...')



def extract_numbers(file):
    data = []

    try:
        for line in file:
            # Converting bytes to string
            line = line.decode('utf-8')
            # Finding all numbers including negative numbers
            numbers = re.findall(r'-?\d+\.?\d*', line)
            # Converting all found strings to floats or integers
            numbers = [float(num) if '.' in num else int(num) for num in numbers]
            data.append(numbers)
    except Exception as e:
        logging.error(f"Exception occurred in extract_numbers: {e}")
        raise

    return data

# Streamlit code
st.title('Number Extractor')

uploaded_file = st.file_uploader("Choose a TXT file", type="txt")
if uploaded_file is not None:
    file_details = {"FileName":uploaded_file.name,"FileType":uploaded_file.type,"FileSize":uploaded_file.size}
    st.write(file_details)

    try:
        data = extract_numbers(uploaded_file)
        df = pd.DataFrame(data)
        st.dataframe(df)
    except Exception as e:
        logging.error(f"Exception occurred when processing uploaded file: {e}")
        st.error("An error occurred when processing the uploaded file. Please check the log for more details.")

    if st.button('Save to Excel'):
        output_path = st.text_input('Enter output path', '')
        excel_file = st.text_input('Enter Excel file name', 'output.xlsx')
        if output_path and excel_file:  # only proceed if both output_path and excel_file are not empty
            try:
                full_path = os.path.join(output_path, excel_file)
                df.to_excel(full_path, index=False, header=False)
                st.success(f'Excel file saved as {full_path}')
            except Exception as e:
                logging.error(f"Exception occurred when saving DataFrame to Excel: {e}")
                st.error("An error occurred when saving the DataFrame to Excel. Please check the log for more details.")
# Your code here
logging.debug('Finished running this part of the code.')