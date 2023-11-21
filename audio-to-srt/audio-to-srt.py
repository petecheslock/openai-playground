from openai import OpenAI
import os

client = OpenAI()

sub_correction_prompt = 'subtitle-transcription-prompt.txt'
sub_transcription_prompt = 'subtitle-transcription-prompt.txt'

# Check if the file for subtitle correction prompt exists
if not os.path.isfile(sub_correction_prompt):
    # Raise an error if the file doesn't exist
    raise FileNotFoundError(f"""The file '{sub_correction_prompt}' does not exist. 
                            Please ensure the file is in the correct location.""")
else:
    # Open the file and read its content
    with open(sub_correction_prompt, 'r') as file:
        subtitle_correction_prompt = file.read()

# Check if the file for subtitle transcription prompt exists
if not os.path.isfile(sub_transcription_prompt):
    # Raise an error if the file doesn't exist
    raise FileNotFoundError(f"""The file '{sub_transcription_prompt}' does not exist. 
                            Please ensure the file is in the correct location.""")
else:
    # Open the file and read its content
    with open(sub_transcription_prompt, 'r') as file:
        transcription_prompt = file.read()

def get_filename_from_path(file_path):
    """
    Get the filename from a given file path.

    Parameters:
    file_path (str): The path of the file.

    Returns:
    file_name (str): The name of the file without extension.
    """
    base_name = os.path.basename(file_path)  # Get the filename with extension
    file_name, _ = os.path.splitext(base_name)  # Remove the extension
    return file_name

def transcribe(audio_file):
    """
    Create a transcription of an audio file and save it to a file.

    Parameters:
    audio_file (file): The audio file to transcribe.

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
        with open("original.srt", "w") as file:
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
                                  audio_file):
    """
    Generate a corrected transcript by first transcribing the audio file and then
    processing the transcription with an AI model.

    Parameters:
    temperature (float): The temperature parameter for the AI model, controlling the randomness of the output.
    subtitle_correction_prompt (str): The system prompt for the AI model, providing initial instructions.
    audio_file (file): The audio file to transcribe.
    original_transcript_file_name (str): The name of the file to write the original transcription to.

    Returns:
    corrected_transcript (str): The corrected transcription.
    None: If an error occurs during the transcription.
    """

    transcript = transcribe(audio_file)
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

    with open(get_filename_from_path(audio_file_path) + ".srt", "w") as file:
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

corrected_text = generate_corrected_transcript(0, subtitle_correction_prompt, audio)