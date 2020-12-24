import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
from random import randint
from scraper_api import ScraperAPIClient
import requests


def attribute_cleaner(dirty_attribute):
    clean_attribute = " ".join(dirty_attribute.split())
    return clean_attribute


client = ScraperAPIClient('# Insert scraper api key here')
total_df = pd.DataFrame()

# Phase 1: Link extraction
links = []
counter = 0

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

for x in range(1, 54):
    if x % 3 != 0:
        main_web = client.get('https://www.lamudi.com.mx/mexico/huixquilucan/casa/for-sale/?page='+str(x))
        soup = BeautifulSoup(main_web.text, 'lxml')
        for i in soup.find_all('a', class_='ListingCell-moreInfo-button-v2_redesign'):
            if i['href'] not in links:
                links.append(i['href'])
            else:
                continue
    else:
        sleep(randint(1, 3))
        main_web = requests.get('https://www.lamudi.com.mx/mexico/huixquilucan/casa/for-sale/?page=' + str(x), headers=headers)
        soup = BeautifulSoup(main_web.text, 'lxml')
        for i in soup.find_all('a', class_='ListingCell-moreInfo-button-v2_redesign'):
            if i['href'] not in links:
                links.append(i['href'])
            else:
                continue
    print('Page ' + str(x) + ' links done.')

print("\n\n Link extraction done! Moving to link info extraction...\n\n")

# Phase 2: Info extraction
for link in links:
    if counter % 3 == 0:
        web = requests.get(link, headers=headers)
        soup = BeautifulSoup(web.text, 'lxml')
        try:
            price = int(soup.find('span', class_='Overview-main FirstPrice').get_text().split()[1].replace(",", ""))
        except:
            price = 'N/A'
        try:
            address = soup.find('span', class_='Header-title-address-text').get_text()
            address = attribute_cleaner(address)
        except:
            address = 'N/A'
        try:
            latitude = float(soup.find('div', id='js-developmentMap')['data-lat'])
        except:
            latitude = 'N/A'
        try:
            longitude = float(soup.find('div', id='js-developmentMap')['data-lng'])
        except:
            longitude = 'N/A'
        try:
            parking_spaces = soup.find('div', {"data-attr-name": "car_spaces"}).next_sibling.next_sibling.get_text()
            parking_spaces = int(attribute_cleaner(parking_spaces))
        except:
            parking_spaces = 'N/A'
        try:
            bedrooms = soup.find('div', {"data-attr-name": "bedrooms"}).next_sibling.next_sibling.get_text()
            bedrooms = int(attribute_cleaner(bedrooms))
        except:
            bedrooms = 'N/A'
        try:
            bathrooms = soup.find('div', {"data-attr-name": "bathrooms"}).next_sibling.next_sibling.get_text()
            bathrooms = float(attribute_cleaner(bathrooms))
        except:
            bathrooms = 'N/A'
        try:
            building_size = soup.find('div', {"data-attr-name": "building_size"}).next_sibling.next_sibling.get_text()
            building_size = int(attribute_cleaner(building_size))
        except:
            building_size = 'N/A'
        try:
            land_size = soup.find('div', {"data-attr-name": "land_size"}).next_sibling.next_sibling.get_text()
            land_size = float(attribute_cleaner(land_size))
        except:
            land_size = 'N/A'
        # Amenities
        amenities = []
        try:
            for i in soup.find_all('div', class_='columns medium-12 small-12 ViewMore-text-description'):
                for h in i.find_all('div', class_='ellipsis'):
                    amenities.append(attribute_cleaner(h.get_text()))
        except:
            continue
        counter += 1
    else:
        web = client.get(link)
        soup = BeautifulSoup(web.text, 'lxml')
        try:
            price = int(soup.find('span', class_='Overview-main FirstPrice').get_text().split()[1].replace(",", ""))
        except:
            price = 'N/A'
        try:
            address = soup.find('span', class_='Header-title-address-text').get_text()
            address = attribute_cleaner(address)
        except:
            address = 'N/A'
        try:
            latitude = float(soup.find('div', id='js-developmentMap')['data-lat'])
        except:
            latitude = 'N/A'
        try:
            longitude = float(soup.find('div', id='js-developmentMap')['data-lng'])
        except:
            longitude = 'N/A'
        try:
            parking_spaces = soup.find('div', {"data-attr-name": "car_spaces"}).next_sibling.next_sibling.get_text()
            parking_spaces = int(attribute_cleaner(parking_spaces))
        except:
            parking_spaces = 'N/A'
        try:
            bedrooms = soup.find('div', {"data-attr-name": "bedrooms"}).next_sibling.next_sibling.get_text()
            bedrooms = int(attribute_cleaner(bedrooms))
        except:
            bedrooms = 'N/A'
        try:
            bathrooms = soup.find('div', {"data-attr-name": "bathrooms"}).next_sibling.next_sibling.get_text()
            bathrooms = float(attribute_cleaner(bathrooms))
        except:
            bathrooms = 'N/A'
        try:
            building_size = soup.find('div', {"data-attr-name": "building_size"}).next_sibling.next_sibling.get_text()
            building_size = int(attribute_cleaner(building_size))
        except:
            building_size = 'N/A'
        try:
            land_size = soup.find('div', {"data-attr-name": "land_size"}).next_sibling.next_sibling.get_text()
            land_size = float(attribute_cleaner(land_size))
        except:
            land_size = 'N/A'

        # Amenities
        amenities = []
        try:
            for i in soup.find_all('div', class_='columns medium-12 small-12 ViewMore-text-description'):
                for h in i.find_all('div', class_='ellipsis'):
                    amenities.append(attribute_cleaner(h.get_text()))
        except:
            continue
        counter += 1

    data = {"Address": address, "Latitude": latitude, "Longitude": longitude, "Price": price,
            "Parking_Spaces": parking_spaces, "Bedrooms": bedrooms, "Bathrooms": bathrooms,
            "Building_Size": building_size, "Land_Size": land_size}

    df = pd.DataFrame(data, index=[0])

    for i in amenities:
        if i not in df.columns:
            df[str(i)] = 1
        else:
            continue

    total_df = pd.concat([total_df, df], axis=0, ignore_index=True)
    print("Link #" + str(counter) + " done!")

total_df.to_csv('real_estate_data.csv', index=False)
