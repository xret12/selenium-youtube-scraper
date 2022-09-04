import requests
from bs4 import BeautifulSoup

youtube_trending_url = 'https://www.youtube.com/feed/trending'
#does not execute javascript, fetches the first instance of html the site has loaded
response = requests.get(youtube_trending_url)

# with open('trending.html', 'w') as f:
#   f.write(response.text)

trending_page_soup = BeautifulSoup(response.text, 'html.parser')
video_divs = trending_page_soup.find_all(
    'div', class_='style-scope ytd-video-renderer')

print(f'Found {len(video_divs)} videos')
