url1 = "https://batdongsan.com.vn"
url_sosanhnha = "https://sosanhnha.com"
url_dothi = "https://dothi.net"
url_alonhdat = "https://alonhadat.com.vn"
url_nhaphonet = "https://nhaphonet.vn/"

from csv import DictReader
import pandas as pd
import io
import csv 

df = pd.read_csv(r'D:\\OneDrive\\KiotViet\\Python_for_work\\KFinance\\CSV_crawl_data\\all_bds_final_clean.csv',usecols=['City','District','Ward','Street']).drop_duplicates()
csv_string = df.to_csv(index=False)
f = io.StringIO(csv_string)
dict_reader = DictReader(f)
city_district_mapping_raw = list(dict_reader)

# print(city_district_mapping)

# Đọc dữ liệu từ file CSV và chuyển đổi thành nested dictionary
def csv_to_nested_dict(csv_file):
    nested_dict = {}
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # print(row)
            city = row['City']
            district = row['District']
            ward = row['Ward']
            street = row['Street']
            if city not in nested_dict:
                nested_dict[city] = {}
            if district not in nested_dict[city]:
                nested_dict[city][district] = {}
            if ward not in nested_dict[city][district]:
                nested_dict[city][district][ward] = []
            nested_dict[city][district][ward].append(street)
    return nested_dict

# Đường dẫn tới file CSV
df_csv = pd.read_csv(r'D:\\OneDrive\\KiotViet\\Python_for_work\\KFinance\\CSV_crawl_data\\all_bds_final_clean.csv',usecols= ['City','District','Ward','Street'],encoding='utf-8').drop_duplicates()
df_csv.dropna().to_csv(r'D:\\OneDrive\\KiotViet\\Python_for_work\\KFinance\\CSV_crawl_data\\location_clean_new.csv', index=False, mode = 'w', encoding="utf-8")
csv_file_path = r'D:\\OneDrive\\KiotViet\\Python_for_work\\KFinance\\CSV_crawl_data\\location_clean_new.csv'

# Chuyển đổi từ file CSV thành nested dictionary
city_district_mapping = csv_to_nested_dict(csv_file_path)

# In ra nested dictionary
# print(nested_dict)
