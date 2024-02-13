from bs4 import BeautifulSoup as bs  # for HTML file manipulation
from urllib.request import urlopen as ur, Request as re  # for HTTP manipulation
import pandas as pd  # for data frame manipulation
import time as t  # for pauses
import json
import os
import gzip
import shutil
import re

################################################################
"""a class dedicated to the scrapping of the weather document"""
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
            i=0
            # Loop through the list of URLs
            for url in urls:
                # Open the URL in the browser
                driver.get(url)
                t.sleep(1)
                # Optionally, you can add a delay to give the page time to load
                # driver.implicitly_wait(1)  # Waits for 1 seconds (adjust as needed)
                #to have a traceback
                i=i+1
                if(i % 10)==0:
                    print(f"link number {i} opened")
                    
        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            # Close the browser window
            driver.quit()
            
            
            
################################################################
"a class dedicated to the handlng of the zipped folder and file"
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
        if type(input_folder) != list :
            all_files = self.get_all_files_in_directory(input_folder)
        else:
            all_files=input_folder
            
        # Initialize an empty DataFrame
        combined_df = pd.DataFrame()

        # Read each CSV file and concatenate into the combined DataFrame
        for file in all_files:
            df = pd.read_csv(file)
            combined_df = pd.concat([combined_df, df], ignore_index=True)

        # Write the combined DataFrame to a CSV file
        combined_df.to_csv(output_file, index=False)


    """getting year of dataset"""
    def extraire_valeurs_absolues(self,texte):
        # Utiliser une expression régulière pour trouver tous les nombres positifs dans le texte
        number = re.findall(r'\b\d+\.\d+|\b\d+\b', texte)
        
        # Convertir les chaînes de caractères en nombres (float) et prendre la valeur absolue
        absolute_v = [abs(float(number)) for number in number]
        
        #return the max of the number
        return max(absolute_v, default=0)

    
    """removing non-consitent datase below year<2000"""
    def delete_file(self,directory:bool,repertoire,year:int):
        
        if directory==True:
            # Récupérer la liste des fichiers dans le répertoire
            fichiers = os.listdir(repertoire)

            # Parcourir tous les fichiers du répertoire
            for fichier in fichiers:
                #file path
                chemin_fichier = os.path.join(repertoire, fichier)
                
                # Vérifier si le fichier existe et est un fichier régulier
                if os.path.isfile(chemin_fichier):
                    # Extraire les valeurs absolues des nombres dans le chemin du fichier
                    valeurs_absolues = self.extraire_valeurs_absolues(chemin_fichier)
                    
                    # Vérifier si la valeur absolue maximale est inférieure à 2000
                    if valeurs_absolues < year:
                        # Supprimer le fichier
                        os.remove(chemin_fichier)
                        print(f"file remove : {chemin_fichier}")
        
        
        elif directory ==True and type(repertoire)==list:
            
            for fichier in repertoire:         
                # Vérifier si le fichier existe et est un fichier régulier
                if os.path.isfile(fichier):
                    # Extraire les valeurs absolues des nombres dans le chemin du fichier
                    valeurs_absolues = self.extraire_valeurs_absolues(fichier)
                    
                    # Vérifier si la valeur absolue maximale est inférieure à 2000
                    if valeurs_absolues < 2000:
                        # Supprimer le fichier
                        os.remove(fichier)
                        print(f"file remove : {fichier}")
    
    
        elif directory == False:
            
            if os.path.isfile(repertoire):
                # Extraire les valeurs absolues des nombres dans le chemin du fichier
                valeurs_absolues = self.extraire_valeurs_absolues(repertoire)
                
                # Vérifier si la valeur absolue maximale est inférieure à 2000
                if valeurs_absolues < 2000:
                    # Supprimer le fichier
                    os.remove(repertoire)
                    print(f"file remove : {repertoire}")


    def decompress_move_and_delete_zip(self, input_zip_folder, output_folder):
            # Liste des fichiers zip dans le dossier
            zip_files = [f for f in os.listdir(input_zip_folder) if f.endswith('.gz')]
            
            # Créer le dossier 'final_departement'
            final_departement_folder = os.path.join(output_folder, 'final_departement')
            os.makedirs(final_departement_folder, exist_ok=True)
            
            # Dictionnaire pour stocker les DataFrames par préfixe de nom de fichier
            file_dict = {}
            
            # Parcourir chaque fichier zip
            for zip_file in zip_files:
                # Chemin complet du fichier zip
                zip_file_path = os.path.join(input_zip_folder, zip_file)
                
                # Extraire le contenu du fichier zip dans le dossier de sortie
                self.decompress_and_move(zip_file_path, output_folder)
                
                # Supprimer le fichier zip après extraction
                os.remove(zip_file_path)
                print(f"Zip file removed: {zip_file_path}")
                
            # Liste des fichiers CSV dans le dossier d'extraction
            extracted_files = [f for f in os.listdir(output_folder) if f.endswith('.csv')]
            
            # Parcourir chaque fichier CSV
            for csv_file in extracted_files:
                # Récupérer le préfixe du nom de fichier (4 ou 5 premiers caractères)
                prefix = csv_file[:5]
                
                # Vérifier si le préfixe existe déjà dans le dictionnaire
                if prefix in file_dict:
                    # Lire le fichier CSV et concaténer avec le DataFrame existant dans le dictionnaire
                    df = pd.read_csv(os.path.join(output_folder, csv_file))
                    file_dict[prefix] = pd.concat([file_dict[prefix], df], ignore_index=True)
                else:
                    # Ajouter le DataFrame dans le dictionnaire
                    file_dict[prefix] = pd.read_csv(os.path.join(output_folder, csv_file))
            
            # Écrire chaque DataFrame dans un fichier CSV séparé dans le dossier final_departement
            for prefix, df in file_dict.items():
                output_file_path = os.path.join(final_departement_folder, f"{prefix}_combined.csv")
                df.to_csv(output_file_path, index=False)
                print(f"Combined CSV file created: {output_file_path}")
##############################################################################################

