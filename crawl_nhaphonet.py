from typing import List
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import pandas as pd
import time
import config

class RealEstateCrawler:
    def __init__(self, type_realestate: str) -> None:
        self.type_realestate = type_realestate
        self.df_res: pd.DataFrame = pd.DataFrame()
    
    def crawl_page(self, page_number: int) -> pd.DataFrame:
        self.options = uc.ChromeOptions()
        self.options.headless = False
        # self.options.add_argument("user-agent=Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)")
        self.browser = uc.Chrome(options=self.options)
        self.browser.get(f"{config.url_nhaphonet}/{self.type_realestate}{page_number}/ ")

        titles = WebDriverWait(self.browser, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "js-format-phone")))
        prices = WebDriverWait(self.browser, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "property-row__meta__item.is-price")))
        areas = WebDriverWait(self.browser, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "property-row__meta__item.is-area")))
        locations = WebDriverWait(self.browser, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "d-none.w-100.d-sm-inline.mt-2.mt-md-0.property-row__address")))
        

        res_title = [title.text for title in titles]
        res_price = [price.text for price in prices]
        res_area = [area.text for area in areas]
        res_location = [location.text for location in locations]

        max_len = max(len(res_title), len(res_price), len(res_area), len(res_location))
        if len(res_title) < max_len:
            res_title += [''] * (max_len - len(res_title))
        if len(res_price) < max_len:
            res_price += [''] * (max_len - len(res_price))
        if len(res_area) < max_len:
            res_area += [''] * (max_len - len(res_area))
        if len(res_location) < max_len:
            res_location += [''] * (max_len - len(res_location))

        df: pd.DataFrame = pd.DataFrame({
            'Title': res_title,
            'Price': res_price,
            'Area': res_area,
            'Location': res_location,
            'type': 'cho_thue_cua_hang'
        })
        time.sleep(2)
        self.browser.close()

        return df

    def crawl_and_save_data(self, start_page: int, end_page: int) -> None:
        for i in range(start_page, end_page):
            start_time = time.time()
            print(f"Progress to page {i+1}")
            df = self.crawl_page(i+1)
            self.df_res = pd.concat([self.df_res, df], ignore_index=True)
            end_time = time.time()
            print(f"1 iteration takes {end_time-start_time}")
            if (i+1) % 20 == 0:
                self.df_res.to_csv(f"D:\\OneDrive\KiotViet\\Python_for_work\\KFinance\\CSV_crawl_data\\nhaphonet_thue_nha_mat_pho_{i+1}.csv", index=False, encoding='utf-8-sig')
                self.df_res = pd.DataFrame()

if __name__ == '__main__':
    types_realestate: List[str] = ["cho-thue/nha-mat-pho/page/"]
    # types_realestate: List[str] = ["cho-thue-cua-hang-kiot"]

    for type_realestate in types_realestate:
        real_estate_crawler = RealEstateCrawler(type_realestate)
        real_estate_crawler.crawl_and_save_data(0, 100)  # Thay đổi khoảng trang bạn muốn crawl ở đây 