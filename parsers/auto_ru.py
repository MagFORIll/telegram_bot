# parsers/auto_ru.py
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


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

        for key, item in self._preferences.items():
            print(key, item)
            try:
                if key == 'brand':
                    mark_wrapper = self._wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR,"div.Input2__wrapper-ypcf0"))
                    )
                    self._driver.execute_script('arguments[0].click;', mark_wrapper)
                    ActionChains(self._driver).move_to_element(mark_wrapper).click().perform()
                    time.sleep(0.5)
                    mark_wrapper.send_keys(item)
                    self._wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.InputSuggest__suggests')))
                    mark_wrapper.send_keys(Keys.ARROW_DOWN)
                    mark_wrapper.send_keys(Keys.RETURN)
                    time.sleep(1)
                elif key == 'model':
                    field = self._wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='model']"))
                    )
                    field.click()
                    field.send_keys(item)
                    time.sleep(1)
                    field.send_keys(Keys.ARROW_DOWN)
                    field.send_keys(Keys.RETURN)
                elif key == 'mileage':
                    field = self._wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='km_age_from']"))
                    )
                    field.clear()
                    field.send_keys(item)
                elif key == 'price':
                    field = self._wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='price_from']"))
                    )
                    field.clear()
                    field.send_keys(item)
                elif key == 'year':
                    field = self._wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='year_from']"))
                    )
                    field.click()
                    field.send_keys(item)
                    field.send_keys(Keys.RETURN)
                else:
                    continue

            except Exception as exc:
                print(f'Error: {exc}')

        try:
            search_button = self._wait.until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//button[contains(., 'Показать')]"
                ))
            )
            self._driver.execute_script('arguments[0].scrollIntoView(true);', search_button)
            time.sleep(0.5)
            self._driver.execute_script('arguments[0].click();', search_button)
        except Exception as exc:
            print(f'Error: {exc}')

        items = self._wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, 'div.ListingItemUniversal__snippet-ZSzaf')
            )
        )[:self._limit]

        for item in items:
            try:
                title = item.find_element(By.CSS_SELECTOR, 'a.ListingItemTitle__link').text
                year = item.find_element(By.CSS_SELECTOR, 'div.Typography2__h5-mkmlZ').text
                power = item.find_element(By.CSS_SELECTOR, 'span.ListingItemUniversalSpecs__spec-IcgjK').text
                price = item.find_element(By.CSS_SELECTOR, 'div.ListingItemUniversalPrice__title-Mi4tV').text
                url = item.find_element(By.CSS_SELECTOR, 'a.ListingItemUniversalSpecs__link-vOcwF').get_attribute(
                    'href')

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

                self._cars.append(car_data)
            except Exception as exc:
                print('Ошибка при парсинге:', exc)
        return self._cars

    def close(self):
        self._driver.quit()
