import streamlit as st
import pandas as pd
import re
import os
import logging

logging.basicConfig(level=logging.DEBUG)

logging.debug('Starting to run the script...')

def extract_numbers(file):
    data = []

    try:
        for line in file:
            logging.debug('Decoding line...')
            line = line.decode('utf-8')

            logging.debug('Finding numbers in line...')
            numbers = re.findall(r'-?\d+\.?\d*', line)

            logging.debug('Converting numbers...')
            numbers = [float(num) if '.' in num else int(num) for num in numbers]

            logging.debug('Appending numbers to data...')
            data.append(numbers)
    except Exception as e:
        logging.error(f"Exception occurred in extract_numbers: {e}")
        raise

    return data

logging.debug('Starting Streamlit code...')

st.title('Number Extractor')

uploaded_file = st.file_uploader("Choose a TXT file", type="txt")
if uploaded_file is not None:
    file_details = {"FileName":uploaded_file.name,"FileType":uploaded_file.type,"FileSize":uploaded_file.size}
    st.write(file_details)

    try:
        logging.debug('Calling extract_numbers...')
        data = extract_numbers(uploaded_file)

        logging.debug('Creating DataFrame...')
        df = pd.DataFrame(data)

        logging.debug('Displaying DataFrame...')
        st.dataframe(df)
    except Exception as e:
        logging.error(f"Exception occurred when processing uploaded file: {e}")
        st.error("An error occurred when processing the uploaded file. Please check the log for more details.")

    output_path = st.text_input('Enter output path', '')
    excel_file = st.text_input('Enter Excel file name', 'output.xlsx')
    
    if st.button('Save to Excel') and output_path and excel_file:
        try:
            logging.debug('Joining paths...')
            full_path = os.path.join(output_path, excel_file)

            logging.debug('Saving DataFrame to Excel...')
            df.to_excel(full_path, index=False, header=False)

            logging.debug('Excel file saved.')
            st.success(f'Excel file saved as {full_path}')
        except Exception as e:
            logging.error(f"Exception occurred when saving DataFrame to Excel: {e}")
            st.error("An error occurred when saving the DataFrame to Excel. Please check the log for more details.")

logging.debug('Finished running the script.')
