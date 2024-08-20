# :baby: Generate truyện cổ tích cho trẻ em, My AI Fairy-Tale 📖
<br>
</br>

<p align="center"><img src ="https://user-images.githubusercontent.com/119478998/228507228-d11276a3-f62d-4806-96d7-99826c7f3037.png"></p>

<div align="center">
Hello! This is My AI Fairy-Tale, a fairy tale creation service for children. <br> 
Draw a picture and Quintgram will make a fairy tale for you. Let's have fun making fairy tales with MIT!
</div>


## :information_desk_person: 서비스 소개
Trẻ em ngày nay tiêu thụ phương tiện truyền thông một cách thụ động, chỉ đơn giản là xem video trên điện thoại thông minh và máy tính bảng của chúng. Ngay cả trẻ 3 và 4 tuổi cũng tiêu thụ trung bình hơn 4 giờ 8 phút truyền thông, vượt xa thời gian khuyến nghị của WHO để tiêu thụ. Chúng tôi phát triển dịch vụ vì chúng tôi cảm thấy cần một dịch vụ mà trẻ em có thể tích cực tham gia, thay vì phương tiện truyền thông mà trẻ em tiêu thụ thụ động. 
My AI Fairy-Tale là một dịch vụ web sáng tạo có sự tham gia tạo ra những hình ảnh cổ tích và truyện cổ tích dựa trên những bức vẽ của trẻ em và đọc to chúng. Bằng cách tạo ra những câu chuyện cổ tích và hình vẽ mới làm say đắm trái tim trẻ em, nó được kỳ vọng sẽ đóng góp rất lớn vào sự phát triển cảm xúc của trẻ em.


🏠 [My AI Fairy-Tale Access Link]

🔎 프로젝트의 자세한 내용을 알고싶다면? [포트폴리오](https://github.com/Minju-nimm/MIT_PJT/blob/main/src/mit_presentaion.pdf)와 [보고서](https://github.com/Minju-nimm/MIT_PJT/blob/main/src/%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8_%EB%9E%A9%EC%97%85_%EB%A6%AC%ED%8F%AC%ED%8A%B8.pdf)를 참고하세요!

<br>
</br>

## 🗺️ Process Map
<img src="https://user-images.githubusercontent.com/119478998/228760864-3408c253-e957-499e-9e98-4b3df45aa1d3.png" width="800" height="500" />

<br>
</br>


## 🎥 Demonstration Video
Due to file size limitations, the original video has been uploaded to YouTube, where you can experience the actual loading time and voice services.

👉🏻 [ Click here to watch the full demonstration video! ](https://www.youtube.com/watch?v=IdmWXjR6ajg) 👈🏻
<br>
</br>

### 1. Service Guide
<img src="https://user-images.githubusercontent.com/119478998/228752379-ac0cdc14-d5e0-4014-935a-ef74564def43.gif" width="800" height="400" />
<br>
</br>

### 2. Drawing Recognition
<img src="https://user-images.githubusercontent.com/119478998/228748433-6366ac3d-2e8b-4c5e-a6d7-208a5bd8bee5.gif" width="800" height="400" />
<br>
</br>

### 3. Fairy Tale Generation
<img src="https://user-images.githubusercontent.com/119478998/228751099-122cf77c-48fa-4e5d-be71-7bcd4ecd1bf4.gif" width="800" height="400" />

<br>
</br>

## :computer: Installation
Each process has different requirements, so please refer to the README.md file for each process!

```bash
pip install -r requirements.txt
```
<br>
</br>

<div align="center">

![Pytorch](https://img.shields.io/badge/Pytorch-v1.13.1-orange?logo=Pytorch&style=plastic)
![NodeJS](https://img.shields.io/badge/Node.js-v18.14.2-339933?logo=node.js&style=plastic)
![react](https://img.shields.io/badge/react-v18.2.0-61dafb?logo=React&style=plastic)
![javascript](https://img.shields.io/badge/javascript-ES6-yellow?logo=javascript&style=plastic)

![Deepspeed](https://img.shields.io/badge/Deepspeed-v0.8.2+4ae3a3da-blue?logo=Deepspeed&style=plastic)
![Transformer](https://img.shields.io/badge/Transformer-v4.27.2-green?logo=Transformer&style=plastic)
![fastai](https://img.shields.io/badge/fastai-v2.7.11-orange?logo=fastai&style=plastic)

</div>

<br>
</br>

## 🛠 Architecture
<img src="https://user-images.githubusercontent.com/119478998/229721569-cc2b6136-b86f-4b3a-a8c1-b6108efc4395.png" width="900" height="400" />


## :deciduous_tree: Project Tree 
```bash
MIT_PJT
├── CNN
│   ├── Deepspeed
│   ├── src
│   ├── README.md
│   ├── deepspeeconfig.json
│   ├── modelsave.py
│   └── train.py
├── KoGPT2
│   ├── models
│   ├── README.md
│   ├── input_recursion.py
│   ├── inference.py
│   ├── main.py
│   ├── koGPT2_trainer.py
│   └── text_preprocessing.py
├── koGPT2_split
│   ├── RESULT
│   ├── models
│   ├── README.md
│   ├── inference.py
│   ├── main.py
│   ├── train.py
│   ├── txt_preprocessing.py
│   └── util.py
├── react
│   ├── public
│   └── src
├── flask
│   └── app.py
├── requirements.txt
└── README.md
```

<br>
</br>

## 🖱️ Usage
### CNN
```python
# Command to train with DeepSpeed
# Parameters like batch size and max_epoch can be adjusted in the deepspeedconfig.json file
deepspeed train.py --deepspeed_config deepspeedconfig.json 

# Command to train with regular torch
# After removing DeepSpeed code and setting parameters in get_args, use the following command
python train.py 
```

### koGPT2
```python
# Command to train the model
python koGPT2/main.py

# Command to generate fairy tales, requires the trained model
python koGPT2/inference.py
```

### Web Deployment and Execution
```node.js
# Command for bundling, optimizing, and obfuscating source code
npm run build

# Command to execute deployment
serve -s build
```

<br>
</br>

## 📂 Dataset
- [quickdraw-dataset](https://github.com/googlecreativelab/quickdraw-dataset)
<br>
</br>

## 📚 Reference
- https://www.yna.co.kr/view/AKR20210113064500005
- https://github.com/uvipen/QuickDraw
- https://github.com/microsoft/DeepSpeed
- https://github.com/boostcampaitech3/final-project-level3-nlp-06
- https://github.com/ttop32/KoGPT2novel
- https://openai.com/blog/dall-e/
- [React Redux](https://react-redux.js.org/)
