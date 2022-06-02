import pathlib
import threading
import tkinter as tk
import tkinter.ttk as ttk
import pygubu

from libs.speech import SpeechRecognizer
from libs.search_web import WebSurfer
from loguru import logger
from threading import Thread
from utils import ColorConfig


PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / 'searchengine.ui'

MAINWINDOW       = 'mainwindow'
SEARCH_BUTTON    = 'search_button'
SPEAK_BUTTON     = 'speak_button'
SEARCH_ENTRY     = 'search_entry'
RESPONSE_TEXTBOX = 'response_textbox'


class App:
    WIDGETS = {
        MAINWINDOW: None, 
        SEARCH_BUTTON: None, 
        SPEAK_BUTTON: None, 
        SEARCH_ENTRY: None,
        RESPONSE_TEXTBOX: None
    }

    def __init__(self, master=None) -> None:
        self.builder = builder = pygubu.Builder()
        self.master = master

        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)

        for widget_key in self.WIDGETS:
            self.WIDGETS[widget_key] = builder.get_object(widget_key, master)
        
        builder.connect_callbacks(self)
        logger.debug('Connected callbacks for ui elements')

        self.WIDGETS[RESPONSE_TEXTBOX].config(state=tk.DISABLED)
        self.recognizer = SpeechRecognizer()
        self.color_config = ColorConfig('colors.json')

        self.WIDGETS[MAINWINDOW].config(
            bg=self.color_config.extra_color
        )

        self.WIDGETS[SEARCH_BUTTON].config(
            bg=self.color_config.secondary_color, 
            fg=self.color_config.extra_color
        )

        self.WIDGETS[SPEAK_BUTTON].config(
            bg=self.color_config.secondary_color, 
            fg=self.color_config.extra_color
        )

        self.WIDGETS[SEARCH_ENTRY].config(
            bg=self.color_config.primary_color
        )

        self.WIDGETS[RESPONSE_TEXTBOX].config(
            bg=self.color_config.primary_color
        )

    def search_button_pressed(self, event):
        text = self.WIDGETS[SEARCH_ENTRY].get()
        logger.debug(f'Searching for "{text}"')

        if text != '':
            self.WIDGETS[SEARCH_ENTRY].delete(0, tk.END)
            self.WIDGETS[RESPONSE_TEXTBOX].config(state=tk.NORMAL)
            self.WIDGETS[RESPONSE_TEXTBOX].delete('1.0', tk.END)
    
            self.recognizer.text_to_speech(f'Searching for "{text}"')
    
            response = WebSurfer.google_search_keywords(text)
            for link in response:
                self.WIDGETS[RESPONSE_TEXTBOX].insert(tk.END, f'{link}\n')
            self.WIDGETS[RESPONSE_TEXTBOX].config(state=tk.DISABLED)

    def speak_button_pressed(self, event):
        logger.debug('Listening for voice input')

        thread = Thread(target=self.search_with_voice)
        thread.start()

    def search_with_voice(self):
        text = self.recognizer.recognize_speech()
        logger.debug(f'Recognized {text}')

        if text:
            self.recognizer.text_to_speech(f'Searching for {text}')

            self.WIDGETS[RESPONSE_TEXTBOX].config(state=tk.NORMAL)
            self.WIDGETS[RESPONSE_TEXTBOX].delete('1.0', tk.END)

            response = WebSurfer.google_search_keywords(text)
            for link in response:
                self.WIDGETS[RESPONSE_TEXTBOX].insert(tk.END, f'{link}\n')
            self.WIDGETS[RESPONSE_TEXTBOX].config(state=tk.DISABLED)

    def run(self):
        self.WIDGETS[MAINWINDOW].mainloop()


if __name__ == '__main__':
    app = App()
    app.run()
