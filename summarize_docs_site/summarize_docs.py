import glob
from openai import OpenAI
import sys

client = OpenAI()

def summarize_text(text):
    prompt = f"Summarize the following content into no longer than 150 characters for an Open Graph description field. The summary should be for improving SEO for a technical documentation site:\n{text}"
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
          {"role": "system", "content": "You are an expert in summarizing the English language to optimize for open graph descriptions for SEO, aiming for brevity and clarity."},
          {"role": "user", "content": prompt}
        ],
        max_tokens=100,
        temperature=0.5
    )
    summary = response.choices[0].message.content.strip()
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


def process_folder(folder_path):
    matched_files = glob.glob(f"{folder_path}/**/*.md", recursive=True)
    print(f"Found {len(matched_files)} files.")
    for md_file in matched_files:
        print(f"Processing: {md_file}")
        update_markdown_file(md_file)


if len(sys.argv) < 2:
  print("Please provide a directory path as a command line argument.")
  sys.exit(1)

folder_path = sys.argv[1]
process_folder(folder_path)