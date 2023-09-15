# education platform
Платформа обучения  

### Технологии: 
Django==4.2.5, Pillow==10.0.1


### Установка: 
#### Windows
`python -m venv venv`

`venv/Scripts/activate`

`python -m pip install --upgrade pip`

`pip install -r requirements.txt`

`в корне проекта создать файл .env и поместить туда данные:`  
`KEY = ваш джанго ключ`  
`DBG = True (или False)`  
`STRIPE_PUBLISHABLE_KEY = 'ваш публичный ключ со stripe'`  
`STRIPE_SECRET_KEY = 'ваш секретный ключ со stripe'`  
`STRIPE_API_VERSION = 'версия апи stripe в формате (2022-08-01)'`  

## Описание: 
