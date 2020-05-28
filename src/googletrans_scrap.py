from selenium import webdriver
import time


class google_trans:

    def __init__(self):
        self.driver = webdriver.Chrome(r"C:\Users\blasc\PycharmProjects\chromedriver.exe")
        url = "https://www.google.com/search?q=traductor&rlz=1C1CHBD_esES859ES859&oq=traductor&aqs=chrome" \
              "..69i57j69i61.2062j0j8&sourceid=chrome&ie=UTF-8 "
        self.driver.get(url)

    def translate_into_esp(self, tweet):
        search_box = self.driver.find_element_by_xpath('//*[@id="tw-source-text-ta"]')
        search_box.send_keys(tweet)
        time.sleep(1.7)
        translate_box = self.driver.find_element_by_css_selector('#tw-target-text')
        translate_box_fem = self.driver.find_element_by_css_selector('#tw-target-text-feminine > span:nth-child(1)')
        translate_box_masc = self.driver.find_element_by_css_selector('#tw-target-text-masculine > span:nth-child(1)')
        traduccion = translate_box.text
        if not traduccion:
            # traduccion_fem = translate_box_fem.text
            # print(f"\ntraduccion fem: {traduccion_fem}")
            traduccion = translate_box_masc.text
            # print(f"traduccion masc: {traduccion}\n")
        # else:
        # print(f"traduccion: {traduccion}")
        time.sleep(0.4)
        search_box.clear()
        return traduccion

    def exit_browser(self):
        self.driver.quit()
        time.sleep(0.3)
