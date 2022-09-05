from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import logging
import time

youtube_trending_url = 'https://www.youtube.com/feed/trending'


def get_driver():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless')  #No GUI
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def scrollDown(driver, value):
    driver.execute_script("window.scrollBy(0," + str(value) + ")")


# Scroll down the page
def scrollDownAllTheWay(driver):
    old_page = driver.page_source
    while True:
        logging.debug("Scrolling loop")
        for i in range(2):
            scrollDown(driver, 1000)
            time.sleep(1)
        new_page = driver.page_source
        if new_page != old_page:
            old_page = new_page
        else:
            break
    return True


def get_videos(driver, youtube_trending_url):
    driver.get(youtube_trending_url)
    scrollDownAllTheWay(driver)
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.ID, "channel-header-container")))
    except:
        driver.quit()
    video_div_tag = 'ytd-video-renderer'
    videos = driver.find_elements(By.TAG_NAME, video_div_tag)
    return videos


def parse_video(video):
    title_tag = video.find_element(By.ID, 'video-title')
    video_title = title_tag.text
    video_url = title_tag.get_attribute('href')

    thumbnail_tag = video.find_element(By.TAG_NAME, 'img')
    video_thumbnail = thumbnail_tag.get_attribute('src')

    channel_div = video.find_element(By.CLASS_NAME, 'ytd-channel-name')
    video_channel = channel_div.text

    video_description = video.find_element(By.ID, 'description-text').text

    video_info_dict = {
        'title': video_title,
        'url': video_url,
        'thumbnail': video_thumbnail,
        'channel': video_channel,
        'description': video_description
    }
    return video_info_dict


# def get_videos(driver, youtube_trending_url):
#     driver.get(youtube_trending_url)
#     video_div_id = 'dimissible'
#     videos = driver.find_elements(By.ID, video_div_id)
#     return videos

if __name__ == "__main__":
    print('Configuring driver...')
    driver = get_driver()

    print('Fetching trending videos..')
    videos = get_videos(driver, youtube_trending_url)

    print(f'Found {len(videos)}')
    # for vid in videos:
    #   print(vid.text)

    # print('Parsing the first video...')
    #title, url, thumbnail, url, channel, views, uploaded, description
    # video = videos[0]
    # title = video.find_element(By.ID, 'video-title').text
    # print(title)

    videos_data = [parse_video(video) for video in videos[:10]]
    print('Saving data to csv...')

    videos_df = pd.DataFrame(videos_data)
    videos_df.to_csv('trending.csv', index=None)
