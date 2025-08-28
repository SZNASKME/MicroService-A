from flask import Flask, request, jsonify
import os

app = Flask(__name__)

def simple_label(filename):
    ext = os.path.splitext(filename)[1].lower()
    if ext in ['.jpg', '.jpeg', '.png']:
        return 'image'
    elif ext in ['.pdf']:
        return 'document'
    elif ext in ['.docx', '.doc']:
        return 'word_document'
    elif ext in ['.xlsx', '.xls']:
        return 'excel_document'
    else:
        return 'other'

@app.route('/auto-label', methods=['POST'])
def auto_label():
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file uploaded'}), 400

    label = simple_label(file.filename)
    return jsonify({'filename': file.filename, 'label': label})

if __name__ == '__main__':
    app.run(debug=True)
