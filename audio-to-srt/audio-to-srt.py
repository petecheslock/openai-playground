from openai import OpenAI
import os

client = OpenAI()

if not os.path.isfile('prompt.txt'):
    raise FileNotFoundError("The file 'prompt.txt' does not exist. Please ensure the file is in the correct location.")
else:
    with open('prompt.txt', 'r') as file:
        system_prompt = file.read()


original_subtitle_file="old.srt"
corrected_subtitle_file="new.srt"

def transcribe(audio_file, output_file):
    """
    Create a transcription of an audio file and save it to a file.

    Parameters:
    audio_file (file): The audio file to transcribe.
    output_file (str): The name of the file to write the transcription to.

    Returns:
    transcript (str): The transcription of the audio file.
    None: If an error occurs during the transcription.
    """
    try:
        # Create a transcription of the audio file using the whisper-1 model
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="srt"
        )

        print(transcript.headers)

        # Open the output file in write mode
        with open(output_file, "w") as file:
            # Write the transcript to the file
            file.write(transcript)

        # Return the transcript
        return transcript
    except Exception as e:
        # Print an error message if an error occurs during the transcription
        print(f"An error occurred during transcription: {e}")
        # Return None if an error occurs
        return None


def generate_corrected_transcript(temperature,
                                  system_prompt,
                                  audio_file,
                                  original_transcript_file_name,
                                  corrected_transcript_file_name):
    """
    Generate a corrected transcript by first transcribing the audio file and then processing the transcription with an AI model.

    Parameters:
    temperature (float): The temperature parameter for the AI model, controlling the randomness of the output.
    system_prompt (str): The system prompt for the AI model, providing initial instructions.
    audio_file (file): The audio file to transcribe.
    original_transcript_file_name (str): The name of the file to write the original transcription to.
    corrected_transcript_file_name (str): The name of the file to write the corrected transcription to.

    Returns:
    corrected_transcript (str): The corrected transcription.
    None: If an error occurs during the transcription.
    """

    transcript = transcribe(audio_file, original_transcript_file_name)
    if transcript is None:
        return None

    response = client.chat.completions.create(
        model="gpt-4",
        temperature=temperature,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": transcript
            }
        ]
    )
    corrected_transcript = response.choices[0].message.content

    with open(corrected_transcript_file_name, "w") as file:
        file.write(corrected_transcript)

    return corrected_transcript

# Prompt the user to enter the path for the audio file
audio_file_path = input("Please enter the path for the audio file: ").strip("'")

# Check if the file exists
if not os.path.isfile(audio_file_path):
    print("The file does not exist.")
else:
    # Open the audio file
    audio = open(audio_file_path, "rb")

corrected_text = generate_corrected_transcript(0, system_prompt, audio, original_subtitle_file, corrected_subtitle_file)
