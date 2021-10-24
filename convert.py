import pandas as pd
import csv

with open('dviz_data2.csv', 'w', encoding='utf-8') as file:
    writer = csv.writer(file)
    header = ['Name', 'Price', 'VIN', 'Vehicle Summary', 'Top Features and Specs']
    writer.writerow(header)


data = ['Car', 'Price', '1234hnfh', ['black', 'blue', 'green'], ['It can fly']]

with open('dviz_data.csv2', 'a', encoding='utf-8', newline='') as file:
    field_names = ['Name', 'Price', 'VIN']
    writer = csv.writer(file)
    writer.writerow(data)

read_file = pd.read_csv('dviz_data2.csv')
read_file.to_excel('dviz_data2.xlsx', index=None, header=True)



# data = [car_name.text, car_price.text, vin_number.text, vehicle_summary_list, top_features_and_specs_list]
#                 with open('dviz_data.csv', 'a', encoding='utf-8', newline='') as file:
#                     writer = csv.writer(file)
                    # writer.writerow(data)