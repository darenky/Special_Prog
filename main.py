from datetime import datetime
import os
import pandas as pd
import re
import requests

# Dictionary for changing regioun indexes used on website to NOAA indexes
NOAAIndex = {
        1:24,
        2:25,
        3:5,
        4:6,
        5:27,
        6:23,
        7:26,
        8:7,
        9:11,
        10:13,
        11:14,
        12:15,
        13:16,
        14:17,
        15:18,
        16:19,
        17:21,
        18:22,
        19:8,
        20:9,
        21:10,
        22:1,
        23:3,
        24:2,
        25:4, 
        26:12, # for Kiev
        27:20 # for Sevastopol
}

save_dir = "files"  # Directory where files will be stored

#Download data from website + data cleaning 
def download_data(region_index, save_dir):
    if region_index not in NOAAIndex:
        print("Invalid region index.")
        return None

    noaa_index = NOAAIndex[region_index]
    url = f"https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?provinceID={noaa_index}&country=UKR&yearlyTag=Weekly&type=Mean&TagCropland=land&year1=1982&year2=2023"
    response = requests.get(url)

    if response.status_code == 200:  # Successful request 
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M")
        filename = os.path.join(save_dir, f"file_{formatted_datetime}.csv")

        with open(filename, 'wb') as file:   # + some data cleaning
            content = response.text.replace("</pre></tt>", "")
            content = content.replace("<tt><pre>", "")
            content = content.replace("<br>", "")
            content = content.replace(" VHI", "VHI")
            content = content.replace(" SMN", "SMN")
            content = content.replace("weeklyfor", "weekly for")
            content = re.sub(r',\n', '\n', content)  # Remove trailing commas

            file.write(content.encode('utf-8'))

        print(f"The file {filename} has been downloaded and saved")
        return filename
    else:
        print("Failed to download the file")
        return None

for i in range(1,28):
    download_data(i,save_dir)

region_index = 1  # Desired region index

downloaded_filename = download_data(region_index, save_dir)

headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI']
df = pd.read_csv(downloaded_filename, header=1, names=headers)
df = df[df['SMN'] != -1.0]  # Delete rows that contain "-1"

df.to_csv(downloaded_filename, index=False)  # Need it to save previous change in file itself 

def extremums_vhi(df, year: int):  # Find extremums for the specific year
    year_str = str(year)
    max_vhi = df.loc[df['Year'].astype(str) == year_str, 'VHI'].max()
    min_vhi = df.loc[df['Year'].astype(str) == year_str, 'VHI'].min()
    return max_vhi, min_vhi

print(extremums_vhi(df,1995))

def extreme_drought():  # Get info about extreme droughts for the entire time
  return  df[(df.VHI <= 15)]

print(extreme_drought())

def moderate_drought():  # Get info about moderate droughts for the entire time
  return  df[(df.VHI > 15)&(df.VHI <= 35)]

print(moderate_drought())