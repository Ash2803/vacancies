# Что делает
Выводит статистику по 10 языкам программирования, собирая данные на hh.ru и superjob.ru


# Как запустить
Для запуска требуется установленный Python версии 3.6 и выше и macOS или Linux

- Скачайте код
- Установите зависимости из requirements.txt
```
pip install -r requirements.txt
```
# Вывод статистки по hh.ru
- Запустите hh_vacancies.py:
```
python hh_vacancies.py
```
# Вывод статистки по superjob.ru

- Получить ключ к API <a href="https://api.superjob.ru/" target="_blank">тут</a>
- Создать переменную окружения `SECRET_KEY` и поместить в нее полученный токен
- Запустить скрипт
```
python superjob_vacancies.py
```

# Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков dvmn.org.