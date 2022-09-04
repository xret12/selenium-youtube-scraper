from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

youtube_trending_url = 'https://www.youtube.com/feed/trending'


def get_driver():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless')  #No GUI
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def get_videos(driver, youtube_trending_url):
  driver.get(youtube_trending_url)
  video_div_tag = 'ytd-video-renderer'
  videos = driver.find_elements(By.TAG_NAME, video_div_tag)
  return videos



if __name__ == "__main__":
  print('Configuring driver...')
  driver = get_driver()

  print('Fetching trending videos..')
  videos = get_videos(driver, youtube_trending_url)

  print(f'Found {len(videos)}')

  print('Parsing the first video...')
  #title, url, thumbnail, url, channel, views, uploaded, description
  video = videos[0]
  title = video.find_element(By.ID, 'video-title').text
  print(title)