import glob
from openai import OpenAI
import os

client = OpenAI()

def summarize_text(text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
          {"role": "system", "content": "You are an expert in summarizing the English language to optimize for open graph descriptions for SEO"},
          {"role": "user", "content": f"Summarize the following content in 155-160 characters optimized for an Open Graph description field:\n{text}"}
        ],
        max_tokens=100,
        temperature=0.5
    )
    summary = response.choices[0].message['content']
    print(summary)
    return summary

def update_markdown_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Assuming the header is separated by '---' from the content
    parts = content.split('---', 2)
    header = parts[1]
    body = parts[2] if len(parts) > 2 else ""

    # Check if a description is already present in the header
    if 'description:' in header:
        print(f"Skipping {file_path}, description already present.")
        return

    summary = summarize_text(body)

    # Insert the description into the header
    updated_header = header + f'\ndescription: "{summary}"\n'
    
    # Save the file with the updated header
    with open(file_path, 'w') as file:
        file.write(f"---{updated_header}---{body}")

def process_folder(folder_path):
    for md_file in glob.glob(f"{folder_path}/**/*.md", recursive=True):
        update_markdown_file(md_file)

# Example usage
folder_path = "/Users/petecheslock/repos/applandinc.github.io/_docs/integrations"
process_folder(folder_path)