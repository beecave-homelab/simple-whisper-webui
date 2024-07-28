from flask import Flask, request, render_template, jsonify, send_from_directory, session
from pydub import AudioSegment
import requests
import os
import time

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for session handling

class Whisper:
    def __init__(self, domain):
        self.domain = domain
        self.whole_response = []
        self.total_segments = 0
        self.progress_bar_value = 0

    def split_audio(self, file_path):
        audio = AudioSegment.from_file(file_path)
        segments = []
        segment_length_ms = 10 * 60 * 1000  # 10 minutes in milliseconds
        for start_ms in range(0, len(audio), segment_length_ms):
            end_ms = start_ms + segment_length_ms
            segment = audio[start_ms:end_ms]
            segments.append(segment)
        self.total_segments = len(segments)
        self.progress_bar_value = 100 / self.total_segments if self.total_segments else 0
        return segments

    def process_segment(self, segment_file_path):
        try:
            with open(segment_file_path, "rb") as audio_file:
                files = {'file': audio_file}
                data = {'model': 'whisper-large-q5_0'}
                response = requests.post(f"{self.domain}/v1/audio/transcriptions", files=files, data=data)
                response.raise_for_status()
                self.whole_response.append(response.json().get('text', ''))
        except Exception as e:
            print(f"Error: {e}")

    def process_file(self, audio_file):
        try:
            segments = self.split_audio(audio_file)
            for i, segment in enumerate(segments):
                segment_file_path = f"uploads/segment_{i}.mp3"
                segment.export(segment_file_path, format="mp3")
                self.process_segment(segment_file_path)
                session['progress'] = min(100, int((i + 1) * self.progress_bar_value))
                time.sleep(1)  # Simulate delay
            return ' '.join(self.whole_response)
        except Exception as e:
            print(f"Error: {e}")
            return ""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    session['progress'] = 0
    if 'audio_file' not in request.files or 'domain' not in request.form:
        return jsonify({"error": "No file or domain provided"}), 400

    audio_file = request.files['audio_file']
    domain = request.form['domain']

    if audio_file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    file_path = os.path.join('uploads', audio_file.filename)
    audio_file.save(file_path)

    whisper = Whisper(domain)
    transcript = whisper.process_file(file_path)

    transcript_filename = os.path.splitext(audio_file.filename)[0] + '.txt'
    transcript_path = os.path.join('transcripts', transcript_filename)

    with open(transcript_path, 'w') as f:
        f.write(transcript)

    return jsonify({"transcript": transcript, "transcript_path": transcript_filename})

@app.route('/progress', methods=['GET'])
def progress():
    return jsonify(progress=session.get('progress', 0))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory('transcripts', filename)

if __name__ == "__main__":
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('transcripts', exist_ok=True)
    app.run(debug=True)
