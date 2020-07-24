from selenium import webdriver

# 本地谷歌浏览器的配置
option = webdriver.ChromeOptions()
option.binary_location = 'C:\Program Files (x86)\Google\Chrome\Application\Chrome.exe'
option.add_experimental_option('debuggerAddress', '127.0.0.1:9222')

# 谷歌浏览器驱动地址
driver = webdriver.Chrome(executable_path=r"F:\chromedriver.exe")

driver.get('https://login.taobao.com/')

driver.maximize_window()

user = driver.find_element_by_id('fm-login-id')
user.send_keys('莫玉尘')
pwd = driver.find_element_by_id('fm-login-password')
pwd.send_keys('txc,111.')

login_button = driver.find_element_by_xpath('//*[@id="login-form"]/div[4]/button')
login_button.click()
