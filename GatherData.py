import os
import sys
import requests
from bs4 import BeautifulSoup
import gzip
import lz4.frame
import io

import pandas as pd

MOBI_URL = 'https://www.mobibikes.ca/en/system-data'
MAX_NUMBER_OF_REQUESTS = 5
DATA_LIMIT = 100 # Limit set to 100 to gather all Mobi Data

class Google_Shared_Link:
    def __init__(self):
        self.shared_link = dict()

    def append(self, name, value):
        name = "_".join(name.split())
        if name == (None or ""):
            return
        
        value_split = value.split('d/')[1]
        value_google_shared_link = value_split.split('/')[0]

        self.shared_link[name] = value_google_shared_link

    def items(self):
        return self.shared_link.items()


def request_mobi_Data(data_limit):
    """
        To print 
            - HTML Parser was successful
            - The Month Year that was parsed
            - If parser failed for a month year then print failure
    """
    mobi_response = requests.get(MOBI_URL, timeout=10)
    if mobi_response.status_code != requests.codes.ok:
        print(f"Request to Mobi could not be made")
        return None
    print("Successful request to Mobi-system-data")

    mobi_parsed = BeautifulSoup(mobi_response.text, 'html.parser')

    mobi_div_container = mobi_parsed.find(attrs='FcwDynamicPageTextContent')
    mobi_a_refs = mobi_div_container.find_all('a')

    mobi_shared_google_links = Google_Shared_Link()
    data_limit_iterator = 0
    for a_ref in mobi_a_refs:
        if 'drive.google.com' not in a_ref.get('href'):
            if 'docs.google.com' not in a_ref.get('href'):
                continue

        mobi_shared_google_links.append(a_ref.string, a_ref.get('href'))

        data_limit_iterator += 1
        if data_limit_iterator == data_limit:
            break
    return mobi_shared_google_links


# https://stackoverflow.com/questions/38511444/python-download-files-from-google-drive-using-url
def download_file_from_google_drive(mobi_shared_links):
    URL = "https://docs.google.com/uc?export=download&confirm=1"

    session = requests.Session()

    for month, shared_link in mobi_shared_links.items():
        response = session.get(URL, params={"id": shared_link}, stream=True)
        token = get_confirm_token(response)

        if token:
            params = {"id": shared_link, "confirm": token}
            response = session.get(URL, params=params, stream=True)

        save_response_content(response, month)
        print(f"Completed download of date: {month}")

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith("download_warning"):
            return value

    return None

# FIX: Can specify what file type wanted
def save_response_content(response, destination):
    CHUNK_SIZE = 32768
    if not os.path.exists('Mobi_data_csv'):
        os.mkdir('Mobi_Data_csv')
    if not os.path.exists('Mobi_data_gzip'): # and file_type is a set to confirm file
        os.mkdir('Mobi_Data_gzip')
    if not os.path.exists('Mobi_data_lz4'):
        os.mkdir('Mobi_data_lz4')
    
    file_csv = open(f"Mobi_Data_csv/{destination}.csv", "wb")
    file_gzip = gzip.open(f"Mobi_Data_gzip/{destination}.gzip", "wb")
    file_l4z = lz4.frame.open(f"Mobi_Data_lz4/{destination}.lz4", "wb")

    for chunk in response.iter_content(CHUNK_SIZE):
        if chunk:  # filter out keep-alive new chunks
            file_gzip.write(chunk)
            file_csv.write(chunk)
            file_l4z.write(chunk)

    file_gzip.close()
    file_csv.close()
    file_l4z.close()

def test_data():
    df_csv = pd.read_csv('Mobi_Data_csv/June_2025.csv')
    df_gzip = pd.read_csv('Mobi_Data_gzip/June_2025.gzip', compression='gzip')

    print("Printing data from CSV file")
    print(df_csv)
    print("Printing data from gzip file")
    print(df_gzip)

    # chunk_size = 128 * 1024 * 1024
    with lz4.frame.open('Mobi_Data_lz4/June_2025.lz4', 'rb') as file:
        chunk_data = file.read()
    data_stream = io.StringIO(chunk_data.decode('utf-8'))
    df_lz4 = pd.read_csv(data_stream)

    print("Printing data from lz4 file")
    print(df_lz4)



def gather_data(data_limit=DATA_LIMIT):
    TIME_OUT_REQUESTS = 3
    number_of_requests = 0

    while number_of_requests <= TIME_OUT_REQUESTS:
        if number_of_requests >= MAX_NUMBER_OF_REQUESTS:
            print('Google drive shareable link could not be found')
            break

        mobi_shared_links = request_mobi_Data(data_limit)
        if mobi_shared_links:
            break

        requests_number += 1
    
    if not mobi_shared_links:
        return

    download_file_from_google_drive(mobi_shared_links)


if __name__ == '__main__':
    """
        To run
            python3 GatherData.py 1
        arg 1: an int
            Will grab from the top of the list in system data
    """
    if len(sys.argv) >= 2:
        data_limit = sys.argv[1] # Limit input for the amount of data that will be retrieved
        gather_data(data_limit) # Using the arg value given
    else:
        gather_data() # Using the default value (Default: 100 (Gather all data))