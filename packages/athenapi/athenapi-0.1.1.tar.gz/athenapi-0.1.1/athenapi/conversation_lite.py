from openai import AsyncOpenAI
import random
import string
import asyncio
import nltk
from nltk.tokenize import sent_tokenize
from athenapi.rpi0_iqaudio_board import Rpi0IQAudioBoard
from dotenv import load_dotenv
import os

load_dotenv()
client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def generate_random_text(length):
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for _ in range(length))
    return result_str


async def stt(recording_file):
    file = open(recording_file, "rb")
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


async def play_all_audios(queue, board):
    while True:
        file = await queue.get()
        if file is None:
            break
        board.play_audio(file)
        while board.is_playing():
            await asyncio.sleep(0.5)
        queue.task_done()


def main():
    asyncio.run(main_loop())


async def main_loop():
    nltk.download('popular')
    board = Rpi0IQAudioBoard()
    board.start()
    try:
        random_text = generate_random_text(100)
        recording_file = f'/tmp/{random_text}speech.wav'
        while True:
            board.recording(recording_file)
            msg = await stt(recording_file)
            queue = asyncio.Queue()
            await asyncio.gather(llm_tts(msg, queue), play_all_audios(queue, board))
    except KeyboardInterrupt:
        print("Finished")
    finally:
        print("Cleaning up")
        board.stop()


if __name__ == "__main__":
    main()
