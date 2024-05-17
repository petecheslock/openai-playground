import glob
from openai import OpenAI
import sys
import os 

client = OpenAI()

def summarize_text(text):
    prompt = f"Summarize the following content into no longer than 160 characters for an Open Graph description field. The summary should be for improving SEO for a technical documentation site and you should ensure that AppMap is prominently featured:\n{text}"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
          {"role": "system", "content": "You are an expert in summarizing the English language to optimize for open graph descriptions for SEO, aiming for brevity and clarity. You need to ensure that your summary of any received text is approximately 150-160 characters but must not exceed 160 characters. It's better to have a summary less than 150 characters than over 160."},
          {"role": "user", "content": prompt}
        ],
        max_tokens=100,
        temperature=0.5
    )
    summary = response.choices[0].message.content.strip()
    print(f"Summary length: {len(summary)} characters")
    print(summary)
    return summary

def update_markdown_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    in_header = False
    description_present = False
    title_index = -1
    header_end_index = -1

    # Identify the header, check for description, and find insertion point for new description
    for i, line in enumerate(lines):
        if line.strip() == '---':
            if in_header:
                header_end_index = i
                break  # Exit after header is processed
            else:
                in_header = True
        elif in_header:
            if line.startswith('title:'):
                title_index = i
            elif line.startswith('description:'):
                description_present = True

    if description_present or title_index == -1:
        print(f"Skipping {file_path}. Description present or title not found.")
        return

    # Generate summary
    body = ''.join(lines[header_end_index+1:])  # Content after header
    summary = summarize_text(body).strip('"')

    # Insert the description after the title
    lines.insert(title_index + 1, f'description: "{summary}"\n')

    # Write the changes back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)
    print(f"Updated {file_path}")


def process_path(path):
    if os.path.isdir(path):
        matched_files_md = glob.glob(f"{path}/**/*.md", recursive=True)
        matched_files_markdown = glob.glob(f"{path}/**/*.markdown", recursive=True)
        matched_files_html = glob.glob(f"{path}/**/*.html", recursive=True)
        matched_files = matched_files_md + matched_files_markdown + matched_files_html
        print(f"Found {len(matched_files)} files.")
        for file in matched_files:
            print(f"Processing: {file}")
            update_markdown_file(file)
    elif os.path.isfile(path):
        print(f"Processing: {path}")
        update_markdown_file(path)
    else:
        print("Invalid path provided.")

if len(sys.argv) < 2:
    print("Please provide a directory path or a single md file path as a command line argument.")
    sys.exit(1)

path = sys.argv[1]
process_path(path)