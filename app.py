from flask import Flask, request, render_template, jsonify, send_from_directory, session
from pydub import AudioSegment
import requests
import os
import time

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for session handling

class Whisper:
    def __init__(self, domain, model):
        self.domain = domain
        self.model = model
        self.whole_response = []
        self.total_segments = 0

    def split_audio(self, file_path):
        session['messages'].append("Checking length of audio file.")
        audio = AudioSegment.from_file(file_path)
        segments = []
        segment_length_ms = 10 * 60 * 1000  # 10 minutes in milliseconds
        session['messages'].append(f"Cutting audio file into {len(audio) // segment_length_ms + 1} segments.")
        for start_ms in range(0, len(audio), segment_length_ms):
            end_ms = start_ms + segment_length_ms
            segment = audio[start_ms:end_ms]
            segments.append(segment)
        self.total_segments = len(segments)
        return segments

    def process_segment(self, segment_file_path, segment_number):
        try:
            session['messages'].append(f"Sending segment {segment_number + 1} of {self.total_segments} to Whisper.")
            with open(segment_file_path, "rb") as audio_file:
                files = {'file': audio_file}
                data = {'model': self.model}
                response = requests.post(f"{self.domain}/v1/audio/transcriptions", files=files, data=data)
                response.raise_for_status()
                self.whole_response.append(response.json().get('text', ''))
            session['messages'].append(f"Done with segment {segment_number + 1} of {self.total_segments}.")
        except Exception as e:
            session['messages'].append(f"Error processing segment {segment_number + 1}: {e}")

    def process_file(self, audio_file):
        try:
            segments = self.split_audio(audio_file)
            for i, segment in enumerate(segments):
                segment_file_path = f"uploads/segment_{i}.mp3"
                segment.export(segment_file_path, format="mp3")
                self.process_segment(segment_file_path, i)
                time.sleep(1)  # Simulate delay
            combined_transcript = ' '.join(self.whole_response)
            session['messages'].append("Transcript is ready.")
            return combined_transcript
        except Exception as e:
            session['messages'].append(f"Error: {e}")
            return ""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    session['messages'] = ["File successfully uploaded. Starting transcription process."]
    if 'audio_file' not in request.files or 'domain' not in request.form or 'model' not in request.form:
        return jsonify({"error": "No file, domain, or model provided"}), 400

    audio_file = request.files['audio_file']
    domain = request.form['domain']
    model = request.form['model']

    if audio_file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    file_path = os.path.join('uploads', audio_file.filename)
    audio_file.save(file_path)

    whisper = Whisper(domain, model)
    transcript = whisper.process_file(file_path)

    transcript_filename = os.path.splitext(audio_file.filename)[0] + '.txt'
    transcript_path = os.path.join('transcripts', transcript_filename)

    with open(transcript_path, 'w') as f:
        f.write(transcript)

    return jsonify({"transcript": transcript, "transcript_path": transcript_filename})

@app.route('/messages', methods=['GET'])
def messages():
    return jsonify(messages=session.get('messages', []))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    session['messages'] = ["Fetching uploaded file."]
    return send_from_directory('uploads', filename)

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    session['messages'] = ["Preparing file for download."]
    return send_from_directory('transcripts', filename)

if __name__ == "__main__":
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('transcripts', exist_ok=True)
    app.run(debug=True)
