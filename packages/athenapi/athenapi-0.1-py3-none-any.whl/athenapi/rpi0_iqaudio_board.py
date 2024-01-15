import os
import re
import pyaudio
import RPi.GPIO as GPIO
from athenapi.rpi_button import Button
from athenapi.rpi_led import LED

class Rpi0IQAudioBoard(object):
    def __init__(self):
        GPIO.setmode(GPIO.BCM)

        self._button = Button(27)
        self._greenLED = LED(23)
        self._redLED = LED(24)
        self._recording_count = 0

        index = self._find_audio_device("IQaudIO")
        os.environ['AUDIODEV'] = f'hw:{index},0'
        print("audio device:index", index)

        info = pyaudio.PyAudio().get_default_input_device_info()
        print("Default input device: ", info)

    def _find_audio_device(self, pattern):
        pa = pyaudio.PyAudio()
        device_index = None
        for i in range(pa.get_device_count()):
            device_info = pa.get_device_info_by_index(i)
            device_name = device_info.get('name')
            if re.search(pattern, device_name):
                match = re.search(r'\(hw:(\d+),\d+\)', device_name)
                if match:
                    device_index = match.group(1)
                else:
                    device_index = i
                break
        pa.terminate()
        return device_index

    def start(self):
        self._greenLED.turn_on()

    def stop(self):
        self._greenLED.turn_off()
        GPIO.cleanup()

    def check_for_events(self, events):
        triggered_event = None
        for event in events:
            if event == 'toggle_recording':
                if self._button.is_pressed():
                    triggered_event = event
                    self._button.clear_state()
                    break

            if event == 'exit':
                if self._button.is_long_pressed():
                    triggered_event = event
                    self._button.clear_state()
                    break

        return triggered_event

    def on_recording_frame(self):
        if self._recording_count % 30 == 0:
            self._greenLED.toggle()

    def on_recording_finish(self):
        self._greenLED.turn_on()
