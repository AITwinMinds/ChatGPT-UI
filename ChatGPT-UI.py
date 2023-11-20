import sys
import os
import json
import re
import httpx
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QMessageBox, QRadioButton, QCheckBox,
    QTextEdit, QLabel, QComboBox
)
from PyQt5.QtGui import QPalette, QColor, QFont
import openai
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from bs4 import BeautifulSoup
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter


class GPTUI(QWidget):
    CONFIG_FILE_PATH = "config.json"

    def __init__(self):
        super().__init__()

        self.client = None
        self.api_key_fixed = False
        self.stop_generation = False

        self.init_ui()

        self.load_config_from_file()

    def init_ui(self):
        self.setWindowTitle('ChatGPT')
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QtGui.QIcon("icon.png"))

        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(45, 45, 45))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(30, 30, 30))
        dark_palette.setColor(QPalette.AlternateBase, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(26, 82, 118))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        self.setPalette(dark_palette)

        layout = QVBoxLayout()

        input_layout = QHBoxLayout()

        self.api_key_input = QLineEdit(self)
        self.api_key_input.setPlaceholderText('Enter API key...')
        self.set_widget_palette_color(self.api_key_input, '#3498db')
        input_layout.addWidget(self.api_key_input)

        self.fix_api_key_button = QPushButton('Fix/Unfix API Key', self)
        self.fix_api_key_button.clicked.connect(self.toggle_api_key)

        input_layout.addWidget(self.fix_api_key_button)
        layout.addLayout(input_layout)

        self.toggle_always_on_top_button = QPushButton('Always On Top', self)
        self.toggle_always_on_top_button.clicked.connect(self.toggle_always_on_top)
        self.toggle_always_on_top_button.setStyleSheet('background-color: #447ea3; min-width: 0px; font: 10.5pt;')
        input_layout.addWidget(self.toggle_always_on_top_button)

        prompt_layout = QHBoxLayout()

        self.radio_rephrase = QRadioButton('Rephrase', self)
        self.radio_rephrase.setChecked(True)
        prompt_layout.addWidget(self.radio_rephrase)

        self.radio_debug_code = QRadioButton('Debug code', self)
        prompt_layout.addWidget(self.radio_debug_code)

        self.radio_summarize = QRadioButton('Summarize', self)
        prompt_layout.addWidget(self.radio_summarize)

        self.radio_translate = QRadioButton('Translate', self)
        prompt_layout.addWidget(self.radio_translate)

        self.radio_email = QRadioButton('Reply to email', self)
        prompt_layout.addWidget(self.radio_email)

        self.radio_explain = QRadioButton('Explain', self)
        prompt_layout.addWidget(self.radio_explain)

        self.radio_manual_prompts = QRadioButton('Manual prompts', self)
        prompt_layout.addWidget(self.radio_manual_prompts)
        layout.addLayout(prompt_layout)

        language_layout = QHBoxLayout()

        language_layout.setAlignment(Qt.AlignLeft)

        self.from_language_dropdown = QComboBox(self)
        self.to_language_dropdown = QComboBox(self)
        self.from_language_dropdown.setHidden(True)
        self.to_language_dropdown.setHidden(True)

        self.from_language_dropdown.setMaximumWidth(100)
        self.to_language_dropdown.setMaximumWidth(100)

        self.from_language_label = QLabel('From Language:', self)
        self.to_language_label = QLabel('To Language:', self)
        self.from_language_label.setHidden(True)
        self.to_language_label.setHidden(True)

        self.from_language_label.setMaximumWidth(120)
        self.to_language_label.setMaximumWidth(100)

        language_layout.addWidget(self.from_language_label)
        language_layout.addWidget(self.from_language_dropdown)
        language_layout.addWidget(self.to_language_label)
        language_layout.addWidget(self.to_language_dropdown)

        layout.addLayout(language_layout)

        self.radio_translate.toggled.connect(self.toggle_language_dropdowns)

        available_languages = [
            "Afrikaans", "Albanian", "Amharic", "Arabic", "Armenian", "Azerbaijani", "Basque", "Belarusian", "Bengali",
            "Bosnian", "Bulgarian", "Catalan", "Cebuano", "Chichewa", "Chinese (Simplified)", "Chinese (Traditional)",
            "Corsican", "Croatian",
            "Czech", "Danish", "Dutch", "English", "Esperanto", "Estonian", "Filipino", "Finnish", "French", "Frisian",
            "Galician", "Georgian", "German", "Greek", "Gujarati", "Haitian Creole", "Hausa", "Hawaiian", "Hebrew",
            "Hindi",
            "Hmong", "Hungarian", "Icelandic", "Igbo", "Indonesian", "Irish", "Italian", "Japanese", "Javanese",
            "Kannada",
            "Kazakh", "Khmer", "Kinyarwanda", "Korean", "Kurdish (Kurmanji)", "Kyrgyz", "Lao", "Latin", "Latvian",
            "Lithuanian",
            "Luxembourgish", "Macedonian", "Malagasy", "Malay", "Malayalam", "Maltese", "Maori", "Marathi", "Mongolian",
            "Myanmar (Burmese)",
            "Nepali", "Norwegian", "Pashto", "Persian", "Polish", "Portuguese", "Punjabi", "Romanian", "Russian",
            "Samoan",
            "Scots Gaelic", "Serbian", "Sesotho", "Shona", "Sindhi", "Sinhala", "Slovak", "Slovenian", "Somali",
            "Spanish",
            "Sundanese", "Swahili", "Swedish", "Tajik", "Tamil", "Telugu", "Thai", "Turkish", "Ukrainian", "Urdu",
            "Uzbek", "Vietnamese", "Welsh", "Xhosa", "Yiddish", "Yoruba", "Zulu"
        ]
        self.from_language_dropdown.addItems(available_languages)
        self.to_language_dropdown.addItems(available_languages)

        self.checkbox_clipboard = QCheckBox('Use last clipboard text', self)
        self.checkbox_clipboard.setChecked(True)
        layout.addWidget(self.checkbox_clipboard)

        self.input_text = QTextEdit(self)
        self.input_text.setPlaceholderText('Enter prompt manually...')
        self.input_text.setFixedHeight(70)
        self.input_text.setStyleSheet("QTextEdit { background-color: #202020; color: white; font-size: 12pt; }")
        self.input_text.setHidden(True)
        layout.addWidget(self.input_text)

        self.text_editor = QTextEdit(self)
        self.text_editor.setPlaceholderText('Enter text manually...')
        self.text_editor.setStyleSheet("QTextEdit { background-color: #202020; color: white; font-size: 12pt; }")
        self.text_editor.setFixedHeight(150)
        self.text_editor.setHidden(True)
        layout.addWidget(self.text_editor)

        self.proxy_checkbox = QCheckBox('Enable HTTP proxy', self)
        self.proxy_checkbox.toggled.connect(self.configure_proxy)
        layout.addWidget(self.proxy_checkbox)

        self.proxy_input_layout = QVBoxLayout()
        self.proxy_server_label = QLabel('Proxy Server:', self)
        self.proxy_server_input = QLineEdit(self)
        self.proxy_server_label.setHidden(True)
        self.proxy_server_input.setHidden(True)

        self.proxy_input_layout.addWidget(self.proxy_server_label)
        self.proxy_input_layout.addWidget(self.proxy_server_input)

        self.proxy_port_label = QLabel('Proxy Port:', self)
        self.proxy_port_input = QLineEdit(self)
        self.proxy_port_label.setHidden(True)
        self.proxy_port_input.setHidden(True)
        self.proxy_input_layout.addWidget(self.proxy_port_label)
        self.proxy_input_layout.addWidget(self.proxy_port_input)

        layout.addLayout(self.proxy_input_layout)

        self.save_proxy_button = QPushButton('Save Proxy Settings', self)
        self.save_proxy_button.clicked.connect(self.save_proxy_settings)
        self.save_proxy_button.setHidden(True)
        layout.addWidget(self.save_proxy_button)

        self.checkbox_clipboard.stateChanged.connect(self.toggle_clipboard_text)

        self.radio_manual_prompts.toggled.connect(self.toggle_manual_prompt_input)

        self.proxy_checkbox.stateChanged.connect(self.configure_proxy)

        self.output_text = QTextEdit(self)
        self.output_text.setPlaceholderText('Response will appear here...')
        self.output_text.setStyleSheet("QTextEdit { background-color: #202020; color: white; font-size: 12pt; }")
        layout.addWidget(self.output_text)

        button_layout = QHBoxLayout()

        self.run_regenerate_button = QPushButton('Generate', self)
        self.run_regenerate_button.clicked.connect(self.run_regenerate_text)
        self.set_widget_palette_color(self.run_regenerate_button, '#1a5276')
        button_layout.addWidget(self.run_regenerate_button)

        self.copy_button = QPushButton('Copy response', self)
        self.copy_button.clicked.connect(self.copy_text)
        self.set_widget_palette_color(self.copy_button, '#2ecc71')
        button_layout.addWidget(self.copy_button)

        self.stop_button = QPushButton('Stop', self)
        self.stop_button.clicked.connect(self.stop_generation_process)
        self.set_widget_palette_color(self.stop_button, '#e74c3c')
        button_layout.addWidget(self.stop_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

        font = QFont()
        font.setPointSize(12)
        self.setFont(font)

        self.from_language_dropdown.currentIndexChanged.connect(self.save_config_to_file)
        self.to_language_dropdown.currentIndexChanged.connect(self.save_config_to_file)

        self.load_config_from_file()
        if self.api_key_input.text() == "":
            self.fix_api_key_button.setStyleSheet('background-color: #447ea3; min-width: 0px; font: 10.5pt;')
        else:
            self.fix_api_key_button.setStyleSheet('background-color: #2ecc71; min-width: 0px; font: 10.5pt;')
        print("Key is:", self.api_key_input.text())

    def toggle_language_dropdowns(self, checked):
        self.from_language_dropdown.setHidden(not checked)
        self.to_language_dropdown.setHidden(not checked)
        self.from_language_label.setHidden(not checked)
        self.to_language_label.setHidden(not checked)

    def toggle_manual_prompt_input(self, checked):
        self.input_text.setHidden(not checked)
        if checked:
            self.input_text.setFocus()

    def toggle_api_key(self):
        if self.api_key_fixed:
            self.api_key_fixed = False
            self.api_key_input.setReadOnly(False)
            self.set_widget_palette_color(self.api_key_input, '#3498db')
            self.fix_api_key_button.setStyleSheet(
                'background-color: #447ea3; min-width: 0px; font: 10.5pt;')
        else:
            self.set_api_key()
            self.fix_api_key_button.setStyleSheet(
                'background-color: #2ecc71; min-width: 0px; font: 10.5pt;')

    def toggle_proxy_settings(self, state):
        self.proxy_server_label.setHidden(not state)
        self.proxy_server_input.setHidden(not state)
        self.proxy_port_label.setHidden(not state)
        self.proxy_port_input.setHidden(not state)
        self.save_proxy_button.setHidden(not state)

    def load_config_from_file(self):
        if os.path.exists(self.CONFIG_FILE_PATH):
            with open(self.CONFIG_FILE_PATH, 'r') as config_file:
                config_data = json.load(config_file)
                saved_api_key = config_data.get('api_key')
                saved_proxy_enabled = config_data.get('proxy_enabled', False)
                self.saved_proxy_server = config_data.get('proxy_server', '')
                self.saved_proxy_port = config_data.get('proxy_port', '')
                from_language = config_data.get('from_language', '')
                to_language = config_data.get('to_language', '')

                from_index = self.from_language_dropdown.findText(from_language)
                to_index = self.to_language_dropdown.findText(to_language)

                if from_index != -1:
                    self.from_language_dropdown.setCurrentIndex(from_index)

                if to_index != -1:
                    self.to_language_dropdown.setCurrentIndex(to_index)

                if saved_api_key:
                    self.api_key_input.setText(saved_api_key)
                    self.set_api_key()

                if saved_proxy_enabled:
                    self.proxy_checkbox.setChecked(True)
                    self.proxy_server_input.setText(self.saved_proxy_server)
                    self.proxy_port_input.setText(self.saved_proxy_port)
                    self.toggle_proxy_settings(False)
                print(self.saved_proxy_server)
                print(self.proxy_port_input)

    def save_config_to_file(self):
        api_key = self.api_key_input.text().strip()
        proxy_enabled = self.proxy_checkbox.isChecked()
        proxy_server = self.proxy_server_input.text().strip()
        proxy_port = self.proxy_port_input.text().strip()

        from_language = self.from_language_dropdown.currentText()
        to_language = self.to_language_dropdown.currentText()

        config_data = {
            'api_key': api_key,
            'proxy_enabled': proxy_enabled,
            'proxy_server': proxy_server,
            'proxy_port': proxy_port,
            'from_language': from_language,
            'to_language': to_language
        }

        with open(self.CONFIG_FILE_PATH, 'w') as config_file:
            json.dump(config_data, config_file)

    def save_proxy_settings(self):
        proxy_server = self.proxy_server_input.text().strip()
        proxy_port = self.proxy_port_input.text().strip()
        if not proxy_server or not proxy_port:
            self.show_error_message("Please enter both proxy server and port.")
            self.proxy_checkbox.setChecked(False)
            return

        self.save_config_to_file()
        self.toggle_proxy_settings(False)

    def configure_proxy(self):
        if self.proxy_checkbox.isChecked():
            self.toggle_proxy_settings(True)
            proxy_server = self.proxy_server_input.text().strip()
            proxy_port = self.proxy_port_input.text().strip()

            self.client = openai.OpenAI(api_key=self.api_key, http_client=httpx.Client(proxies=f"http://{proxy_server}:{proxy_port}"))

        else:
            self.client = openai.OpenAI(api_key=self.api_key)
            self.toggle_proxy_settings(False)

    def run_regenerate_text(self):
        from_language = self.from_language_dropdown.currentText()
        to_language = self.to_language_dropdown.currentText()

        if not self.api_key_fixed:
            self.set_api_key()

        if self.radio_rephrase.isChecked():
            prompt = "Rephrase and improve the following text:"
        elif self.radio_debug_code.isChecked():
            prompt = "Debug the following code:"
        elif self.radio_explain.isChecked():
            prompt = "Explain the following text:"
        elif self.radio_summarize.isChecked():
            prompt = "Summarize the following text:"
        elif self.radio_translate.isChecked():
            prompt = f"Translate the following text from {from_language} to {to_language}:"
        elif self.radio_email.isChecked():
            prompt = "Write a reply to this email. Avoid wordy language:"
        elif self.radio_manual_prompts.isChecked():
            prompt = self.input_text.toPlainText()
        else:
            prompt = "Rephrase and improve the following text:"

        if self.checkbox_clipboard.isChecked():
            clipboard = QApplication.clipboard()
            prompt += " " + clipboard.text()

        elif not self.checkbox_clipboard.isChecked():
            prompt += " " + self.text_editor.toPlainText()

        elif not self.checkbox_clipboard.isChecked() and self.radio_manual_prompts.isChecked():
            prompt = self.input_text.toPlainText() + " " + self.text_editor.toPlainText()

        self.save_config_to_file()
        self.generate_response(prompt)

    def toggle_clipboard_text(self, state):
        self.text_editor.setHidden(state == Qt.Checked)

    def toggle_always_on_top(self):
        if self.windowFlags() & Qt.WindowStaysOnTopHint:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
            self.toggle_always_on_top_button.setStyleSheet(
                'background-color: #447ea3; min-width: 0px; font: 10.5pt;')
        else:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
            self.toggle_always_on_top_button.setStyleSheet(
                'background-color: #2ecc71; min-width: 0px; font: 10.5pt;')
        self.show()

    def set_api_key(self):
        self.api_key = self.api_key_input.text().strip()
        if self.api_key:
            try:
                self.api_key_fixed = True
                self.api_key_input.setReadOnly(True)
                self.set_widget_palette_color(self.api_key_input, '#e67e22')
            except openai.OpenAIError as err:
                self.show_api_key_error_alert(str(err))
        else:
            self.show_api_key_error_alert("Please enter a valid API key.")

        self.save_config_to_file()

    def generate_response(self, prompt):
        try:
            self.stop_generation = False
            full_text = ""
            block_color_status = 0
            self.configure_proxy()
            self.toggle_proxy_settings(False)

            for part in self.client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    model="gpt-3.5-turbo",
                    stream=True,
            ):

                if self.stop_generation:
                    break
                new_content = part.choices[0].delta.content or ""

                if block_color_status == 0:
                    if new_content.startswith("```"):
                        block_color_status = 1
                        new_content = new_content.replace('\n', '<br>')
                        full_text += '<font color="green">' + new_content + '</font>'
                    elif new_content.startswith("`"):
                        new_content = new_content.replace('\n', '<br>')
                        full_text += '<font color="green">' + new_content + '</font>'
                    else:
                        new_content = new_content.replace('\n', '<br>')
                        full_text += '<font color="white">' + new_content + '</font>'

                elif block_color_status == 1:
                    if new_content.startswith("``"):
                        block_color_status = 0
                    new_content = new_content.replace('\n', '<br>')
                    full_text += '<font color="green">' + new_content + '</font>'

                if new_content:
                    self.output_text.setHtml(full_text)

                self.output_text.verticalScrollBar().setValue(self.output_text.verticalScrollBar().maximum())

                QApplication.processEvents()

            code_blocks = re.findall(r"```([\s\S]+?)``", full_text)

            html_code = ''.join(code_blocks)

            soup = BeautifulSoup(html_code, 'html.parser')

            for br_tag in soup.find_all('br'):
                br_tag.replace_with('\n')

            plain_text = soup.get_text()

            language = ""
            for code_block in code_blocks:

                start_delimiter = '<font color="green">'
                end_delimiter = '</font>'

                start_index = code_block.find(start_delimiter)
                end_index = code_block.find(end_delimiter, start_index + len(start_delimiter))

                if start_index != -1 and end_index != -1:
                    language = code_block[start_index + len(start_delimiter):end_index]

                if language == "":
                    language = "python"

                print(language)

                lexer = get_lexer_by_name(language, stripall=True)
                formatter = HtmlFormatter(style="native", noclasses=True)
                highlighted_code = highlight(plain_text, lexer, formatter)
                try:
                    updated_html = full_text.replace('``</font><font color="green">`', '```')
                except:
                    updated_html = full_text

                full_text = updated_html.replace(f"```{code_block}```", highlighted_code)

            full_text = full_text.replace('<br><br></font><font color="green">',
                                          '<br></font><font color="green">')
            full_text = full_text.replace('</font><font color="green"><br><br>',
                                          '</font><font color="green">')

            self.output_text.setHtml(full_text)
            QApplication.processEvents()

        except openai.OpenAIError as err:
            self.output_text.setPlainText(str(err))

    def copy_text(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.output_text.toPlainText())

    def stop_generation_process(self):
        self.stop_generation = True

    def show_api_key_error_alert(self, error_message):
        alert = QMessageBox()
        alert.setWindowTitle("API Key Error")
        alert.setIcon(QMessageBox.Critical)
        alert.setText("Error setting API key:")
        alert.setInformativeText(error_message)
        alert.setStandardButtons(QMessageBox.Ok)
        alert.exec_()

    def show_error_message(self, message):
        error_message = QMessageBox()
        error_message.setWindowTitle("Error")
        error_message.setIcon(QMessageBox.Critical)
        error_message.setText(message)
        error_message.exec_()

    def set_widget_palette_color(self, widget, color):
        palette = widget.palette()
        palette.setColor(QPalette.WindowText, QColor(color))
        widget.setPalette(palette)

def main():
    app = QApplication(sys.argv)

    app_icon = QtGui.QIcon("icon.png")
    app.setWindowIcon(app_icon)

    app.setStyle('Fusion')

    ui = GPTUI()

    ui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
