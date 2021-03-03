# Asynchronous transcription: GCP's Speech to Text API

This repo contains a tool to transcribe audio files using Google Cloud Platform's Speech to Text asynchronous API.

## Setup

To test this, you need to have a GCP account. You can start a free trial with $300 GCP credits.

1. Create a new project or use an existing one and enable the Speech To Text API
2. [Create a service account](https://console.cloud.google.com/apis/credentials/serviceaccountkey) and save the config file provided
3. If you want to transcribe audio files in GCS (Google Cloud Storage), [create a new storage bucket](https://console.cloud.google.com/storage/browser).
4. Download or clone this repo
5. Copy your config file in the root folder and rename it *config.json*
6. Create a .env file in the root folder
7. (Optional) Create a python virtual environment
8. Run `pip install requirements.txt`

## Environment variables

In the .env file you created, paste this:

```
GOOGLE_APPLICATION_CREDENTIALS="config.json"
BUCKET_NAME="<YOUR_BUCKET_NAME>"
```

**Note:** If you don't want to use GCS, leave the bucket name blank

## Usage

To transcribe a file, run this:

```
python transcribe.py <mode> <file_path> <language>
```

The 2 modes available are 'gcs' and 'local'.  
With the gcs option the script will fetch audio files in GCS and with the local option the script will use local files.  
**Please note that local files cannot be longer than 1 minute.**

The file path either corresponds to your local file path or to the path in your storage bucket.

Language can either be 'fr' for French or 'en' for English. Feel free to modify the code to add any language you want, as long as it is [supported by the API](https://cloud.google.com/speech-to-text/docs/languages).

Please use a file in wav format for automatic detection of the settings (ideal rate 16000 Hz and needs to be monochannel). If you want to use another encoding, look at the [supported encodings](https://cloud.google.com/speech-to-text/docs/encoding) and [how to specify the settings](https://cloud.google.com/speech-to-text/docs/reference/rest/v1/RecognitionConfig).

### Examples

To transcribe a local file in French whose relative path is "test_files/test-stt-fr.wav" (checked in the repo), run 

```
python transcribe.py local "test_files/test-stt-fr.wav" fr
```

To transcribe a file in English at the root of your GCS bucket named "test-stt-en.wav", run 

```
python transcribe.py gcs "test-stt-en.wav" en
```

## Output

In the command line, you'll see the output split each time there is a pause.  
For each part, you'll see the transcription as well as the confidence level.  

The overall transcription is also saved in a txt file located in the *transcripts* directory.

