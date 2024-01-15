import RPi.GPIO as GPIO
import time


class Button(object):
    def __init__(self, pin_num):
        button_pin = pin_num
        GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(button_pin, GPIO.BOTH,
                              callback=self._button_callback)
        self.is_button_pressed = False
        self.is_button_long_pressed = False
        self.press_time = None

    def _button_callback(self, channel):
        if GPIO.input(channel):
            self._button_rising_callback(channel)
        else:
            self._button_falling_callback(channel)

    def _button_rising_callback(self, channel):
        self.is_button_pressed = True
        if self.press_time is not None:
            if time.time() - self.press_time > 2:
                self.is_button_long_pressed = True
        self.press_time = None

    def _button_falling_callback(self, channel):
        self.press_time = time.time()

    def is_pressed(self):
        return self.is_button_pressed

    def is_long_pressed(self):
        return self.is_button_long_pressed

    def clear_state(self):
        self.is_button_pressed = False
        self.is_button_long_pressed = False
        self.press_time = None
