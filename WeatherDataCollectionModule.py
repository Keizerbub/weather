from bs4 import BeautifulSoup as bs  # for HTML file manipulation
from urllib.request import urlopen as ur, Request as re  # for HTTP manipulation
import pandas as pd  # for data frame manipulation
import time as t  # for pauses
import json
from selenium import webdriver
import os
import gzip
import shutil

class Scraping:
    def __init__(self, url, info: bool):
        self.url = url
        self.info = info

    """Getting links from the government API function"""
    def get_links(self):
        if self.info:
            print("---Accessing the URL---")
            page = re(self.url, headers={"User-agent": "Mozilla/5.0"})
            html = ur(page)
            soup = bs(html)

            # Getting API results
            print("---\nGetting API results---")
            search = soup.find_all("p")
            print("---Success: Step 1---")

            # Transforming HTML to text, then into JSON format
            print("\nSecond part")
            print("---Transforming into text---")
            text = search[0].text
            text = json.loads(text)
            print("---Success: Step 2---")

            # Navigating our JSON
            print("\nThird part")
            print("---Data---")
            json_data = text['data']
            print("---Success: Step 3---")

            # Final step: getting links
            print("\nFourth part")
            print("---Getting links---")

            # List to keep results
            result = []

            # Adding found links to the result
            for i in json_data:
                element = i['url']
                result.append(element)

            # Returning result
            print("---Success: Step 4---\n")
            return result

        else:
            page = re(self.url, headers={"User-agent": "Mozilla/5.0"})
            html = ur(page)
            soup = bs(html)
            search = soup.find_all("p")
            text = search[0].text
            text = json.loads(text)
            json_data = text['data']
            result = []
            for i in json_data:
                element = i['url']
                result.append(element)
            print("---Success: True---\n")
            return result

    """Open links function"""
    def open_url(self, urls):
        # Initialize the WebDriver (assuming you are using Chrome)
        driver = webdriver.Chrome()
        try:
            # Loop through the list of URLs
            for url in urls:
                # Open the URL in the browser
                driver.get(url)
                t.sleep(1)
                # Optionally, you can add a delay to give the page time to load
                # driver.implicitly_wait(10)  # Waits for 10 seconds (adjust as needed)

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            # Close the browser window
            driver.quit()



class AggregationDataset:
    def __init__(self):
        pass

    """Get the names of all files in the folder"""
    def get_all_files_in_directory(self, directory):
        all_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                all_files.append(os.path.join(root, file))
        return all_files

    """Find the file and move it to another directory"""
    def decompress_and_move(self, input_gz_file, output_folder):
        with gzip.open(input_gz_file, 'rb') as f_in:
            # Get the input file name without the .gz extension
            base_filename = os.path.basename(input_gz_file)
            output_file = os.path.join(output_folder, os.path.splitext(base_filename)[0])

            with open(output_file, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

    """Merge all CSV files into a single CSV file"""
    def combine_csv_files(self, input_folder, output_file):
        all_files = self.get_all_files_in_directory(input_folder)
        # Initialize an empty DataFrame
        combined_df = pd.DataFrame()

        # Read each CSV file and concatenate into the combined DataFrame
        for file in all_files:
            df = pd.read_csv(file)
            combined_df = pd.concat([combined_df, df], ignore_index=True)

        # Write the combined DataFrame to a CSV file
        combined_df.to_csv(output_file, index=False)
