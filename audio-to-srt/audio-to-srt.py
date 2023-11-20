from openai import OpenAI
import os

client = OpenAI()

if not os.path.isfile('subtitle-correction-prompt.txt'):
    raise FileNotFoundError("The file 'prompt.txt' does not exist. Please ensure the file is in the correct location.")
else:
    with open('subtitle-correction-prompt.txt', 'r') as file:
        subtitle_correction_prompt = file.read()

if not os.path.isfile('subtitle-transcription-prompt.txt'):
    raise FileNotFoundError("The file 'prompt.txt' does not exist. Please ensure the file is in the correct location.")
else:
    with open('subtitle-transcription-prompt.txt', 'r') as file:
        transcription_prompt = file.read()

original_subtitle_file="old.srt"
corrected_subtitle_file="new.srt"

def transcribe(audio_file, output_file):
    """
    This function transcribes an audio file and saves the transcription to a specified file.

    Parameters:
    audio_file (file): The audio file to be transcribed.
    output_file (str): The name of the file where the transcription will be written.

    Returns:
    transcript (str): The transcription of the audio file.
    None: If an error occurs during the transcription.

    Raises:
    Exception: If there's an error during the transcription process.
    """
    try:
        # Create a transcription of the audio file using the whisper-1 model
        transcript = client.audio.transcriptions.create(
            prompt=transcription_prompt,
            model="whisper-1",
            file=audio_file,
            response_format="srt"
        )

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
                                  subtitle_correction_prompt,
                                  audio_file,
                                  original_transcript_file_name,
                                  corrected_transcript_file_name):
    """
    Generate a corrected transcript by first transcribing the audio file and then processing the transcription with an AI model.

    Parameters:
    temperature (float): The temperature parameter for the AI model, controlling the randomness of the output.
    subtitle_correction_prompt (str): The system prompt for the AI model, providing initial instructions.
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
                "content": subtitle_correction_prompt
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

corrected_text = generate_corrected_transcript(0, subtitle_correction_prompt, audio, original_subtitle_file, corrected_subtitle_file)
