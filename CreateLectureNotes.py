import cv2
import os
from openai import OpenAI

client = OpenAI(api_key='YOUR_OPENAI_API_KEY')
from pytube import YouTube
from fpdf import FPDF
from tqdm import tqdm

# Set up OpenAI API key

class PDF(FPDF):
    def __init__(self, title, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = title

    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, self.title, 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def download_youtube_video(url, output_path='video.mp4', max_retries=3):
    yt = YouTube(url)
    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    total_size = stream.filesize
    print(f"Total video size: {total_size / (1024 * 1024):.2f} MB")

    for attempt in range(max_retries):
        try:
            stream.download(filename=output_path)
            print(f"Download completed successfully.")
            return output_path
        except Exception as e:
            print(f"Download attempt {attempt + 1} failed with error: {e}")
            if attempt + 1 == max_retries:
                raise
    return None

def format_transcript(transcript_data):
    formatted_transcript = []
    for entry in transcript_data:
        start = entry['start']
        duration = entry['duration']
        text = entry['text']
        formatted_transcript.append((start, start + duration, text))
    return formatted_transcript

def read_transcript(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    title = lines[0].strip()
    transcript = []
    for line in lines[1:]:
        if line.startswith('(') and ')' in line:
            try:
                parts = line.split(')')
                time_part = parts[0][1:].strip()
                text_part = parts[1].strip()
                if ':' in time_part:
                    minutes, seconds = map(int, time_part.split(':'))
                    start_time = minutes * 60 + seconds
                    transcript.append((start_time, text_part))
                else:
                    print(f"Skipping line with invalid timestamp format: {line}")
            except ValueError as e:
                print(f"Error processing line: {line}. Error: {e}")
        else:
            print(f"Skipping line with missing timestamp: {line}")
    return title, transcript

def capture_scene(video_path, timestamp):
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_MSEC, max(0, (timestamp - 1) * 1000))  # Ensure timestamp is non-negative
    ret, frame = cap.read()
    cap.release()
    return frame if ret else None

def summarize_text_chatgpt(text, max_length=40):
    response = client.chat.completions.create(model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant in writing the lecture notes for transcript. While generating the summary do not explicitly mention that, the text describes. Create natural sentences"},
        {"role": "user", "content": f"Summarize the following text in {max_length} words:\n\n{text}"}
    ],
    max_tokens=60,
    temperature=0.5)
    summary = response.choices[0].message.content.strip()
    return summary

def sanitize_text(text):
    return text.encode('latin-1', 'replace').decode('latin-1')

def create_pdf(transcript, video_path, output_pdf, title, output_folder='scenes'):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    pdf = PDF(title)
    pdf.set_left_margin(10)
    pdf.set_right_margin(10)

    # Progress bar for summarizing all transcripts
    with tqdm(total=len(transcript), desc="Summarizing transcript") as pbar:
        for i, (timestamp, text) in enumerate(transcript):
            scene = capture_scene(video_path, timestamp)
            if scene is not None:
                scene_filename = f'{output_folder}/scene_{i + 1:04d}.png'
                cv2.imwrite(scene_filename, scene)

                summary = summarize_text_chatgpt(text, max_length=40)
                pbar.update(1)

                pdf.add_page()
                pdf.set_xy(10, 10)
                pdf.set_font("Arial", size=14)
                pdf.image(scene_filename, 10, 20, 190)

                sanitized_summary = sanitize_text(summary)

                pdf.set_xy(10, 200)
                pdf.set_font("Arial", size=12)
                pdf.set_text_color(0, 0, 0)
                pdf.multi_cell(0, 10, sanitized_summary)

    pdf.output(output_pdf, "F")
    print(f'PDF created: {output_pdf}')

if __name__ == "__main__":
    youtube_url = 'https://www.youtube.com/watch?v=IpGxLWOIZy4'  # Replace with your YouTube URL
    #video_path = download_youtube_video(youtube_url)
    video_path = 'video.mp4'
    transcript_file_path = 'transcript.txt'
    output_pdf = 'lecture_notes.pdf'

    title, transcript_data = read_transcript(transcript_file_path)
    create_pdf(transcript_data, video_path, output_pdf, title)
