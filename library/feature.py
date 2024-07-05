
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


def replace_all(replacement_values):
    value = ""
    for i in replacement_values:
        value += replacement_values.pop(0)+" "
    return value


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
                hashTag += i+" "
            hashTag += "\n"
            this_tags = re.split(r'[,\s\n]+', info['tag'])
            this_tags = [
                '@' + tag if not tag.startswith('@') else tag for tag in this_tags]
            # add tagname
            tweet = re.sub(
                r'&&&', lambda match: replace_all(this_tags), tweet)
            log(tweet)
            # add hashtag
            # tweet = re.sub(r'#', lambda match: replace_and_increment(this_hashtags), tweet)
            sub_hashtags = re.split(r'[,\s\n]+', info['subhashtag'])
            sub_hashtags = [
                '#' + tag if not tag.startswith('#') else tag for tag in sub_hashtags]
            sub_hashtag = ""
            for i in sub_hashtags:
                sub_hashtag += i+" "
            tweet = hashTag+tweet + "\n"+sub_hashtag
            log(tweet)
            if (len(tweet) > tweet_len_limit):
                log_error_message(error_text, "post " + str(
                    info['name']) + " too long  . Limit at 280 words (include tag, hastag, space, enter)")
                log("too long")
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
