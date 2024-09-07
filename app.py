from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    email = request.json.get('email')
    
    # Настройка Selenium
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Запуск в фоновом режиме
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Запуск браузера
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get('https://cloud-desktop.ru/')
        
        # Нажимаем кнопку "Протестировать бесплатно"
        test_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Протестировать бесплатно')]")
        test_button.click()
        
        # Вводим email
        email_input = driver.find_element(By.XPATH, "//input[@placeholder='Введите ваш Емейл']")
        email_input.send_keys(email)
        
        # Ставим галочку "Согласен с условиями использования"
        agree_checkbox = driver.find_element(By.XPATH, "//input[@type='checkbox']")
        agree_checkbox.click()
        
        # Нажимаем кнопку "ТЕСТИРОВАТЬ"
        final_test_button = driver.find_element(By.XPATH, "//button[contains(text(), 'ТЕСТИРОВАТЬ')]")
        final_test_button.click()

        time.sleep(5)  # Ждем, чтобы увидеть результат (можно настроить по необходимости)
        
        return jsonify({"message": "Email отправлен", "email": email}), 200
    except Exception as e:
        return jsonify({"message": "Ошибка: " + str(e)}), 500
    finally:
        driver.quit()

if __name__ == '__main__':
    app.run(debug=True)
