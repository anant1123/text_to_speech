# app.py
from flask import Flask, render_template, request, send_file
from gtts import gTTS
import chardet
app = Flask(__name__)

# Specify the folder where uploaded files will be stored
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions for document uploads
ALLOWED_EXTENSIONS = {'txt', 'docx'}

# Function to check if a file has a valid extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tts', methods=['POST'])
def tts():
    text = request.form['text']
    uploaded_file = request.files['file']

    if text:
        content = text
    elif uploaded_file and allowed_file(uploaded_file.filename):
        # Determine the encoding dynamically
        raw_data = uploaded_file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']

        # Set a default encoding if chardet fails
        if encoding is None:
            encoding = 'utf-8'

        try:
            # Decode the content using the detected encoding
            content = raw_data.decode(encoding)
        except UnicodeDecodeError:
            # Handle the situation based on your requirements
            return f"Failed to decode the content with encoding {encoding}."

    else:
        return "Invalid input. Please enter text or upload a valid document file."

    language = 'en'
    tts = gTTS(text=content, lang=language, slow=False)

    # Save the audio file
    audio_filename = 'output.mp3'
    tts.save(audio_filename)

    return send_file(audio_filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
