import threading
from _ast import arg
import encodings.idna
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import codecs
import time
import re

def test():
    global goodStrings
    global badStrings
    global allStrings

    driver = webdriver.Chrome(executable_path=r"C:\chromedriver\chromedriver.exe")

    wait = WebDriverWait(driver, 30)
    #i = startString

    while True:
        fOut = codecs.open('outParse.csv', 'a', 'utf-8')
        tmpReadFileVal = fIn.readline()

        if not tmpReadFileVal:
            break

        tmpReadFileValSplitted = tmpReadFileVal.split(';')
        link = "http://admotors.ru/products/" + str(tmpReadFileValSplitted[2].replace(' ', '%20')) + "/" + str(tmpReadFileValSplitted[0])
        driver.get(link)

        #EC.element_to_be_clickable((By.CLASS_NAME, "b-nep-filter-reset-btn")) or
        #EC.text_to_be_present_in_element((By.TAG_NAME, "h1"), "Страница, которую вы ищете, не существует") or EC.element_to_be_clickable((By.CLASS_NAME, "b-nep-filter-reset-btn"))
        try:
            #wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "b-nep-filter-reset-btn")))
            wait.until(EC.any_of(EC.element_to_be_clickable((By.CLASS_NAME, "b-nep-filter-reset-btn")),
                                       EC.text_to_be_present_in_element((By.TAG_NAME, "h1"), "Страница, которую вы ищете, не существует")))
        except:
            pass
        main_page = driver.page_source

        if len(re.findall(r'<div class=\"b-nep-mstd-width\" style=\"\"> *[0-9]{1,4}\.[0-9]{1,4} *</div>', main_page)) != 0:
            #print(str(re.findall(r'[0-9]{1,3}\.[0-9]{1,4}', re.findall(r'<div class=\"b-nep-mstd-width\" style=\"\"> *[0-9]{1,3}\.[0-9]{1,4} *</div>', main_page)[0])[0]))
            fOut.write(tmpReadFileVal.replace('\n', '').replace('\r', '') + ";" + str(re.findall(r'[0-9]{1,3}\.[0-9]{1,4}', re.findall(r'<div class=\"b-nep-mstd-width\" style=\"\"> *[0-9]{1,3}\.[0-9]{1,4} *</div>', main_page)[0])[0]) + "\n")
            goodStrings += 1
        else:
            badStrings += 1
            #print("-")
            fOut.write(tmpReadFileVal.replace('\n', '').replace('\r', '') + ";null\n")
        allStrings += 1
        if allStrings > 1 and round(countOfStrings / (allStrings - 1) * 100) != round(countOfStrings / allStrings * 100):
            print('Текущий прогресс: ' + str(round(allStrings / countOfStrings * 100)) + '%. Всего считано: ' + str(allStrings) + ' Успешно/Провально: ' + str(goodStrings) + '/' + str(badStrings) + ' | Максимальное время ожидания: ' + str(round(((countOfStrings - allStrings) * 30)/60/countOfThreads, 2)) + ' минут')
        fOut.close()
    print("Поток завершил свою работу")
    driver.close()

#fileName = 'inParse'
fileName = input('Введите название csv файла (): ')

print('Анализ входного файла...')
fIn = codecs.open(fileName + '.csv', 'r', 'utf-8')
countOfStrings = 0

allStrings = 0
goodStrings = 0
badStrings = 0

while fIn.readline():
    countOfStrings += 1
fIn.close()
print('Обнаружено ' + str(countOfStrings) + ' строк\n')


print('Парсинг рекомендуется ставить на ночь')
print('Рекомендуется закрыть все сторонние программы \nи во время парсинга не приблежаться к компьютеру ближе чем на 2 метра')
print('\nВНИМАНИЕ! ПРИ УСТАНОВКЕ СВЫШЕ 15 ПОТОКОВ КОМП СГОРИТ!')
print('Рекомендуемое значение 10. Ограничение выставлено до 20 потоков')
countOfThreads = int(input('\nВведите кол-во потоков: '))

if countOfThreads > 20:
    print('Вы нарушили первое правило парсера - никогда не ставить большое количество потоков на парсер. Увидимся позже')
    exit()

fIn = codecs.open(fileName + '.csv', 'r', 'utf-8')
fOut = codecs.open('outParse.csv', 'w', 'utf-8')
fOut.close()

t = [threading.Thread(target=test, args=()) for j in range(countOfThreads)]
for i in range(countOfThreads):
    t[i].start()
for i in range(countOfThreads):
    t[i].join()

print('Парсинг окончен!')
print('Всего считано: ' + str(allStrings) + ' Успешно/Провально: ' + str(goodStrings) + '/' + str(badStrings))

fIn.close()