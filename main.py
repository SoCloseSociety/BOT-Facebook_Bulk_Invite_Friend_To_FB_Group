import time
from random import random

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import traceback


def xpath_soup(element):
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:
        siblings = parent.find_all(child.name, recursive=False)
        components.append(
            child.name
            if siblings == [child] else
            '%s[%d]' % (child.name, 1 + siblings.index(child))
        )
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)


options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--disable-notifications")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=options)  # version_main allows to specify your chrome version instead of following chrome global version
driver.maximize_window()
driver.get("https://www.facebook.com/")
time.sleep(2)


fb_group_link = input("Enter the group link : ")

choose = input("Enter \"y\" after logging in : ")

# #######
# limit_to_sent_invitation = 500
# #######



if choose == "y":

    while True:
        select_followers_to_be_sent = random.randint(5, 10)
        error_occured = False
        now_selected = 0

        driver.get(fb_group_link)
        count_find_or_not = 0

        while True:
            invite_friends_button_xpath = None
            html = driver.page_source
            soup = BeautifulSoup(html, features="html.parser")
            arr_button = soup.find_all("div", attrs={"role": "button"})
            for ele_arr_button in arr_button:
                try:
                    print(ele_arr_button.attrs["aria-label"])
                    if "Inviter" in ele_arr_button.attrs["aria-label"]:
                        invite_friends_button_xpath = ele_arr_button
                        break

                except:
                    pass

            if invite_friends_button_xpath is not None:
                break

            count_find_or_not = count_find_or_not + 1
            if count_find_or_not == 10:
                break
            time.sleep(1)

        print("invite_friends_button_xpath : ", invite_friends_button_xpath)
        driver.find_element(By.XPATH, xpath_soup(invite_friends_button_xpath)).click()

        count_find_or_not = 0
        while True:
            invite_friends_menu_button_xpath = None
            html = driver.page_source
            soup = BeautifulSoup(html, features="html.parser")
            arr_menu_button = soup.find_all("div", attrs={"role": "menuitem"})
            for ele_arr_menu_button in arr_menu_button:
                try:
                    print(ele_arr_menu_button.text)
                    if "Inviter des amis Facebook" in ele_arr_menu_button.text:
                        invite_friends_menu_button_xpath = ele_arr_menu_button
                        break

                except:
                    pass

            if invite_friends_menu_button_xpath is not None:
                break

            count_find_or_not = count_find_or_not + 1
            if count_find_or_not == 10:
                break
            time.sleep(1)

        driver.find_element(By.XPATH, xpath_soup(invite_friends_menu_button_xpath)).click()

        count_find_or_not = 0
        while True:
            invite_friends_dialogue = None
            html = driver.page_source
            soup = BeautifulSoup(html, features="html.parser")
            invite_friends_dialogue = soup.find("div", attrs={"aria-label": "Invitez des amis à rejoindre ce groupe"})

            if invite_friends_dialogue is not None:
                break

            count_find_or_not = count_find_or_not + 1
            if count_find_or_not == 10:
                break
            time.sleep(1)


        html = driver.page_source
        soup = BeautifulSoup(html, features="html.parser")
        invite_friends_dialogue = soup.find("div", attrs={"aria-label": "Invitez des amis à rejoindre ce groupe"})
        invite_friends_list_first_item = invite_friends_dialogue.find_all("div", attrs={"style": "padding-left: 8px; padding-right: 8px;"})


        length_friends = len(invite_friends_list_first_item)
        i = 0

        while i < length_friends:
            try:
                targeted_friend = invite_friends_list_first_item[i]
                print(targeted_friend)
                if targeted_friend.find("div", attrs= {"role": "checkbox"}) :
                    element = driver.find_element(By.XPATH, xpath_soup(targeted_friend))
                    driver.execute_script("arguments[0].scrollIntoView()", element)

                    driver.find_element(By.XPATH, xpath_soup(targeted_friend)).click()

                    now_selected = now_selected + 1

                    print("Now is  going  on => "+str(i+1)+ " out  of  "+str(select_followers_to_be_sent))
                    if i+1 == select_followers_to_be_sent:
                        break

                    i = i + 1
                    time.sleep(1)
                    html = driver.page_source
                    soup = BeautifulSoup(html, features="html.parser")
                    invite_friends_dialogue = soup.find("div", attrs={"aria-label": "Invitez des amis à rejoindre ce groupe"})
                    invite_friends_list_first_item = invite_friends_dialogue.find_all("div",
                                                                                    attrs={"style": "padding-left: 8px; padding-right: 8px;"})

                    length_friends = len(invite_friends_list_first_item)
                    print("Now length of current list => "+ str(length_friends))
                    print("=====================================")

                else:
                    i = i + 1
                    time.sleep(1)
                    html = driver.page_source
                    soup = BeautifulSoup(html, features="html.parser")
                    invite_friends_dialogue = soup.find("div", attrs={"aria-label": "Invitez des amis à rejoindre ce groupe"})
                    invite_friends_list_first_item = invite_friends_dialogue.find_all("div",
                                                                                    attrs={"style": "padding-left: 8px; padding-right: 8px;"})

                    length_friends = len(invite_friends_list_first_item)
                    print("I am in else")
                    # print("Now length of current list => "+ str(length_friends))
                    # print("=====================================")

            except Exception:
                traceback.print_exc()
                error_occured = True
                # if i+1 == limit_to_sent_invitation:
                #     break
                i = i + 1
                time.sleep(1)
                html = driver.page_source
                soup = BeautifulSoup(html, features="html.parser")
                invite_friends_dialogue = soup.find("div", attrs={"aria-label": "Invitez des amis à rejoindre ce groupe"})
                invite_friends_list_first_item = invite_friends_dialogue.find_all("div",
                                                                                attrs={"style": "padding-left: 8px; padding-right: 8px;"})

                length_friends = len(invite_friends_list_first_item)
                print("Error Occurs")
                print("=====================================")
                break

        print("Now")

        if error_occured & now_selected > 0:
            break

        html = driver.page_source
        soup = BeautifulSoup(html, features="html.parser")
        find_all_btns = soup.find("div", attrs={"aria-label": "Envoyer les invitations"})
        driver.find_element(By.XPATH, xpath_soup(find_all_btns)).click()
        time.sleep(4)
