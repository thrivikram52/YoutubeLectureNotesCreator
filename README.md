## YouTube Video to Lecture Notes

This project provides a script to download a YouTube video, Read its transcript, capture scenes from the video, summarize the transcript using OpenAI's GPT-4, and compile everything into a PDF document. Each page of the PDF contains a scene image, a summary of the transcript for that scene, and the full transcript text.

## Prerequisites

- Python 3.6 or higher
- pip (Python package installer)
- OpenAI API key

## Installation

1. **Clone this Repository**


2. **Create a Virtual Environment (Optional but Recommended)**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```sh
   pip install -r requirements.txt
   ```

   Create a `requirements.txt` file with the following content:

   ```text
   opencv-python
   pytube
   fpdf
   tqdm
   openai
   ```

## Configuration

1. **Set Up OpenAI API Key**

   Replace `'YOUR_OPENAI_API_KEY'` in the script with your actual OpenAI API key.

   ```python
   openai.api_key = 'YOUR_OPENAI_API_KEY'
   ```

2. **Set YouTube Video URL**

   Replace the YouTube URL in the script with the desired video URL.

   ```python
   youtube_url = 'https://www.youtube.com/watch?v=IpGxLWOIZy4'  # Replace with your YouTube URL
   ```

3. **Prepare Transcript File**
   **Install chrome extention youtube summary from the follwing link**
    
    https://chromewebstore.google.com/detail/youtube-summary-with-chat/nmmicjeknamkfloonkhhcjmomieiodli

   
   Create a `transcript.txt` file in the same directory as the script, and copy the transcript using the above extention on the you tube page and paste on the file.

   Example `transcript.txt`:

   ```text
   A Friendly Introduction to Machine Learning - YouTube
   (00:01) Hi and welcome to the machine learning course
   (00:35) machine learning is about...
   ```

## Usage

1. **Run the Script**

   ```sh
   python CreateLectureNotes.py
   ```

2. **Output**

   The script will generate a PDF file named `lecture_notes.pdf` in the current directory. This file contains the captured scenes, summaries, and full transcript text for each segment of the video.

