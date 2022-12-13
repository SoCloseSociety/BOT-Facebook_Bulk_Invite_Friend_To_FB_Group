import time

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
time.sleep(20)

choose = input("Enter \"y\" after logging in : ")

#######
limit_to_sent_invitation = 500
#######

if choose == "y":
    html = driver.page_source
    soup = BeautifulSoup(html, features="html.parser")
    invite_friends_dialogue = soup.find("div", attrs={"aria-label": "Invitez des amis à rejoindre ce groupe"})
    invite_friends_list_first_item = invite_friends_dialogue.find_all("div",
                                                                      attrs={"style": "padding-left: 8px; padding-right: 8px;"})


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

                print("Now is  going  on => "+str(i+1)+ " out  of  "+str(limit_to_sent_invitation))
                if i+1 == limit_to_sent_invitation:
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

    print("Now")
    html = driver.page_source
    soup = BeautifulSoup(html, features="html.parser")
    find_all_btns = soup.find("div", attrs={"aria-label": "Envoyer les invitations"})
    driver.find_element(By.XPATH, xpath_soup(find_all_btns)).click()
    time.sleep(4)
