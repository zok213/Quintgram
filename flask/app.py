from flask import Flask, request , send_file, jsonify, session
from flask_cors import CORS
import json
import openai
import requests
import io
import random
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'CNN')))
sys.path.append(os.path.join(os.path.dirname(__file__), '../KoGPT2'))
from koGPT2_trainer import *
import cv2
import numpy as np
from src.config import *
from src.dataset import CLASSES
import torch
import base64
# from PIL import Image // Save image 
import urllib.request

import os
import sys

from transformers import AutoModelWithLMHead, PreTrainedTokenizerFast
from fastai.text.all import *


app = Flask(__name__)
CORS(app)
app.secret_key = ""

class_dict = {'apple': '사과', 'book': '책', 'bowtie': '보타이', 'candle': '촛대', 'cloud': '구름', 'cup': '컵',
'door': '문', 'envelope': '봉투', 'eyeglasses': '안경', 'guitar': '기타', 'hammer': '망치', 'hat': '모자',
'ice cream': '아이스크림', 'leaf': '나뭇잎', 'scissors': '가위', 'star': '별', 't-shirt': '티셔츠',
'pants': '바지', 'lightning': '번개', 'tree': '나무'}

keyword_key = [] # Global variable to enter Dali and story
story_key = [] # Global variables that tell a story
story_key_en = [] # A global variable that makes the story in English and puts it in Dali 

def get_session_id():
    if 'user_id' in session:
        return session['user_id']
    else:
        session['user_id'] = request.remote_addr
        return session['user_id']

# download model and tokenizer
tokenizer = PreTrainedTokenizerFast.from_pretrained("skt/kogpt2-base-v2",
                                                    bos_token='</s>', eos_token='</s>', unk_token='<unk>',
                                                    pad_token='<pad>', mask_token='<mask>') 
model = AutoModelWithLMHead.from_pretrained("skt/kogpt2-base-v2")

class TransformersTokenizer(Transform):
    def __init__(self, tokenizer): self.tokenizer = tokenizer
    def encodes(self, x): 
        toks = self.tokenizer.tokenize(x)
        return tensor(self.tokenizer.convert_tokens_to_ids(toks))
    def decodes(self, x): return TitledStr(self.tokenizer.decode(x.cpu().numpy()))

class DropOutput(nn.Module):
    def __init__(self, p=0.):
        super().__init__()
        self.p = p


@app.route('/post_data', methods=['POST',"GET"])
def post_data():
    if 'user_id' not in session:
        user_id = get_session_id()
        # Extract HTTP POST request data.
        data = request.get_json()
        image_data = data.get('image', '')
        # Restore image data from base64 string.
        image_64 = base64.b64decode(image_data.split(',')[1])
        image_array = np.frombuffer(image_64, np.uint8)
        # with open('./image/canvas_image.png', 'wb') as f:
        #     f.write(image_64)

        image = cv2.imdecode(image_array, cv2.IMREAD_UNCHANGED)
        _, _, _, alpha = cv2.split(image)
        image_gray = alpha

        # Model Code ------------------------------------------------------ from here
        # Resize the image to 28*28 size.
        img_resized = cv2.resize(image_gray, (28, 28))
        
        # Convert the image to a numpy array.
        img_array = np.array(img_resized, dtype=np.float32)

        # Make the image a four-dimensional input.
        img_tensor = np.expand_dims(img_array, axis=0)
        img_tensor = np.expand_dims(img_tensor, axis=0)

        # Convert the image to a pytorch tensor.
        img_tensor = torch.from_numpy(img_tensor)

        model = torch.load("D:\Gitrepo\MIT_PJT-main\CNN_trained\whole_model_quickdraw.txt", map_location=torch.device('cpu'))
        model.eval()

        with torch.no_grad():
            logits = model(img_tensor)
            pred = torch.argmax(logits, dim=1).item()
            pred_class = CLASSES[pred]
            pred_class_kr = class_dict.get(pred_class, '알 수 없는 객체')  # Convert the class name to Korean.
            keyword_key.clear()
            keyword_key.append(pred_class_kr)

        # Log the prediction results.
        app.logger.info(f'user_id: {user_id}, pred_class: {pred_class}, pred_class_kr: {pred_class_kr}')

        # Returns the prediction results to the client.
        return {"prediction": pred_class_kr}  


learn = load_learner('models\koGPT2_model_0322_4.pkl')
learn.model.cuda() # Moving the Model to the GPU

@app.route('/get_story', methods=['GET','POST'])
def get_story():
    if 'user_id' not in session:
        user_id = get_session_id()
        
        prompt1 = "옛날 옛적에 " + keyword_key[0]
        prompt_ids1 = tokenizer.encode(prompt1)
        inp1 = tensor(prompt_ids1)[None].cuda()
        
        prompt2 = ""
        max_iterations = 100

        for i in range(max_iterations):
            preds = learn.model.generate(inp1,
                                        max_length=20,
                                        pad_token_id=tokenizer.pad_token_id,
                                        eos_token_id=tokenizer.eos_token_id,
                                        bos_token_id=tokenizer.bos_token_id,
                                        repetition_penalty=2.0,
                                        use_cache=True,
                                        do_sample=True)

            generated_text = tokenizer.decode(preds[0].cpu().numpy())

        #  If the last character of a sentence is either a period, an exclamation mark, or a question mark, define it as the second prompt (prompt2)
            if generated_text[-1] in [".", "!", "?"]:
                prompt2 = generated_text
                break
            else:
                continue

        prompt_ids2 = tokenizer.encode(prompt2)
        inp2 = tensor(prompt_ids2)[None].cuda()

        prompt3 = ""

        for i in range(max_iterations):
            preds = learn.model.generate(inp2,
                                        max_length=40,
                                        pad_token_id=tokenizer.pad_token_id,
                                        eos_token_id=tokenizer.eos_token_id,
                                        bos_token_id=tokenizer.bos_token_id,
                                        repetition_penalty=2.0,
                                        use_cache=True,
                                        do_sample=True)

            generated_text2 = tokenizer.decode(preds[0].cpu().numpy())

        # If the last character of a sentence is a period, exclamation point, or question mark, define it as the second prompt (prompt3)
            if generated_text2[-1] in [".", "!", "?"]:
                prompt3 = generated_text2 
                break
            else:
                continue

        prompt_ids3 = tokenizer.encode(prompt3)
        inp3 = tensor(prompt_ids3)[None].cuda()

# Finally generate the text
        for i in range(max_iterations):
            preds = learn.model.generate(inp3,
                                        max_length=70,
                                        pad_token_id=tokenizer.pad_token_id,
                                        eos_token_id=tokenizer.eos_token_id,
                                        bos_token_id=tokenizer.bos_token_id,
                                        repetition_penalty=2.0,
                                        use_cache=True,
                                        do_sample=True)

            generated_text3 = tokenizer.decode(preds[0].cpu().numpy())

        # It ends when the last character of the sentence is one of the da., yo., and joe
        # if generated_text3[-1] in [".", "!", "?"]:
            if generated_text3[-1] in ["다.", "요.", "죠."]:
                generated_text3 = generated_text3
            else:
                continue

        generated_text3 = generated_text3.replace(".", ". \n").replace("!", "! \n").replace("?","? \n").replace("다.","다. \n").replace("요.","요. \n").replace("죠.","죠. \n")

        # .replace("! ", "!\n").replace("? ", "?\n")
        #Code to put stories from GPT into the story voice up to the nth sentence
        sentences = generated_text3.split(". \n")
        story_key.clear()
        for i in range(10):
            if i < len(sentences):
                sentence = sentences[i].strip() + "."
                story_key.append(sentence)

        if story_key:  # Prints only if the story key list is not empty
            print(f"스토리 키 : {story_key}")
        else:
            print("세 번째 마침표 이전의 문장을 찾을 수 없습니다.")

        

        # Translate story data to Dali Papago API
        client_id = ""
        client_secret = ""
        encText = urllib.parse.quote(story_key[0])# Translate the first sentence in the story and put it in Dali Even if you put the first sentence in it, the image and the story are similar.
        data = "source=ko&target=en&text=" + encText
        url = "https://naveropenapi.apigw.ntruss.com/nmt/v1/translation"
        request = urllib.request.Request(url)
        request.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
        request.add_header("X-NCP-APIGW-API-KEY",client_secret)
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        rescode = response.getcode()
        if(rescode==200):
            response_body = response.read()
            print(response_body.decode('utf-8'))
        else:
            print("Error Code:" + rescode)
        data = response_body

        # Code that receives only the translatedText portion of the received data
        parsed_data = json.loads(data)
        translated_text = parsed_data['message']['result']['translatedText'].replace('\n', ' ')
        print(f"translatedText 부분:{translated_text}")

        story_key_en.clear()
        story_key_en.append(translated_text) #Translate the story for Dali 
        
        app.logger.info(f'user_id: {user_id}, story_key: {story_key}, story_key_en: {story_key_en}')
        # Send the return in Korean
        return story_key[:-1]




@app.route('/get_data', methods=['GET','POST'])
def get_data():
    if 'user_id' not in session:
        user_id = get_session_id() # Utilize the user's IP address as the session ID.

        # Code to get the DALL-E API
        openai.api_key = ""
        openai.Model.list()
        response = openai.Image.create(
            prompt=f"Draw an incredibly cute and adorable illustration featuring characters with big, cheerful faces and small, adorable bodies that resemble babies. with{story_key_en[0]}",
            # story_key[0],keyword_key[0]
            n=1,
            size = "512x512"
        )
        if response and response.data and response.data[0].url:
            url = response.data[0].url
            image_data = requests.get(url).content

            # Convert image data to BytesIO objects.
            image_io = io.BytesIO(image_data)
            
            # Specify the file path and file name where you want to save the image.
            save_path = './image/new_image.png'
            
            # Save the image as a file.
            with open(save_path, 'wb') as f:
                f.write(image_data)
                
        app.logger.info(f'user_id: {user_id}, send_file: {send_file}')
        return send_file(image_io, mimetype='image/png', as_attachment=True, download_name='new_image.png')


@app.route('/get_voice', methods=['GET','POST'])
def get_voice():
    if 'user_id' not in session:
        user_id = get_session_id()# Utilize the user's IP address as the session ID.
        client_id = ""
        client_secret = ""
        story_text = ''.join(story_key[:-1])# Combine all string data in a story key into one
        encText = urllib.parse.quote(story_text,encoding="UTF-8") #story_kr
        data = f"speaker=ngoeun&volume=0&speed=0&pitch=0&format=mp3&text=" + encText
        url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"
        request = urllib.request.Request(url)
        request.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
        request.add_header("X-NCP-APIGW-API-KEY",client_secret)
        response = urllib.request.urlopen(request, data=data.encode('utf-8'))
        rescode = response.getcode()
        if(rescode==200):
            print("TTS mp3 저장")
            response_body = response.read()
            with open('./image/1111.mp3', 'wb') as f:
                f.write(response_body)
        else:
            print("Error Code:" + rescode)

        app.logger.info(f'user_id: {user_id}, send_file: {send_file}')
        return send_file("./image/1111.mp3", mimetype='audio/mpeg') 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3500, debug=True)