import csv
import requests
from bs4 import BeautifulSoup

URL = 'https://calendar.smmplanner.com/'
months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sen', 'oct', 'nov', 'dec']


def parse():
    data = {}
    for month in months:
        month_data_list = []
        try:
            print(f'Starting go to this page: {URL}...')
            response = requests.get(URL + month)
            soup = BeautifulSoup(response.text, 'lxml')
            try:
                print(f'Start parsing this page: {URL}')
                events_list = soup.find('div', class_='t-container').find_all('div',
                                                                              class_='t513__row t-row t-clear')
                for event in events_list:
                    event_date_and_name = event.text.replace('→', '')
                    event_url = event.find('a').attrs['href']
                    all_event_info = event_date_and_name + event_url
                    all_event_info = all_event_info.split('  ')[1:]
                    month_data_list.append(all_event_info)
                data[month] = month_data_list
            except Exception:
                print('Parsing was stopped something went wrong try again!')
        except Exception:
            print(f'{URL} incorrect please check url and try again!')
    return data

if __name__ == '__main__':
    data = parse()
    try:
        print('Starting creat events csv files')
        for event_date, event_data in data.items():
            with open(f'events_{event_date}.csv', 'w') as events_file:
                writer = csv.writer(events_file)
                writer.writerows(event_data)
    except Exception:
        print('Something went wrong try again!')