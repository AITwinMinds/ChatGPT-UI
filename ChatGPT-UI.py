import os
import sys
import json
import re
import httpx
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QMessageBox, QRadioButton, QCheckBox,
    QTextEdit, QLabel, QComboBox
)
from PyQt5.QtGui import QPalette, QColor, QFont, QPixmap, QIcon
import openai
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import QtGui
from bs4 import BeautifulSoup
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from icon_binary_code import ICON_DATA

class GPTUI(QWidget):
    CONFIG_FILE_PATH = "config.json"

    def __init__(self):
        super().__init__()

        self.client = None
        self.api_key_fixed = False
        self.stop_generation = False
        self.base_resolution = (1920, 1080)
        self.screen_resolution = QApplication.desktop().screenGeometry()

        if self.screen_resolution.width() > self.screen_resolution.height():
            self.window_width_percentage = 38
            self.window_height_percentage = 56
            self.scaling_factor_width = self.screen_resolution.width() / self.base_resolution[0]
            self.scaling_factor_height = self.screen_resolution.height() / self.base_resolution[1]
        else:
            self.window_width_percentage = 56
            self.window_height_percentage = 38
            self.scaling_factor_width = self.screen_resolution.width() / self.base_resolution[1]
            self.scaling_factor_height = self.screen_resolution.height() / self.base_resolution[0]

        self.window_width = int(self.screen_resolution.width() * (self.window_width_percentage / 100))
        self.window_height = int(self.screen_resolution.height() * (self.window_height_percentage / 100))

        self.init_ui()
        self.load_config_from_file()
    def init_ui(self):
        self.setWindowTitle('ChatGPT')
        self.setGeometry(100, 100, self.window_width, self.window_height)

        icon_path = os.path.join(os.path.dirname(sys.executable), "icon.ico")
        if not os.path.exists(icon_path):
            with open(icon_path, "wb") as icon_file:
                icon_file.write(ICON_DATA)

        self.setWindowIcon(QIcon(icon_path))

        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(26, 29, 33))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(8, 68, 49))
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

        scrollbar_stylesheet = f"""
            QScrollBar:vertical {{
                border: 1px solid #041b20;
                background: #222529;
                width: {15 * self.scaling_factor_width}px;
                margin: {5 * self.scaling_factor_height}px 0 {5 * self.scaling_factor_height}px 0;
            }}

            QScrollBar::handle:vertical {{
                background: #0b4654;
                min-height: {30 * self.scaling_factor_height}px;  /* Adjust min-height for the handle */
                max-height: {30 * self.scaling_factor_height}px;  /* Adjust max-height for the handle */
            }}

            QScrollBar::add-line:vertical {{
                border: 1px solid #041b20;
                background: #073a43;  /* Change color for the add-line (down arrow) */
                height: {5 * self.scaling_factor_height}px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }}

            QScrollBar::sub-line:vertical {{
                border: 1px solid #041b20;
                background: #073a43;  /* Change color for the sub-line (up arrow) */
                height: {5 * self.scaling_factor_height}px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }}

            QScrollBar:horizontal {{
                border: 1px solid #041b20;
                background: #222529;
                height: {15 * self.scaling_factor_height}px;
                margin: 0 {5 * self.scaling_factor_width}px 0 {5 * self.scaling_factor_width}px;
            }}

            QScrollBar::handle:horizontal {{
                background: #0b4654;
                min-width: {30 * self.scaling_factor_width}px;  /* Adjust min-width for the handle */
                max-width: {30 * self.scaling_factor_width}px;  /* Adjust max-width for the handle */
            }}

            QScrollBar::add-line:horizontal {{
                border: 1px solid #041b20;
                background: #073a43;  /* Change color for the add-line (right arrow) */
                width: {5 * self.scaling_factor_width}px;
                subcontrol-position: right;
                subcontrol-origin: margin;
            }}

            QScrollBar::sub-line:horizontal {{
                border: 1px solid #041b20;
                background: #073a43;  /* Change color for the sub-line (left arrow) */
                width: {5 * self.scaling_factor_width}px;
                subcontrol-position: left;
                subcontrol-origin: margin;
            }}
        """

        input_layout = QHBoxLayout()

        self.api_key_input = QLineEdit(self)
        self.api_key_input.setPlaceholderText('Enter API key...')
        self.api_key_input.setFixedHeight(int(27 * self.scaling_factor_height))
        self.api_key_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: #222529;
                color: white;
                font-size: 11pt;
                min-height: {19 * self.scaling_factor_height}px;
                border: {1 * self.scaling_factor_width}px solid #565856;
                border-radius: {2 * self.scaling_factor_width}px;
            }}
        """)
        input_layout.addWidget(self.api_key_input)

        self.fix_api_key_button = QPushButton('Fix/Unfix API Key', self)
        self.fix_api_key_button.clicked.connect(self.toggle_api_key)
        input_layout.addWidget(self.fix_api_key_button)

        layout.addLayout(input_layout)

        self.toggle_always_on_top_button = QPushButton('Always On Top', self)
        self.toggle_always_on_top_button.clicked.connect(self.toggle_always_on_top)
        self.toggle_always_on_top_button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: #757777;
                border-color: #0f1c19;
                color: #000000;
                min-height: {19 * self.scaling_factor_height}px;
                font: 10.5pt Arial;
            }}
            """
        )
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
        prompt_layout.setAlignment(Qt.AlignLeft)
        layout.addLayout(prompt_layout)

        rephrase_options_layout = QHBoxLayout()
        rephrase_options_layout.setAlignment(Qt.AlignLeft)

        self.rephrase_options_dropdown = QComboBox(self)
        self.rephrase_options_dropdown.addItems(["Simplify", "Informal", "Professional", "Formal", "Generalize"])
        self.rephrase_options_dropdown.setCurrentIndex(0)
        self.rephrase_options_dropdown.setStyleSheet(
            f"""
            background-color: #073a43;
            border-color: #000000;
            color: #FFFFFF;
            min-height: {20 * self.scaling_factor_height}px;
            font: 10.5pt Arial;
            """
        )

        rephrase_options_layout.addWidget(self.rephrase_options_dropdown)
        self.rephrase_options_dropdown.currentIndexChanged.connect(self.set_rephrase_prompt)
        self.radio_rephrase.toggled.connect(self.toggle_radio_rephrase)
        self.set_rephrase_prompt(0)

        layout.addLayout(rephrase_options_layout)

        language_layout = QHBoxLayout()

        language_layout.setAlignment(Qt.AlignLeft)

        self.from_language_dropdown = QComboBox(self)

        self.from_language_dropdown.setStyleSheet(
            f"""
                background-color: #073a43;
                border-color: #000000;
                color: #FFFFFF;
                min-height: {20 * self.scaling_factor_height}px;
                font: 10.5pt Arial;
            """
        )
        self.to_language_dropdown = QComboBox(self)
        self.to_language_dropdown.setStyleSheet(
            f"""
                background-color: #073a43;
                border-color: #000000;
                color: #FFFFFF;
                min-height: {20 * self.scaling_factor_height}px;
                font: 10.5pt Arial;
            """
        )
        self.from_language_dropdown.setHidden(True)
        self.to_language_dropdown.setHidden(True)

        self.from_language_label = QLabel('From Language:', self)
        self.to_language_label = QLabel('To Language:', self)
        self.from_language_label.setHidden(True)
        self.to_language_label.setHidden(True)

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

        clipboard_email_detail_layout = QHBoxLayout()

        self.checkbox_clipboard = QCheckBox('Use last clipboard text', self)
        self.checkbox_clipboard.setChecked(True)

        clipboard_email_detail_layout.addWidget(self.checkbox_clipboard)

        self.checkbox_reply_to_email = QCheckBox('Provide specific information regarding the email response', self)
        self.checkbox_reply_to_email.setHidden(True)

        clipboard_email_detail_layout.addWidget(self.checkbox_reply_to_email)
        clipboard_email_detail_layout.setAlignment(Qt.AlignLeft)

        layout.addLayout(clipboard_email_detail_layout)

        editor_email_details_layout = QHBoxLayout()

        self.editor_email_details = QTextEdit(self)
        self.editor_email_details.setPlaceholderText('Add specific information to enhance the email prompt...')
        self.editor_email_details.setStyleSheet(
            f"""
                        QTextEdit {{
                            background-color: #222529;
                            color: white;
                            font-size: 11.5pt;
                            border: {1 * self.scaling_factor_width}px solid #565856;
                            border-radius: {4 * self.scaling_factor_width}px;
                            padding: {5 * self.scaling_factor_height}px;
                        }}
                        """
        )
        self.editor_email_details.setFixedHeight(int(100 * self.scaling_factor_height))
        self.editor_email_details.verticalScrollBar().setStyleSheet(scrollbar_stylesheet)
        self.editor_email_details.setHidden(True)
        editor_email_details_layout.addWidget(self.editor_email_details)

        layout.addLayout(editor_email_details_layout)

        self.checkbox_reply_to_email.stateChanged.connect(self.toggle_email_details_checkbox)
        self.radio_email.toggled.connect(self.toggle_email_details)
        self.toggle_email_details(False)

        self.input_text = QTextEdit(self)
        self.input_text.setPlaceholderText('Enter prompt manually...')
        self.input_text.setFixedHeight(int(70 * self.scaling_factor_height))
        self.input_text.setStyleSheet(
            f"""
            QTextEdit {{
                background-color: #222529;
                color: white;
                font-size: 11.5pt;
                border: {1 * self.scaling_factor_width}px solid #565856;
                border-radius: {4 * self.scaling_factor_width}px;
                padding: {5 * self.scaling_factor_height}px;
            }}
            """
        )
        self.input_text.verticalScrollBar().setStyleSheet(scrollbar_stylesheet)
        self.input_text.setHidden(True)
        layout.addWidget(self.input_text)

        self.text_editor = QTextEdit(self)
        self.text_editor.setPlaceholderText('Enter text manually...')
        self.text_editor.setStyleSheet(
            f"""
            QTextEdit {{
                background-color: #222529;
                color: white;
                font-size: 11.5pt;
                border: {1 * self.scaling_factor_width}px solid #565856;
                border-radius: {4 * self.scaling_factor_width}px;
                padding: {5 * self.scaling_factor_height}px;
            }}
            """
        )
        self.text_editor.setFixedHeight(int(150 * self.scaling_factor_height))
        self.text_editor.verticalScrollBar().setStyleSheet(scrollbar_stylesheet)
        self.text_editor.setHidden(True)
        layout.addWidget(self.text_editor)

        self.proxy_checkbox = QCheckBox('Enable HTTP proxy', self)
        self.proxy_checkbox.toggled.connect(self.configure_proxy)
        layout.addWidget(self.proxy_checkbox)

        self.proxy_input_layout = QVBoxLayout()
        self.proxy_server_input = QLineEdit(self)
        self.proxy_server_input.setPlaceholderText('Enter server address (e.g., 127.0.0.1)')
        self.proxy_server_input.setStyleSheet(
            f"""
            QLineEdit {{
                background-color: #222529;
                color: white;
                font-size: 11pt;
                border: {1 * self.scaling_factor_width}px solid #565856;
                border-radius: {2 * self.scaling_factor_width}px;
            }}
            """
        )
        self.proxy_server_input.setFixedHeight(int(27 * self.scaling_factor_height))
        self.proxy_server_input.setHidden(True)

        self.proxy_input_layout.addWidget(self.proxy_server_input)

        self.proxy_port_input = QLineEdit(self)
        self.proxy_port_input.setStyleSheet(
            f"""
            QLineEdit {{
                background-color: #222529;
                color: white;
                font-size: 11pt;
                border: {1 * self.scaling_factor_width}px solid #565856;
                border-radius: {2 * self.scaling_factor_width}px;
            }}
            """
        )
        self.proxy_port_input.setFixedHeight(int(27 * self.scaling_factor_height))
        self.proxy_port_input.setPlaceholderText('Enter port number (e.g., 10809)')
        self.proxy_port_input.setHidden(True)
        self.proxy_input_layout.addWidget(self.proxy_port_input)

        layout.addLayout(self.proxy_input_layout)

        self.save_proxy_button = QPushButton('Save proxy settings', self)
        self.save_proxy_button.clicked.connect(self.save_proxy_settings)
        self.save_proxy_button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: #073a43;
                border-color: #127287;
                color: #FFFFFF;
                min-height: {25 * self.scaling_factor_height}px;
                font: 10.5pt Arial;
            }}
            """
        )
        self.save_proxy_button.setFixedHeight(int(25 * self.scaling_factor_height))
        self.save_proxy_button.setHidden(True)
        layout.addWidget(self.save_proxy_button)

        self.checkbox_clipboard.stateChanged.connect(self.toggle_clipboard_text)

        self.radio_manual_prompts.toggled.connect(self.toggle_manual_prompt_input)

        self.proxy_checkbox.stateChanged.connect(self.configure_proxy)

        self.output_text = QTextEdit(self)
        self.output_text.setPlaceholderText('Response will appear here...')
        self.output_text.setStyleSheet(
            f"""
            QTextEdit {{
                background-color: #222529;
                color: white;
                font-size: 11.5pt;
                border: {1 * self.scaling_factor_width}px solid #565856;
                border-radius: {4 * self.scaling_factor_width}px;
                padding: {5 * self.scaling_factor_height}px;
            }}
            """
        )
        self.output_text.verticalScrollBar().setStyleSheet(scrollbar_stylesheet)
        self.output_text.horizontalScrollBar().setStyleSheet(scrollbar_stylesheet)

        layout.addWidget(self.output_text)

        button_layout = QHBoxLayout()

        self.run_regenerate_button = QPushButton('Generate', self)
        self.run_regenerate_button.clicked.connect(self.run_regenerate_text)
        self.run_regenerate_button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: #073a43;
                border-color: #127287;
                color: #FFFFFF;
                min-height: {27 * self.scaling_factor_height}px;
                font: 10.5pt Arial;
            }}
            """
        )
        self.run_regenerate_button.setFixedHeight(int(27 * self.scaling_factor_height))
        button_layout.addWidget(self.run_regenerate_button)

        self.copy_button = QPushButton('Copy response', self)
        self.copy_button.clicked.connect(self.copy_text)
        self.copy_button.setStyleSheet(
            f"""
            background-color: #073a43;
            border-color: #127287;
            color: #FFFFFF;
            min-height: {27 * self.scaling_factor_height}px;
            font: 10.5pt Arial;
            """)
        self.copy_button.setFixedHeight(int(27 * self.scaling_factor_height))
        button_layout.addWidget(self.copy_button)

        self.stop_button = QPushButton('Stop', self)
        self.stop_button.clicked.connect(self.stop_generation_process)
        self.stop_button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: #073a43;
                border-color: #127287;
                color: #FFFFFF;
                min-height: {27 * self.scaling_factor_height}px;
                font: 10.5pt Arial;
            }}
            """
        )
        self.stop_button.setFixedHeight(int(27 * self.scaling_factor_height))
        button_layout.addWidget(self.stop_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

        font = QFont()
        font.setFamily("Arial")
        font.setPointSizeF(11.5)
        self.setFont(font)

        self.from_language_dropdown.currentIndexChanged.connect(self.save_config_to_file)
        self.to_language_dropdown.currentIndexChanged.connect(self.save_config_to_file)

        self.load_config_from_file()
        if self.api_key_input.text() == "":
            self.api_key_fixed = True
            self.api_key_input.setReadOnly(False)
            self.fix_api_key_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: #757777;
                    border-color: #0f1c19;
                    color: #000000;
                    min-height: {19 * self.scaling_factor_height}px;
                    font: 10.5pt Arial;
                }}
            """)
        else:
            self.api_key_fixed = False
            self.api_key_input.setReadOnly(True)
            self.fix_api_key_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: #073a43;
                    border-color: #127287;
                    color: #FFFFFF;
                    min-height: {19 * self.scaling_factor_height}px;
                    font: 10.5pt Arial;
                }}
            """)
        print("Key is:", self.api_key_input.text())

    def toggle_email_details(self, state):
        self.checkbox_reply_to_email.setHidden(not state)
        if not self.radio_email.isChecked():
            self.editor_email_details.setHidden(not state)
            self.checkbox_reply_to_email.setChecked(False)

    def toggle_email_details_checkbox(self, state):
        self.editor_email_details.setHidden(not state)

    def set_rephrase_prompt(self, index):
        options = ["Simplify", "Informal", "Professional", "Formal", "Generalize"]
        selected_option = options[index]

        if selected_option == "Simplify":
            self.additionalPrompt = "Paraphrase the paragraph below. Simplify the language and maintain the core ideas:"
        elif selected_option == "Informal":
            self.additionalPrompt = "Rewrite the paragraph below in a more informal tone, without changing the core message:"
        elif selected_option == "Professional":
            self.additionalPrompt = "Can you suggest a different way to phrase paragraph below to make it sound more professional?:"
        elif selected_option == "Formal":
            self.additionalPrompt = "Rewrite the paragraph below in a more formal tone, without changing the core message:"
        elif selected_option == "Generalize":
            self.additionalPrompt = "Rewrite the technical paragraph below in simpler language, making it easily understandable for a general audience:"

    def toggle_language_dropdowns(self, checked):
        self.from_language_dropdown.setHidden(not checked)
        self.to_language_dropdown.setHidden(not checked)
        self.from_language_label.setHidden(not checked)
        self.to_language_label.setHidden(not checked)

    def toggle_radio_rephrase(self, checked):
        self.rephrase_options_dropdown.setHidden(not checked)

    def toggle_manual_prompt_input(self, checked):
        self.input_text.setHidden(not checked)
        if checked:
            self.input_text.setFocus()

    def toggle_api_key(self):
        if not self.api_key_input.text() == "":
            if self.api_key_fixed is False:
                self.api_key_fixed = True
                self.api_key_input.setReadOnly(False)
                self.fix_api_key_button.setStyleSheet(
                    f"""
                    QPushButton {{
                        background-color: #757777;
                        border-color: #0f1c19;
                        color: #000000;
                        min-height: {19 * self.scaling_factor_height}px;
                        font: 10.5pt Arial;
                    }}
                    """
                )
            else:
                self.api_key_fixed = False
                self.api_key_input.setReadOnly(True)
                self.api_key = self.api_key_input.text()
                self.fix_api_key_button.setStyleSheet(
                    f"""
                    QPushButton {{
                        background-color: #073a43;
                        border-color: #127287;
                        color: #FFFFFF;
                        min-height: {19 * self.scaling_factor_height}px;
                        font: 10.5pt Arial;
                    }}
                    """
                )

        else:
            self.fix_api_key_button.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: #757777;
                    border-color: #0f1c19;
                    color: #000000;
                    min-height: {19 * self.scaling_factor_height}px;
                    font: 10.5pt Arial;
                }}
                """
            )
        self.save_config_to_file()
    def toggle_proxy_settings(self, state):
        self.proxy_server_input.setHidden(not state)
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
                    self.api_key = saved_api_key

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

            try:
                self.client = openai.OpenAI(api_key=self.api_key, http_client=httpx.Client(proxies=f"http://{proxy_server}:{proxy_port}"))
            except:
                pass
        else:
            try:
                self.client = openai.OpenAI(api_key=self.api_key)
            except:
                pass
            self.toggle_proxy_settings(False)

    def run_regenerate_text(self):

        from_language = self.from_language_dropdown.currentText()
        to_language = self.to_language_dropdown.currentText()

        if self.api_key_fixed:
            self.set_api_key()

        if self.radio_rephrase.isChecked():
            prompt = self.additionalPrompt
        elif self.radio_debug_code.isChecked():
            prompt = "Help me to solve the issue and write updated code. Also explain what the issue was and what you did to fix it.\n\nCode:\n"
        elif self.radio_explain.isChecked():
            prompt = "Could you offer a clear and concise explanation for the following text, making it both simple and comprehensive?:"
        elif self.radio_summarize.isChecked():
            prompt = ("Could you please provide a concise and comprehensive summary of the given text? "
                      "The summary should capture the main points and key details of the text while conveying the author's intended meaning accurately. "
                      "Please ensure that the summary is well-organized and easy to read, with clear headings and subheadings to guide the reader "
                      "through each section. The length of the summary should be appropriate to capture the main points and key details of the text, "
                      "without including unnecessary information or becoming overly long. The response should not exceed the length of the main given text:\n")
        elif self.radio_translate.isChecked():
            prompt = f"Can you help me translate the following word/phrase/sentence from {from_language} to {to_language}?:"
        elif self.radio_email.isChecked():
            prompt = "Write a professional and productive reply to this email. Keeping it concise:\n\n"
            if self.checkbox_reply_to_email.isChecked():
                prompt = prompt[:-4]
                prompt += ".\nTake into account the following aspects when formulating the reply:\n\n"
                prompt += self.editor_email_details.toPlainText()
                prompt += "\n\nEmail:\n"
        elif self.radio_manual_prompts.isChecked():
            prompt = self.input_text.toPlainText()

        if self.checkbox_clipboard.isChecked():
            clipboard = QApplication.clipboard()
            prompt += " " + clipboard.text()

        elif not self.checkbox_clipboard.isChecked():
            prompt += " " + self.text_editor.toPlainText()

        elif not self.checkbox_clipboard.isChecked() and self.radio_manual_prompts.isChecked():
            prompt = self.input_text.toPlainText() + ": " + self.text_editor.toPlainText()

        self.save_config_to_file()

        self.run_regenerate_button.setEnabled(False)
        self.run_regenerate_button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: #4b4b4b;
                border-color: #4b4b4b;
                color: #a5a5a5;
                min-height: {27 * self.scaling_factor_height}px;
                font: 10.5pt Arial;
            }}
            """
        )
        self.run_regenerate_button.setText("Generating your response...")

        self.generate_response(prompt)

        self.run_regenerate_button.setEnabled(True)
        self.run_regenerate_button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: #073a43;
                border-color: #127287;
                color: #FFFFFF;
                min-height: {27 * self.scaling_factor_height}px;
                font: 10.5pt Arial;
            }}
            """
        )
        self.run_regenerate_button.setText("Generate")

    def toggle_clipboard_text(self, state):
        self.text_editor.setHidden(state == Qt.Checked)

    def toggle_always_on_top(self):
        if self.windowFlags() & Qt.WindowStaysOnTopHint:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
            self.toggle_always_on_top_button.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: #757777;
                    border-color: #0f1c19;
                    color: #000000;
                    min-height: {19 * self.scaling_factor_height}px;
                    font: 10.5pt Arial;
                }}
                """
            )
        else:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
            self.toggle_always_on_top_button.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: #073a43;
                    border-color: #0f1c19;
                    color: #FFFFFF;
                    min-height: {19 * self.scaling_factor_height}px;
                    font: 10.5pt Arial;
                }}
                """
            )
        self.show()

    def set_api_key(self):
        self.api_key = self.api_key_input.text()
        if self.api_key:
            e = openai.OpenAIError
            self.show_api_key_error_alert(str(e))
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

                lexer = get_lexer_by_name(language, stripall=True)

                formatter = HtmlFormatter(style="native", noclasses=True, nobackground=True)

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

        self.copy_button.setEnabled(False)
        self.copy_button.setText("Copied!")
        self.copy_button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: #04262c;
                border-color: #127287;
                color: #FFFFFF;
                min-height: {27 * self.scaling_factor_height}px;
                font: 10.5pt Arial;
            }}
            """
        )
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.clear_copied)
        self.timer.start(2000)

    def clear_copied(self):
        self.timer.stop()
        self.copy_button.setEnabled(True)
        self.copy_button.setText("Copy response")
        self.copy_button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: #073a43;
                border-color: #127287;
                color: #FFFFFF;
                min-height: {27 * self.scaling_factor_height}px;
                font: 10.5pt Arial;
            }}
            """
        )
    def stop_generation_process(self):
        self.stop_generation = True

    def show_api_key_error_alert(self, error_message):
        alert = QMessageBox()
        alert.setWindowTitle("API Key Error")
        alert.setIcon(QMessageBox.Critical)
        alert.setText("Error setting API key!")
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

    app_icon = QIcon(QPixmap.fromImage(QtGui.QImage.fromData(ICON_DATA)))
    app.setWindowIcon(app_icon)

    app.setStyle('Fusion')

    ui = GPTUI()

    ui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
