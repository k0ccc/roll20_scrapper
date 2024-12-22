import requests
from urllib.parse import urlparse, parse_qs
import logging
import re
import base64
import json
import csv
import datetime

def timestamp_to_datetime(timestamp) -> str:
  dt = datetime.datetime.fromtimestamp(timestamp / 1000)
  return dt.strftime("%Y-%m-%d %H:%M:%S")

def parse_url(link):
  try:
      parsed_url = urlparse(link)
      if not parsed_url:
          return None, None, None

      name_of_campaign = parsed_url.path[23:-1]

      query = parse_qs(parsed_url.query)
      pages_count = int(query["p"][0])

      return name_of_campaign, pages_count

  except Exception as e:
      logging.error(f"Ошибка: {e}")
      return None, None, None

def parseHTML(name_of_campaign, pages_count, cookie):
    headers = {
        "Cookie": cookie,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0"
    }

    response = requests.get('https://app.roll20.net/campaigns/chatarchive/' + name_of_campaign + '/?p='+ str(pages_count) +'&onePage=&hidewhispers=&hiderollresults=', headers=headers)
    if response.status_code != 200:
        logging.error(f"Ошибка запроса: {response.status_code}")
        return None, None, None   
    return response.content

# REMEMBER USE LAST PAGE IN ROLL20 'p=227', SIMULAR TO https://app.roll20.net/campaigns/chatarchive/########/?p=227&onePage=&hidewhispers=&hiderollresults="

LINK = ""
COOKIE = ""

nameOfCampaign, pagesCount = parse_url(LINK)
with open('example.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Timestamp', 'Name', 'Content'])
    for i in reversed(range(pagesCount+1)):

        body = parseHTML(nameOfCampaign, i, COOKIE)
        re_pattern = re.compile(r'var msgdata = "([^"]+)"')
        matches = re_pattern.search(str(body))
        if not matches or len(matches.groups()) < 1:
            logging.error("Не найдены данные в переменной msgdata")
            exit(1)

        encoded_data = matches.group(1)
        # decode
        decoded_data = None
        try:
            decoded_data = base64.b64decode(encoded_data).decode('utf-8')
        except Exception as e:
            logging.error(f"Ошибка декодирования: {e}")
            exit(1)
            

        parsedJSON = json.loads(decoded_data)[0]

        for _, value  in parsedJSON.items():
            dataToWrite = []
            try:
                if not value['inlinerolls']:
                    continue
            except:
                dataToWrite.append(timestamp_to_datetime(value['.priority']))
                dataToWrite.append(value['who'])
                dataToWrite.append(value['content'])
                writer.writerow(dataToWrite)

# with open('filename.json', 'w') as f:
#     json.dump(parsedJSON, f)

