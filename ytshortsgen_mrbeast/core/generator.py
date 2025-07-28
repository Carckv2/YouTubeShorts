
import openai

openai.api_key = "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"

def generate_title_description(transcript):
    prompt = f"Generate a viral YouTube Shorts title and a description from this transcript:
{transcript}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    text = response['choices'][0]['message']['content'].strip()
    parts = text.split('\n', 1)
    title = parts[0].strip()
    description = parts[1].strip() if len(parts) > 1 else ""
    return title, description
