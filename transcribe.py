import io
import logging
import sys
import os
from dotenv import load_dotenv
from google.cloud import speech


def save_transcript(filename, content, directory="transcripts"):
    """Saves the transcript as a txt file."""

    if not os.path.exists(directory):
        os.makedirs(directory)
    with io.open(f"{directory}/{filename}.txt", "w+") as transcript_file:
        transcript_file.write(content)

def split_newlines(content, n=64):
    """Splits a string every n characters by adding a newline."""

    content_newlines = '\n'.join(content[i:i+n] for i in range(0, len(content), n))

    return content_newlines


def transcribe_file(input_language, method, path, bucket_name):
    """Asynchronously transcribes the audio file specified."""

    if input_language == 'fr':
        language = 'fr-FR'
    else:
        language = 'en-US'

    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        language_code=language
    )

    # file on GCS
    if method == "gcs":
        audio = speech.RecognitionAudio(uri=f"{gs_uri_prefix}/{path}")
    # local file
    else:
        with io.open(path, "rb") as audio_file:
            content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    content = ""
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u"Transcript: {}".format(result.alternatives[0].transcript))
        print("Confidence: {}".format(result.alternatives[0].confidence))
        content += result.alternatives[0].transcript

    content_newlines = split_newlines(content)
    filename = path.split('/')[-1]
    save_transcript(filename, content_newlines)


if __name__ == "__main__":

    load_dotenv()
    method = sys.argv[1]
    audio_file_path = sys.argv[2]
    input_language = sys.argv[3]
    bucket_name = os.getenv("BUCKET_NAME")
    gs_uri_prefix = f"gs://{bucket_name}"

    transcribe_file(input_language, method, audio_file_path, gs_uri_prefix)
