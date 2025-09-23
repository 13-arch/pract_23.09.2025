from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Твои 30 ссылок (можно вставить прямо сюда или загрузить из CSV)
links = ['https://catalog.onliner.by/robotcleaner/xiaomi/5prog20',
 'https://catalog.onliner.by/robotcleaner/xiaomi/bhr089reu',
 'https://catalog.onliner.by/robotcleaner/dreame/x50ultracomplete',
 'https://catalog.onliner.by/robotcleaner/xiaomi/bhr0834eubhr7357',
 'https://catalog.onliner.by/robotcleaner/xiaomi/d102gl',
 'https://catalog.onliner.by/robotcleaner/dreame/rlx63ce2wh',
 'https://catalog.onliner.by/robotcleaner/dreame/rll74ce',
 'https://catalog.onliner.by/robotcleaner/dreame/rll22sewh',
 'https://catalog.onliner.by/robotcleaner/roborock/saros10rbl',
 'https://catalog.onliner.by/robotcleaner/roborock/qrevocurvwhru',
 'https://catalog.onliner.by/robotcleaner/deerma/demx70',
 'https://catalog.onliner.by/robotcleaner/deerma/dems30',
 'https://catalog.onliner.by/robotcleaner/dreame/f9prow',
 'https://catalog.onliner.by/robotcleaner/xiaomi/bhr8159eu',
 'https://catalog.onliner.by/robotcleaner/xiaomi/xiaomi5pro',
 'https://catalog.onliner.by/robotcleaner/xiaomi/bhr9220eu',
 'https://catalog.onliner.by/robotcleaner/xiaomi/s20wheu',
 'https://catalog.onliner.by/robotcleaner/xiaomi/bhr8124eu',
 'https://catalog.onliner.by/robotcleaner/xiaomi/bhr084aeu',
 'https://catalog.onliner.by/robotcleaner/xiaomi/m40d110cn',
 'https://catalog.onliner.by/robotcleaner/xiaomi/bhr0834eu',
 'https://catalog.onliner.by/robotcleaner/dreame/rll77sewh',
 'https://catalog.onliner.by/robotcleaner/dreame/rld31se',
 'https://catalog.onliner.by/robotcleaner/dreame/robotvacuuml10sp',
 'https://catalog.onliner.by/robotcleaner/trouver/dreamee10w',
 'https://catalog.onliner.by/robotcleaner/xiaomi/h40ov51',
 'https://catalog.onliner.by/robotcleaner/xiaomi/bhr6783eu',
 'https://catalog.onliner.by/robotcleaner/hobot/legeed8lulu',
 'https://catalog.onliner.by/robotcleaner/xiaomi/robotvacuume5bhr',
 'https://catalog.onliner.by/robotcleaner/dreame/rld52sewh']

options = webdriver.ChromeOptions()
options.add_argument("--headless")  # убрать, если хочешь видеть браузер
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)

data = []

for url in links:
    driver.get(url)
    time.sleep(2)  # ждём прогрузки JS

    # Название
    try:
        title = driver.find_element(By.CLASS_NAME, "catalog-masthead__title").text
    except:
        title = None

    # Цена
    try:
        price = driver.find_element(By.CLASS_NAME, "offers-description__price").text
    except:
        price = None

    # Характеристики
    characteristics = {}
    try:
        rows = driver.find_elements(By.CLASS_NAME, "product-specs__row")
        for row in rows:
            try:
                key = row.find_element(By.CLASS_NAME, "product-specs__title").text
                value = row.find_element(By.CLASS_NAME, "product-specs__value").text
                characteristics[key] = value
            except:
                pass
    except:
        pass

    data.append({
        "url": url,
        "title": title,
        "price": price,
        "characteristics": characteristics
    })

driver.quit()

# В DataFrame
df = pd.DataFrame(data)

# Разворачиваем характеристики в отдельные колонки
df_expanded = df.join(df["characteristics"].apply(pd.Series))
df_expanded.drop(columns=["characteristics"], inplace=True)

# Сохраняем в CSV
df_expanded.to_csv("onliner_products.csv", index=False, encoding="utf-8-sig")

print("Готово! Данные сохранены в onliner_products.csv")

