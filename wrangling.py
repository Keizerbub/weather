from WeatherDataCollectionModule import AggregationDataset

ag=AggregationDataset()

input_folder=r"C:\Users\Regis Likassi\Documents\AIVANCITY\3e année\clinique IA\weather\test_echantillon"
output_folder=r"C:\Users\Regis Likassi\Documents\AIVANCITY\3e année\clinique IA\weather\test_resultat_echantillon"

ag.decompress_move_and_delete_zip(input_folder, output_folder)
