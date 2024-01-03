import json
import requests
import sys
from bs4 import BeautifulSoup
from openai import OpenAI

def main():
    print("Note ID: " + sys.argv[1])
    base_url = "https://note.com/api/v3/notes/"
    note_id = sys.argv[1]
    url = base_url + note_id
    response = requests.get(url)
    print("記事をダウンロードしました")
    data = json.loads(response.text)
    soup = BeautifulSoup(data["data"]["body"], "html.parser")
    for tag in soup.find_all("figure"):
        tag.decompose()
    text = soup.get_text("\n")
    print("MP3に変換しています")
    client = OpenAI()
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text,
    )
    response.stream_to_file(f"{note_id}.mp3")
    print("完了しました")

if __name__ == "__main__":
    main()