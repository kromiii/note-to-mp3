import json
import requests
import sys
from bs4 import BeautifulSoup
from openai import OpenAI
from halo import Halo

def main():
    with Halo(text='記事をダウンロードしています', spinner='dots') as sp:
        base_url = "https://note.com/api/v3/notes/"
        note_id = sys.argv[1]
        url = base_url + note_id
        response = requests.get(url)
        sp.succeed()
    with Halo(text='テキストを抽出しています', spinner='dots') as sp:
        data = json.loads(response.text)
        soup = BeautifulSoup(data["data"]["body"], "html.parser")
        for tag in soup.find_all("figure"):
            tag.decompose()
        text = soup.get_text("\n")
        sp.succeed()
    with Halo(text='音声に変換しています', spinner='dots') as sp:
        client = OpenAI()
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text,
        )
        response.stream_to_file(f"{note_id}.mp3")
        sp.succeed()

if __name__ == "__main__":
    main()