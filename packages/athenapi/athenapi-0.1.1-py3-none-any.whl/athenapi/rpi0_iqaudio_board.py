import time
import pkg_resources
import RPi.GPIO as GPIO
from athenapi.microphone import Microphone
from athenapi.rpi_button import Button
from athenapi.rpi_led import LED
from athenapi.speaker import Speaker

beep_up = pkg_resources.resource_filename('athenapi', 'assets/beep-up.wav')
beep_down = pkg_resources.resource_filename('athenapi', 'assets/beep-down.wav')

class Rpi0IQAudioBoard(object):
    def __init__(self):
        GPIO.setmode(GPIO.BCM)

        self._button = Button(27, press_callback=self._button_press_callback,
                              long_press_callback=self._button_long_press_callback)
        self._greenLED = LED(23)
        self._redLED = LED(24)
        self._speaker = Speaker('IQaudIO')
        self._microphone = Microphone()
        self._is_recording = False

    def _button_press_callback(self):
        self._is_recording = not self._is_recording

    def _button_long_press_callback(self):
        print("Long press detected, exiting...")
        exit(0)

    def start(self):
        self._greenLED.turn_on()

    def stop(self):
        self._greenLED.turn_off()
        self._microphone.stop()
        GPIO.cleanup()

    def recording(self, file_path):
        def should_stop():
            return not self._is_recording

        def on_start():
            self._speaker.play_audio(beep_up)
            

        while not self._is_recording:
            time.sleep(0.1)

        self._microphone.recording(file_path, should_stop, on_start)
        self._speaker.play_audio(beep_down)

    def play_audio(self, file_path):
        self._speaker.play_audio(file_path)

    def is_playing(self):
        return self._speaker.is_playing()
