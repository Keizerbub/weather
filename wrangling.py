from WeatherDataCollectionModule import AggregationDataset

ag=AggregationDataset()

#folder containing our zipped file
input_folder=r"C:\Users\Regis Likassi\Documents\AIVANCITY\3e année\clinique IA\weather\test_echantillon"

#final folder in wich you will have the final_departement generated in
output_folder=r"C:\Users\Regis Likassi\Documents\AIVANCITY\3e année\clinique IA\weather\test_resultat_echantillon"

#the function to decompress and aggregate all file by departement  while removing the original file to not have a storage problem
ag.decompress_move_and_delete_zip(input_folder, output_folder)
