from bs4 import BeautifulSoup
import requests
import csv

with open('url_file.csv', 'r+', newline="") as csv_file:
    with open('info_file.csv', mode='w', newline="") as write_file:
        fieldnames = ['name','url','title','city','country','com_url','facebook','linkedin','twitter','instagram']
        writer = csv.DictWriter(write_file, fieldnames=fieldnames)
        writer.writeheader()

        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1

            target_url = row['url']
            page = requests.get(target_url)
            soup = BeautifulSoup(page.content, "html.parser")
            container = soup.find(id="eboothContainer")
            panel = container.find("div", class_="panel")
            panel_body = panel.find("div", class_="panel-body")
            title = panel_body.find("h1")
            body = panel_body.find("div", class_="BoothContactInfo pull-left")
            city = panel_body.find("span", class_="BoothContactCity")
            country = panel_body.find("span", class_="BoothContactCountry")
            url = panel_body.find("span", class_="BoothContactUrl")

            socialContainer = panel_body.find(id="ctl00_ContentPlaceHolder1_ctrlCustomField_Logos_dlCustomFieldList")
            socialUrls = socialContainer.find_all("span", class_="spCustomFieldIcon")

            dict = {}
            dict['name'] = row['name']
            dict['url'] = row['url']
            dict['title'] = title.text
            dict['city'] = city.text
            dict['country'] = country.text
            dict['com_url'] = url.text

            for item in socialUrls:
                social_url = item.find_all("a")
                if(social_url != []):
                    href = social_url[0]["href"]
                    if (href.count("www.facebook.com") > 0):
                        dict['facebook'] = href
                    else:
                        facebook = ""

                    if (href.count("www.linkedin.com") > 0):
                        dict['linkedin'] = href
                    else:
                        linkedin = ""

                    if (href.count("www.instagram.com") > 0):
                        dict['instagram'] = href
                    else:
                        instagram = ""

                    if (href.count("twitter.com") > 0):
                        dict['twitter'] = href
                    else:
                        twitter = ""

            print(dict)
            writer.writerow(dict)

            line_count += 1

        print(f'***Processed {line_count} lines.***')