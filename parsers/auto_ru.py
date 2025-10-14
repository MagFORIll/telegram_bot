# parsers/auto_ru.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AutoRu:
    def __init__(self, preferences: dict, limit: int = 5):
        """
        preferences - словарь с фильтрами для поиска машин

        limit - сколько машин парсить
        """
        self._preferences = preferences
        self._limit = limit
        self._driver = webdriver.Firefox()
        self._wait = WebDriverWait(self._driver, 10)
        self._url = 'https://auto.ru/podolsk/cars/all/'
        self._cars = []

    def parse(self):


        self._driver.get(self._url)
        items = self._wait.until(
            EC.presence_of_all_elements_located(
                By.CSS_SELECTOR, 'div.ListingItemUniversal__snippet-ZSzaf'
            )
        )[:self._limit]

        for item in items:
            try:
                title = item.find_element(By.CSS_SELECTOR, 'a.ListingItemTitle__link').text
                year = item.find_element(By.CSS_SELECTOR, 'div.Typography2__h5-mkmlZ').text
                power = item.find_element(By.CSS_SELECTOR, 'span.ListingItemUniversalSpecs__spec-IcgjK').text
                price = item.find_element(By.CSS_SELECTOR, 'div.ListingItemUniversalPrice__title-Mi4tV').text
                url = item.find_element(By.CSS_SELECTOR, 'a.ListingItemUniversalSpecs__link-vOcwF').get_attribute('href')

                try:
                    mileage = item.find_element(By.CSS_SELECTOR, 'div.ListingItemUniversalCondition__status-FCDjU').text
                except:
                    mileage = 'не указан'

                model = " ".join(title.split()[1:-1])
                brand = title.split()[0]

                car_data = {
                    'brand': brand,
                    'model': model,
                    'mileage': mileage,
                    'price': price,
                    'year': year,
                    'power': power,
                    'url': url
                }

                if self._matches_preferences(car_data):
                    self._cars.append(car_data)
            except Exception as exc:
                print('Ошибка при парсинге:', exc)
        return self._cars



    def close(self):
        self._driver.quit()