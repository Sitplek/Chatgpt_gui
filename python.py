import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import openai

class ChatWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('ChatGPT')
        self.setFixedSize(600, 800)
        
        self.layout = QtWidgets.QVBoxLayout()
        
        # Создание виджета QScrollArea
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)  # Возможность изменения размера виджета внутри QScrollArea
        self.layout.addWidget(self.scroll_area)

        # Создание виджета QTextEdit для вывода истории чата
        self.chat_history = QtWidgets.QTextEdit()
        self.chat_history.setReadOnly(True)
        self.chat_history.setStyleSheet('font-size: 14px; background-color: #333; color: #EEE; border: none; padding: 10px;')
        self.scroll_area.setWidget(self.chat_history)  # Установка QTextEdit как виджета внутри QScrollArea
        
        self.input_box = QtWidgets.QTextEdit()
        self.input_box.setStyleSheet('font-size: 14px; background-color: #555; color: #EEE; border: 1px solid #888; padding: 10px;')
        self.input_box.setPlaceholderText('Type your message here...')
        self.input_box.setFixedHeight(60)
        self.layout.addWidget(self.input_box, 1)
        
        self.send_button = QtWidgets.QPushButton('Send')
        self.send_button.setStyleSheet('font-size: 14px; background-color: #4CAF50; color: white; padding: 6px 12px;')
        self.send_button.clicked.connect(self.send_message)
        self.layout.addWidget(self.send_button)
        
        # Создание кнопки очистки вывода
        self.clear_button = QtWidgets.QPushButton('Clear')
        self.clear_button.setStyleSheet('font-size: 14px; background-color: #FF0000; color: white; padding: 6px 12px;')
        self.clear_button.clicked.connect(self.clear_chat_history)
        self.layout.addWidget(self.clear_button)

        self.api_key_label = QtWidgets.QLabel('API Key:')
        self.api_key_label.setStyleSheet('font-size: 14px; color: #EEE;')
        self.layout.addWidget(self.api_key_label)

        self.api_key_input = QtWidgets.QLineEdit()
        self.api_key_input.setStyleSheet('font-size: 14px; background-color: #555; color: #EEE; border: 1px solid #888;')
        self.layout.addWidget(self.api_key_input)

        self.setLayout(self.layout)

        self.input_box.setFocus()
        self.input_box.installEventFilter(self)
        
    def eventFilter(self, source, event):
        if (source == self.input_box and event.type() == QtCore.QEvent.KeyPress and
                event.key() == QtCore.Qt.Key_Return and event.modifiers() == QtCore.Qt.NoModifier):
            self.send_message()
            return True
        return super().eventFilter(source, event)
        
    def send_message(self):
        """
        Обработчик события нажатия кнопки "Send".
        Отправляет сообщение пользователя на сервер OpenAI для генерации ответа и обновляет историю чата.
        """
        input_text = self.input_box.toPlainText()
        api_key = self.api_key_input.text().strip()
        
        if not api_key:
            self.update_chat_history(input_text, 'Please enter an API Key.')
            self.input_box.clear()
            return
        
        self.input_box.setEnabled(False)
        self.send_button.setEnabled(False)
        self.api_key_input.setEnabled(False)

        self.thread = QtCore.QThread()
        self.worker = Worker(input_text, api_key)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.process_input)
        self.worker.response_ready.connect(self.update_chat_history)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()
        
    def update_chat_history(self, input_text, response_text):
        """
        Обновляет историю чата с добавлением сообщений пользователя и ответов ChatGPT.
        """
        self.chat_history.append("<b>User:</b> " + input_text)
        self.chat_history.append("<b>ChatGPT:</b> " + response_text)
        self.chat_history.append('<hr/>')
        
        self.scroll_to_bottom()  # Прокрутка вниз при обновлении истории чата

        self.input_box.setEnabled(True)
        self.send_button.setEnabled(True)
        self.api_key_input.setEnabled(True)
        self.input_box.clear()
        self.input_box.setFocus()
        
    def clear_chat_history(self):
        """
        Очищает историю чата.
        """
        self.chat_history.clear()
        
    def scroll_to_bottom(self):
        """
        Прокручивает содержимое виджета QScrollArea вниз.
        """
        scrollbar = self.scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

class Worker(QtCore.QObject):
    response_ready = QtCore.pyqtSignal(str, str)
    finished = QtCore.pyqtSignal()
    
    def __init__(self, input_text, api_key):
        super().__init__()
        self.input_text = input_text
        self.api_key = api_key
        
    @QtCore.pyqtSlot()
    def process_input(self):
        """
        Обработка ввода пользователя.
        Выполняет запрос к API OpenAI для получения ответа ChatGPT.
        """
        try:
            response = self.get_response(self.input_text)
            self.response_ready.emit(self.input_text, response)
        except Exception as e:
            self.response_ready.emit(self.input_text, f"Error: {str(e)}")
        
        self.finished.emit()
        
    def get_response(self, input_text):
        """
        Генерирует ответ ChatGPT на основе введенного пользователем текста.
        """
        prompt = f"User: {input_text}\nChatGPT:"
        openai.api_key = self.api_key
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": input_text}
            ]
        )
        return response.choices[0].message['content']


if __name__ == '__main__':
    openai.api_key = "YOUR_API_KEY"  # Ваш API-ключ OpenAI
    
    app = QtWidgets.QApplication(sys.argv)

    # Настройка темной темы
    app.setStyle("Fusion")
    dark_palette = QtGui.QPalette()
    dark_palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
    dark_palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
    dark_palette.setColor(QtGui.QPalette.Base, QtGui.QColor(25, 25, 25))
    dark_palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
    dark_palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
    dark_palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
    dark_palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
    dark_palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
    dark_palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
    dark_palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
    dark_palette.setColor(QtGui.QPalette.Link, QtGui.QColor(42, 130, 218))
    dark_palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(42, 130, 218))
    dark_palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
    app.setPalette(dark_palette)

    chat_window = ChatWindow()
    chat_window.show()
    sys.exit(app.exec_())
