from loguru import logger

import pyttsx3
import speech_recognition as sr


class SpeechRecognizer:
    def __init__(self, device_index=0) -> None:
        self._recognizer = sr.Recognizer()
        self._microphone = sr.Microphone(device_index=device_index)

        self._text_engine = pyttsx3.init()
        logger.debug(f'Initialized a {self.__class__.__name__} object')        

    def recognize_speech(self) -> str | None:
        try:
            self.text_to_speech('Listening for a command')

            with self._microphone as source:
                self._recognizer.adjust_for_ambient_noise(source)
                audio = self._recognizer.listen(source, timeout=15)
                text = self._recognizer.recognize_google(audio)

                logger.debug(f'Recognized text: "{text}"')
        except Exception as e:
            logger.error(f'Exception caught, err: {e}')
            text = None
        finally:
            logger.debug('Returning vocal input')
            return text

    def text_to_speech(self, command):
        if command:
            logger.debug(f'Text-to-Speech text: {command}')
            
            self._text_engine.say(command)
            self._text_engine.runAndWait()

if __name__ == '__main__':
    recognizer = SpeechRecognizer(device_index=1)

    text = recognizer.recognize_speech()
    recognizer.text_to_speech(text)