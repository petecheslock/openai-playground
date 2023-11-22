# Audio to Text Transcription

This Python script provides a way to transcribe an audio file and generate a corrected transcript using OpenAI's Whisper ASR model.  It then feeds the output of the audio transcription to GPT-4 in order to correct any spelling or grammar mistakes. 

## Dependencies
This script requires the openai Python library. You can install it using pip:

```
pip install openai
```

You'll need an API key from OpenAI to use their servcies. Once you have a key set it as an environment variable:

```
export OPENAI_API_KEY='your-api-key'
```

## What the script does

1. The script first checks if a file named 'subtitle-correction-prompt.txt' and 'subtitle-transcription-prompt.txt' exist in the same directory. This file should contain the system prompt for the AI model and the subtitle creation model.
2. It then transcribes an audio file using the 'whisper-1' model from the OpenAI API.
3. The transcription is then processed by GPT-4 AI model to generate a corrected transcript.

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
   ```python audio_to_srt.py```


## Output

The transcriptions are saved to files in SubRip (.srt) format. Both the original and post-processed transcriptions are saved for comparison. 

## Future ideas

1) Accept a youtube link
2) Parse audio from YT file
3) create a simple webfront end or API endpoint

