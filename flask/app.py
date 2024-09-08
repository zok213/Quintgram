from flask import Flask, request, send_file, jsonify, session
from flask_cors import CORS
import json
import openai
import requests
import io
import random
import sys
import os
import cv2
import numpy as np
from transformers import AutoModelWithLMHead, PreTrainedTokenizerFast
import torch
import base64
import deepl
from TTS.api import TTS
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'CNN')))
sys.path.append(os.path.join(os.path.dirname(__file__), '../KoGPT2'))
from src.config import *
from src.dataset import CLASSES
from koGPT2_trainer import *

# Initialize Flask App
app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app, resources={r"/*": {"origins": ["http://192.168.1.8:3000", "http://127.0.0.1:3000"]}}, supports_credentials=True)

# Initialize DeepL Translator
DEEPL_API_KEY = ""  # Replace with your actual DeepL API Key
translator = deepl.Translator(DEEPL_API_KEY)

# Initialize Coqui TTS
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)

# Model Initialization (Load on GPU if available)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load the KoGPT2 model and tokenizer
tokenizer = PreTrainedTokenizerFast.from_pretrained("skt/kogpt2-base-v2",
                                                    bos_token='</s>', eos_token='</s>', unk_token='<unk>',
                                                    pad_token='<pad>', mask_token='<mask>')
model = AutoModelWithLMHead.from_pretrained("skt/kogpt2-base-v2").to(device)

class_dict = {'apple': '사과', 'book': '책', 'bowtie': '보타이', 'candle': '촛대', 'cloud': '구름', 'cup': '컵',
              'door': '문', 'envelope': '봉투', 'eyeglasses': '안경', 'guitar': '기타', 'hammer': '망치', 'hat': '모자',
              'ice cream': '아이스크림', 'leaf': '나뭇잎', 'scissors': '가위', 'star': '별', 't-shirt': '티셔츠',
              'pants': '바지', 'lightning': '번개', 'tree': '나무'}

# Global variables to store keywords and story
keyword_key = []
story_key = []
story_key_en = []

# Helper to manage user sessions
def get_session_id():
    if 'user_id' in session:
        return session['user_id']
    else:
        session['user_id'] = request.remote_addr
        return session['user_id']

@app.route('/post_data', methods=['POST'])
def post_data():
    user_id = get_session_id()
    data = request.get_json()

    # Decode the base64 image data
    image_data = data.get('image', '')
    image_64 = base64.b64decode(image_data.split(',')[1])
    image_array = np.frombuffer(image_64, np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_UNCHANGED)

    # Convert image to grayscale and resize
    _, _, _, alpha = cv2.split(image)
    image_gray = alpha
    img_resized = cv2.resize(image_gray, (28, 28))
    img_array = np.array(img_resized, dtype=np.float32)
    img_tensor = torch.from_numpy(np.expand_dims(np.expand_dims(img_array, axis=0), axis=0)).to(device)

    # Load pre-trained CNN model for image classification
    model = torch.load("D:\Gitrepo\MIT_PJT-main\CNN_trained\whole_model_MIT328", map_location=device)
    model.eval()

    # Perform prediction
    with torch.no_grad():
        logits = model(img_tensor)
        pred = torch.argmax(logits, dim=1).item()
        pred_class = CLASSES[pred]
        pred_class_kr = class_dict.get(pred_class, 'Unknown Objects')
        keyword_key.clear()
        keyword_key.append(pred_class_kr)

    app.logger.info(f'user_id: {user_id}, pred_class: {pred_class}, pred_class_kr: {pred_class_kr}')
    return jsonify({"prediction": pred_class})

@app.route('/get_story', methods=['POST'])
def get_story():
    user_id = get_session_id()

    prompt1 = "옛날 옛적에 " + keyword_key[0]
    prompt_ids1 = tokenizer.encode(prompt1)
    inp1 = torch.tensor(prompt_ids1).unsqueeze(0).to(device)

    max_iterations = 100
    generated_text1 = ""
    generated_text2 = ""
    generated_text3 = ""

    # First prompt generation
    for i in range(max_iterations):
        preds = model.generate(inp1,
                               max_length=20,
                               pad_token_id=tokenizer.pad_token_id,
                               eos_token_id=tokenizer.eos_token_id,
                               bos_token_id=tokenizer.bos_token_id,
                               repetition_penalty=2.0,
                               use_cache=True,
                               do_sample=True)
        generated_text1 = tokenizer.decode(preds[0], skip_special_tokens=True)
        if generated_text1[-1] in [".", "!", "?"]:
            break

    # Second prompt generation
    prompt_ids2 = tokenizer.encode(generated_text1)
    inp2 = torch.tensor(prompt_ids2).unsqueeze(0).to(device)

    for i in range(max_iterations):
        preds = model.generate(inp2,
                               max_length=40,
                               pad_token_id=tokenizer.pad_token_id,
                               eos_token_id=tokenizer.eos_token_id,
                               bos_token_id=tokenizer.bos_token_id,
                               repetition_penalty=2.0,
                               use_cache=True,
                               do_sample=True)
        generated_text2 = tokenizer.decode(preds[0], skip_special_tokens=True)
        if generated_text2[-1] in [".", "!", "?"]:
            break

    # Third prompt generation
    prompt_ids3 = tokenizer.encode(generated_text2)
    inp3 = torch.tensor(prompt_ids3).unsqueeze(0).to(device)

    for i in range(max_iterations):
        preds = model.generate(inp3,
                               max_length=70,
                               pad_token_id=tokenizer.pad_token_id,
                               eos_token_id=tokenizer.eos_token_id,
                               bos_token_id=tokenizer.bos_token_id,
                               repetition_penalty=2.0,
                               use_cache=True,
                               do_sample=True)
        generated_text3 = tokenizer.decode(preds[0], skip_special_tokens=True)
        if generated_text3[-1] in ["다.", "요.", "죠."]:
            break

    # Format the generated text
    final_story = generated_text3.replace(".", ". \n").replace("!", "! \n").replace("?", "? \n")

    # Split into sentences and store the first 10 sentences
    sentences = final_story.split(". \n")
    story_key.clear()
    for i in range(min(10, len(sentences))):
        sentence = sentences[i].strip() + "."
        story_key.append(sentence)

    if not story_key:
        return jsonify({"error": "Failed to generate story."}), 500

    # Translate to englishs
    translated_text = [translator.translate_text(text, target_lang="EN-US").text for text in story_key]
    story_key_en.clear()
    story_key_en.append(translated_text)

    app.logger.info(f'user_id: {user_id}, story_key: {story_key}, story_key_en: {story_key_en[0]}')
    return jsonify({"story": story_key_en[0][:-1]})


import os

@app.route('/get_data', methods=['POST'])
def get_data():
    user_id = get_session_id()

    openai.api_key ="" # Replace with your actual OpenAI API Key
    response = openai.Image.create(
        prompt=f"Draw an incredibly cute and adorable illustration featuring characters with {story_key_en[0][0]}",
        n=1, size="512x512"
    )

    if response and response['data'] and response['data'][0]['url']:
        image_url = response['data'][0]['url']
        image_data = requests.get(image_url).content
        image_io = io.BytesIO(image_data)

        # Ensure the directory exists
        save_dir = './image'
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # Save the image locally
        save_path = os.path.join(save_dir, 'new_image.png')
        with open(save_path, 'wb') as f:
            f.write(image_data)

    return send_file(image_io, mimetype='image/png', as_attachment=True, download_name='new_image.png')


@app.route('/get_voice', methods=['POST'])
def get_voice():
    user_id = get_session_id()

    # Generate TTS from the story
    story_text = ''.join(story_key[:-1])
    tts_output_path = './image/story_voice.wav'
    tts.tts_to_file(text=story_text, file_path=tts_output_path)

    return send_file(tts_output_path, mimetype='audio/wav', as_attachment=True, download_name='story_voice.wav')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
