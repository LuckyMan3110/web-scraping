from bs4 import BeautifulSoup
import requests
import csv

header = ['name', 'url', 'title', 'city', 'country', 'com_url', 'facebook', 'linkedin', 'twitter', 'instagram']

url = "https://s23.a2zinc.net/clients/WPA/SZ2022/Public/Exhibitors.aspx?Index=All"
req = requests.get(url)

soup = BeautifulSoup(req.content, "html.parser")

div_element = soup.find("div",  class_="listTableBody")
table = div_element.find("table")
body = table.find("tbody")
result = body.find_all("tr")

with open('csv_file.csv', 'w', encoding="UTF8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    prefix = "https://s23.a2zinc.net/clients/WPA/SZ2022/Public/"
    for tr in result:
        data = tr.find("td", class_="companyName")
        url = data.find_all("a")
        print(data.text)
        print(url[0]["href"])
        csv_data = [data.text, prefix + url[0]["href"] ]
        writer.writerow(csv_data)

    
    


