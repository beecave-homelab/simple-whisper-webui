# Transcriptor

Transcriptor is a Flask-based web application that allows users to upload audio files and receive transcriptions. The app uses a service called Whisper (by [open ai](https://platform.openai.com/docs/guides/speech-to-text)), for processing the audio segments and transcribing them into text. Transcriptor works perfectly with locally hosted Whisper models, such as those provided by [localai.io](https://localai.io/features/audio-to-text/) 

## Table of Contents
- [Badges](#badges)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)
- [Contributing](#contributing)

## Badges
![Python](https://img.shields.io/badge/python-3.8-blue.svg)
![Flask](https://img.shields.io/badge/flask-1.1.2-blue.svg)
![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)

## Installation

To set up the project locally, follow these steps:

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/Transcriptor.git
    cd Transcriptor
    ```

2. **Create a virtual environment:**
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Run the application:**
    ```sh
    python app.py
    ```

## Usage

1. Open your web browser and navigate to `http://localhost:5000`.

2. Fill in the required fields:
   - **Domain:** The URL of the Whisper service (e.g., `http://localhost:8000`).
   - **Audio File:** Select the audio file you wish to transcribe.

3. Click the **Upload** button to start the transcription process.

4. Monitor the progress and wait for the transcription to complete. The transcript will be displayed on the page.

## License
![License](https://img.shields.io/badge/license-MIT-blue.svg)

This project is licensed under the MIT license. See [LICENSE](LICENSE) for more information.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Make sure to update tests as appropriate.

---

Feel free to reach out if you have any questions or need further assistance. Enjoy transcribing your audio files with Transcriptor!
