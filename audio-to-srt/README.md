# Audio to Text Transcription

This Python script uses the OpenAI API to transcribe an audio file and then corrects the transcription using an AI model.

## What the script does

1. The script first checks if a file named 'subtitle-correction-prompt.txt' and 'subtitle-correction-prompt.txt' exist in the same directory. This file should contain the system prompt for the AI model and the subtitle creation model.
2. It then transcribes an audio file using the 'whisper-1' model from the OpenAI API.
3. The transcription is then processed by an AI model to generate a corrected transcript.

## Configuration

The script requires the following parameters:

- `temperature`: The temperature parameter for the AI model.
- `system_prompt`: The system prompt for the AI model. This is read from the 'prompt.txt' file.
- `audio_file`: The audio file to transcribe.

These parameters should be passed to the `generate_corrected_transcript` function.

## Usage

1. Make sure you have a file named 'subtitle-correction-prompt.txt' in the same directory as the script. This file should contain the system prompt for the AI model for correcting the text of the initial subtitle result.
2. Setup a virtual env:
   ```python -m venv .venv```
3. Activate it:
   ```source .venv/bin/activate```
4. Install requirements:
   ```pip install -r requirements.txt```
5. Run the script:
   ```python audio-to-srt.py```

## Dependencies

This script requires the OpenAI Python library.

