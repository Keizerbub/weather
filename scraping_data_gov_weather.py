from WeatherDataCollectionModule import Scraping as sc
from WeatherDataCollectionModule import AggregationDataset as ag
import time 

################################################################
"""part1: Scraping"""
#-stocking links
#temp_links=[]

#for i in range(1,250):
    #--url of page to get weather API results
#    url=f"https://www.data.gouv.fr/api/2/datasets/6569b4473bedf2e7abad3b72/resources/?page={i}&page_size=6&type=main&q="

    #--gettinks links
#    scrap=sc(url,info=False)
#    links=scrap.get_links()
#    temp_links.extend(links)
    

"""part2: downloading zipped folder"""
#-opening links to download it
#url="https://meteo.data.gouv.fr/datasets/6569b4473bedf2e7abad3b72"
#scrap=sc(url,info=False)
#scrap.open_url(temp_links)

################################################################
"""part3:gathering all csv in one file"""
#--paths
#---folder where are stock our zipped folder
repository=r"C:\Users\Regis Likassi\Documents\AIVANCITY\3e année\clinique IA\weather\zipped_folder"
#---folder in which we stock our csv
out_directory=r"C:\Users\Regis Likassi\Documents\AIVANCITY\3e année\clinique IA\weather\wetather_csv"
#---the final folder to stock our final csv
final_directory=r"C:\Users\Regis Likassi\Documents\AIVANCITY\3e année\clinique IA\weather"

#-instanciation
folder=ag()
#--getting all file of zipped folder
folder_name=folder.get_all_files_in_directory(directory=repository)
print('\n---success::1---')

#--getting all file of zipped folder
start_time = time.time()
for file in folder_name:
    folder.decompress_and_move(file,out_directory)
    if time.time() - start_time >= 5:
        current_time = time.strftime("%H:%M:%S", time.localtime())
        print(f"Temps actuel : {current_time}")
        start_time = time.time()
print('\n---success::2---')

#--combining all file into 1
folder.combine_csv_files(input_folder=folder_name,output_file=final_directory)
print('\n---success::3---')