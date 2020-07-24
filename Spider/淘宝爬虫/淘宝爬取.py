from selenium import webdriver
import time
import re


def search_product():
    driver.find_element_by_id('q').send_keys(kw)
    driver.find_element_by_xpath('//*[@id="J_TSearchForm"]/div[1]/button').click()
    time.sleep(10)
    token = driver.find_element_by_xpath('//div[@class="total"]').text
    token = int(re.compile('(\d+)').search(token).group(1))
    return token


def drop_down():
    for x in range(1, 11, 2):
        time.sleep(0.5)
        j = x / 10
        js = 'document.documentElement.scrollTop = document.documentElement.scrollHeight * %f' % j
        driver.execute_script(js)


def get_products():
    divs = driver.find_elements_by_xpath('//div[@class="items"]/div[@class="item J_MouserOnverReq  "]')
    for div in divs:
        info = div.find_element_by_xpath('.//div[@class="row row-2 title"]').text
        price = div.find_element_by_xpath('.//div[@class="price g_price g_price-highlight"]/strong').text + '元'
        deal = div.find_element_by_xpath('.//div[@class="deal-cnt"]').text
        image = div.find_element_by_xpath('.//a/img').get_attribute('src')
        name = div.find_element_by_xpath('.//div[@class="shop"]/a/span[2]').text

        product = {'标题': info, '价格': price, '订单量': deal, '图片': image, '名字': name}
        print(product)


def next_page():
    token = search_product()
    drop_down()
    get_products()
    num = 1
    while num != token:
        driver.get('https://s.taobao.com/search?q={}&s={}'.format(kw, 44 * num))
        # 隐式等待，只能等待，最高等待时间为10s，如果超过10s，抛出异常
        driver.implicitly_wait(10)
        num += 1
        drop_down()
        get_products()


if __name__ == '__main__':
    kw = input('请输入要爬取的商品：')
    driver = webdriver.Chrome(r"F:\chromedriver.exe")
    driver.get('http://www.taobao.com/')
    next_page()
