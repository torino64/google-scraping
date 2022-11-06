from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urllib.parse
from collections import deque
from google_scraper import GoogleScraper
import re
import sys
from colored import fg

objectscrap=GoogleScraper()
allurls=objectscrap.run("\"ensias\"")

for Url in allurls:
 for user_url in Url:
    urls = deque([user_url])
    scraped_urls = set()
    emails = set()

    count = 0
    try:
      while len(urls):
        count += 1
        if count == 100:
            break
        url = urls.popleft()
        scraped_urls.add(url)

        parts = urllib.parse.urlsplit(url)
        base_url = '{0.scheme}://{0.netloc}'.format(parts)
        path = url[:url.rfind('/')+1] if '/' in parts.path else url

        print('[%d] Processing %s' % (count, url))
        try:
            response = requests.get(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            continue

        new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
        emails.update(new_emails)

        soup = BeautifulSoup(response.text, features="lxml")

        for anchor in soup.find_all("a"):
            link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
            if link.startswith('/'):
                link = base_url + link
            elif not link.startswith('http'):
                link = path + link
            if not link in urls and not link in scraped_urls:
                urls.append(link)

    except KeyboardInterrupt:
       print('[-] Closing!')
       sys.exit()

    for mail in emails:
       color = fg('blue')
       print(color + mail)
