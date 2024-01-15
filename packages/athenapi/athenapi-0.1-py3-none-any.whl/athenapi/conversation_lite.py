import wave
from openai import AsyncOpenAI
import pyaudio
import pygame
import time
import random
import string
import re
import pkg_resources
import asyncio
import nltk
from nltk.tokenize import sent_tokenize
from athenapi.rpi0_iqaudio_board import Rpi0IQAudioBoard
from dotenv import load_dotenv
import os

load_dotenv()
client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))

beep_up = pkg_resources.resource_filename('athenapi', 'assets/beep-up.wav')
beep_down = pkg_resources.resource_filename('athenapi', 'assets/beep-down.wav')


def generate_random_text(length):
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for _ in range(length))
    return result_str


random_text = generate_random_text(100)

board = Rpi0IQAudioBoard()


def recording():
    global button
    global greenLED
    # Settings
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 256

    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    while True:
        triggered_event = board.check_for_events(['toggle_recording', 'exit'])

        if triggered_event == 'exit':
            print("Long press detected, exiting...")
            exit(0)

        if triggered_event is not None:
            break

        time.sleep(0.1)

    # Start recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True, start=False,
                        frames_per_buffer=CHUNK)

    play_audio(beep_up)

    count = 0
    frames = []
    stream.start_stream()

    print("Listening...")

    while True:
        triggered_event = board.check_for_events(['toggle_recording', 'exit'])
        if triggered_event == 'exit':
            print("Long press detected, exiting...")
            exit(0)

        if triggered_event is not None:
            break

        count += 1
        data = stream.read(CHUNK)
        frames.append(data)

        board.on_recording_frame()

    board.on_recording_finish()
    play_audio(beep_down)

    print('finish recording')

    # Stop recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
    print('stopped recording')

    # Write the WAV file
    with wave.open(f'/tmp/{random_text}speech.wav', 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))


async def stt():
    file = open(f"/tmp/{random_text}speech.wav", "rb")
    transcript = await client.audio.transcriptions.create(
        model="whisper-1",
        file=file
    )

    print(transcript.text)
    return transcript.text


messages = [
    {"role": "system", "content": "You are a helpful assistant. Your name is Athena Pi. You are having a voice conversation with a human. Make sure you response normally as how human would talk. And be concise and ask questions when needed."},
]


async def llm(message):
    user_message = {"role": "user", "content": message}
    stream = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            *messages,
            user_message
        ],
        stream=True)

    delta_content = ""
    async for chunk in stream:
        delta_content += chunk.choices[0].delta.content or ""
        sentences = sent_tokenize(delta_content)

        if len(sentences) > 1:
            yield sentences[0]
            delta_content = " ".join(sentences[1:])

    if (len(delta_content) > 0):
        yield delta_content


def find_audio_device(pattern):
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


def setup_pygame():
    pygame.init()
    pygame.mixer.init()


def play_audio(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():  # Wait for the audio to finish playing
        pygame.time.Clock().tick(10)


async def aplay_audio(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():  # Wait for the audio to finish playing
        await asyncio.sleep(0.5)


async def tts(reply):
    response = await client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=reply,
    )

    random_text_local = generate_random_text(100)
    file_name = f"/tmp/{random_text_local}streaming.mp3"
    response.stream_to_file(file_name)

    return file_name


async def llm_tts(msg, queue):
    async for sentence in llm(msg):
        print(sentence)
        file = await tts(sentence)
        await queue.put(file)

    await queue.put(None)


async def play_all_audios(queue):
    while True:
        file = await queue.get()
        if file is None:
            break
        await aplay_audio(file)
        queue.task_done()


def main():
    asyncio.run(main_loop())


async def main_loop():
    nltk.download('popular')
    board.start()
    setup_pygame()
    try:
        while True:
            recording()
            msg = await stt()
            queue = asyncio.Queue()
            await asyncio.gather(llm_tts(msg, queue), play_all_audios(queue))
    except KeyboardInterrupt:
        print("Finished")
    finally:
        print("Cleaning up")
        board.stop()


if __name__ == "__main__":
    main()
