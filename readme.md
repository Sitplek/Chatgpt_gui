## ChatGPT - Простой чат на основе модели GPT-3.5 Turbo

Приветствуем вас в проекте ChatGPT! Этот проект представляет собой простое приложение чата, разработанное с использованием библиотеки PyQt5 и модели языкового искусственного интеллекта GPT-3.5 Turbo от OpenAI. Приложение позволяет вам общаться с моделью ChatGPT, задавая ей вопросы и получая ответы в реальном времени.

### Установка

1. Склонируйте репозиторий с помощью следующей команды:
   ```
   git clone https://github.com/yourusername/ChatGPT.git
   ```
   Замените `yourusername` на ваше имя пользователя на GitHub.

2. Установите зависимости, указанные в файле `requirements.txt`, с помощью следующей команды:
   ```
   pip install -r requirements.txt
   ```

### Использование

1. Получите API-ключ OpenAI, необходимый для использования модели ChatGPT. Инструкции по получению ключа можно найти на официальном сайте OpenAI.

2. Внесите свой API-ключ в код приложения. Откройте файл `python.py` в текстовом редакторе и замените значение переменной `YOUR_API_KEY` на ваш собственный API-ключ OpenAI.

3. Запустите приложение с помощью следующей команды:
   ```
   python python.py
   ```

4. После запуска приложения появится окно чата. Вы можете вводить свои сообщения в текстовом поле "Type your message here..." и нажимать кнопку "Send" или клавишу Enter для отправки запроса ChatGPT. Ответы модели будут отображаться в истории чата.

### Основные функции

#### 1. Отправка сообщений

Вы можете отправлять сообщения, задавая вопросы или вводя текст, нажимая кнопку "Send" или клавишу Enter. Ваши сообщения будут отображаться в истории чата под именем "User".

#### 2. Очистка истории чата

Для очистки истории чата вы можете нажать кнопку "Clear". После этого вся предыдущая история чата будет удалена.

### Настройка внешнего вида

Приложение имеет темную тему оформления. Если вы хотите изменить внешний вид приложения, вы можете изменить соответствующие параметры в коде в методе `__main__`:

```python
app.setStyle("Fusion")
dark_palette = QtGui.QPalette()
# Настройка цветовой палитры
# ...
app.setPalette(dark_palette)
```

### Замена модели ChatGPT



По умолчанию в приложении используется модель ChatGPT с идентификатором "gpt-3.5-turbo". Если вы хотите заменить модель на другую, вы можете изменить соответствующий параметр в методе `get_response` класса `Worker`:

```python
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    # ...
)
```

Замените "gpt-3.5-turbo" на идентификатор желаемой модели.



### Автор

Автор проекта ChatGPT - Hoodiesn. Вы можете связаться со мной по адресу sitplekda@gmail.com.

