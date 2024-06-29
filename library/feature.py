
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time


def find_element_in_list(driver, xpath_list, wait=3):
    for xpath in xpath_list:
        try:
            element = WebDriverWait(driver, wait).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            return element
        except Exception as e:
            print(f"Element not found with XPath: {xpath}")
    print("No element found in the provided XPath list.")
    return None


def replace_and_increment(replacement_values):
    if replacement_values:
        return replacement_values.pop(0)
    else:
        return ''


def follow_only(driver, status_label, get_url_follow, log, window, global_delay):
    status_label.configure(text=f"Status: Running follow_only")
    window.update()
    urls = get_url_follow()
    n = len(urls)
    log(f"Visiting {len(urls)} profiles.")

    for i in range(n):
        try:
            url = urls[i]
            driver.get(url)
            time.sleep(5)
            try:
                # Perform actions on the profile here
                Xpath = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[1]/div[2]/div/div[1]/button'
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, Xpath)))
                follow_element = driver.find_element(By.XPATH, Xpath)
                assert follow_element.text == 'Follow'
                follow_element.click()
                log(f"Followed profile: {url}")
                time.sleep(2)
            except:
                log(f"Followed profile: {url}")
        except:
            log(f"Failed to visit profile: {url}")
            time.sleep(global_delay)
            continue
        time.sleep(global_delay)
    status_label.configure(text=f"Status: Ready")


def follow_tweet(driver, status_label, window, getInfoOftweet, log, tweet_len_limit, log_error_message, error_text, global_delay):
    status_label.configure(text=f"Status: Running follow_tweet")
    window.update()
    infos = getInfoOftweet()
    for i in range(len(infos)):
        try:
            info = infos[i]
            url = info['url']
            driver.get(url)
            time.sleep(5)
            try:
                # Perform actions on the profile here
                Xpath = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[1]/div[2]/div/div[1]/button'
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, Xpath)))
                follow_element = driver.find_element(By.XPATH, Xpath)
                assert follow_element.text == "Follow"
                follow_element.click()
                print(f"Followed profile: {url}")
                time.sleep(3)
            except:
                print(f"Followed profile: {url}")
            driver.find_element(
                "xpath",
                "/html/body/div[1]/div/div/div[2]/header/div/div/div/div[1]/div[3]/a/div",
            ).click()
            time.sleep(3)

            # Add picture to twitter post
            try:
                xpat1 = "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div/div/div/div[2]/div[2]/div/div/nav/div/div[2]/div/div[1]/div/input"
                xpat2 = "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[3]/div[1]/div/div/div/div[2]/div[2]/div/div/nav/div/div[2]/div/div[1]/div/input"
                xpat3 = "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[4]/div[1]/div/div/div/div[2]/div[2]/div/div/nav/div/div[2]/div/div[1]/div/input"
                input = find_element_in_list(driver, [xpat1, xpat2, xpat3], 2)
                log(input.text)
                input.send_keys(info['image'])
            except Exception as e:
                print(str(e))
                print('can not find image ' + info['image'])
            time.sleep(3)

            # Add content to twitter post
            tweet = str(info['content'])
            this_hashtags = re.split(r'[,\s\n]+', info['hashtag'])
            this_hashtags = [
                '#' + tag if not tag.startswith('#') else tag for tag in this_hashtags]
            hashTag = ""
            for i in this_hashtags:
                hashTag += i+"\n"
            log(hashTag)
            this_tags = re.split(r'[,\s\n]+', info['tag'])
            this_tags = [
                '@' + tag if not tag.startswith('@') else tag for tag in this_tags]
            # add tagname
            tweet = re.sub(
                r'&', lambda match: replace_and_increment(this_tags), tweet)
            # add hashtag
            # tweet = re.sub(r'#', lambda match: replace_and_increment(this_hashtags), tweet)
            try:
                tweet = str(hashTag)+str(tweet)
            except Exception as e:
                print(e)
            log(tweet)
            try:
                tag_ceo = url.split('/')[-1]

            except Exception as e:
                print(e)
            if (len(tweet) + len(tag_ceo) > tweet_len_limit):
                log_error_message(error_text, info['name'] + " too long (" + str(len(tweet) + len(
                    tag_ceo) - tweet_len_limit) + ") . Limit at 280 words (include tag, hastag, space, enter)")
                continue
            element = driver.find_element(
                "class name", "public-DraftEditor-content")
            element.send_keys(tweet)
            time.sleep(3)
            # chưa hiểu đoạn tìm dropdown ở đâu
            try:
                dropdown = driver.find_element(
                    "xpath",
                    "/html/body/div[1]/div/div/div[1]/div[3]",
                )
                driver.execute_script(
                    "arguments[0].parentNode.removeChild(arguments[0]);", dropdown)
            except:
                print('dropdown hidden')
            time.sleep(3)
            driver.find_element(
                "xpath",
                '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div/div/div/div[2]/div[2]/div/div/div/button[2]',
            ).click()
            print(f"Tweeted at profile: {url} : {tweet}")
            time.sleep(global_delay)
        except Exception as e:
            print(f"Failed to visit profile: {url}")
            print(e)
            time.sleep(global_delay)
            continue
        time.sleep(global_delay)
    status_label.configure(text=f"Status: Ready")


def personal_tweet(driver, status_label, window, get_infor_personal_tweet, log, tweet_len_limit, log_error_message, error_text, global_delay):
    status_label.configure(text=f"Status: Running personal_tweet")
    window.update()
    infos = get_infor_personal_tweet()
    log(f"Tweeting")

    for i in range(len(infos)):
        try:
            info = infos[i]
            driver.get("https://twitter.com/compose/tweet")
            time.sleep(5)
            # Perform actions on the profile here

            # add image
            try:
                xpat1 = "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div/div/div/div[2]/div[2]/div/div/nav/div/div[2]/div/div[1]/div/input"
                xpat2 = "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[3]/div[1]/div/div/div/div[2]/div[2]/div/div/nav/div/div[2]/div/div[1]/div/input"
                xpat3 = "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[4]/div[1]/div/div/div/div[2]/div[2]/div/div/nav/div/div[2]/div/div[1]/div/input"
                input = find_element_in_list(driver, [xpat1, xpat2, xpat3], 2)
                input.send_keys(info['image'])
            except Exception as e:
                print(str(e))
                print('can not find image ' + info['image'])
            time.sleep(3)
            # content of tweet
            tweet = str(info['content'])
            this_hashtags = re.split(r'[,\s\n]+', info['hashtag'])
            this_hashtags = [
                '#' + tag if not tag.startswith('#') else tag for tag in this_hashtags]
            hashTag = ""
            for i in this_hashtags:
                hashTag += i+"\n"
            this_tags = re.split(r'[,\s\n]+', info['tag'])
            this_tags = [
                '@' + tag if not tag.startswith('@') else tag for tag in this_tags]
            # add tagname
            tweet = re.sub(
                r'&', lambda match: replace_and_increment(this_tags), tweet)
            log(tweet)
            # add hashtag
            # tweet = re.sub(r'#', lambda match: replace_and_increment(this_hashtags), tweet)
            tweet = hashTag+tweet
            log(tweet)
            if (len(tweet) > tweet_len_limit):
                log_error_message(error_text, "post " + str(
                    info['name']) + " too long  . Limit at 280 words (include tag, hastag, space, enter)")
                continue
            element = driver.find_element(
                "class name", "public-DraftEditor-content")
            element.send_keys(tweet)
            time.sleep(3)
            try:
                dropdown = driver.find_element(
                    "xpath",
                    "/html/body/div[1]/div/div/div[1]/div[3]",
                )
                driver.execute_script(
                    "arguments[0].parentNode.removeChild(arguments[0]);", dropdown)
            except:
                print('dropdown hidden')
            time.sleep(3)

            driver.find_element(
                "xpath",
                '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div/div/div/div[2]/div[2]/div/div/div/button[2]',
            ).click()
            log(f"Tweeted : {tweet}")
            time.sleep(global_delay)
        except Exception as e:
            print(str(e))
            log(f"Failed to tweet")
            continue
        time.sleep(global_delay)
    status_label.configure(text=f"Status: Ready")
