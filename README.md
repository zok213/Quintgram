![0908(2)-1 (1)](https://github.com/user-attachments/assets/aa3bbfbe-2955-4f85-a9e6-04169be4c2f2)![architecture](https://github.com/user-attachments/assets/d712bfd0-5fdf-4dd1-bb1d-a407a768bc77)
https://github.com/user-attachments/assets/cb22d269-73be-4a43-94b7-9e88ba91cd98
# :baby: Generate fairy tales for children, Quintgram 📖

<div align="center">
Hello! This is Quintgram educational comic generator, a fairy tale creation service for children. <br> 
Draw a picture and Quintgram will make a fairy tale for you. Let's have fun making fairy tales with MIT!
</div>


## :information_desk_person: Service Introduction
Today's children consume media passively, simply watching videos on their smartphones and tablets. Even 3- and 4-year-olds consume an average of more than 4 hours and 8 minutes of media, far exceeding the WHO's recommended time to consume. We developed the service because we felt the need for a service that children could actively participate in, rather than media that children passively consume. 
Quintgram educational comic generator is an innovative web service that engages in creating fairy tale images and fairy tales based on children's drawings and reading them aloud. By creating fairy tales and new drawings that captivate children's hearts, it is expected to make a huge contribution to children's emotional development.

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
<img src="https://github.com/user-attachments/assets/600cc919-8550-4140-95fd-19a8f2dfe26e" width="800" height="400" />
<br>
</br>

### 2. Drawing Recognition
<img src="https://github.com/user-attachments/assets/61f9fba3-15be-49a6-86ee-dc360c0cd821" width="800" height="400" />
<br>
</br>

### 3. Fairy Tale Generation
<img src="https://github.com/user-attachments/assets/275adf8d-4c2b-4e1c-9ad3-8316244f68a2" width="800" height="400" />

<br>
</br>

<br>
</br>

## 🛠 Architecture
<img src="https://github.com/user-attachments/assets/dc24aba9-3302-4b98-b399-727b6bab3614" width="900" height="400" />


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

