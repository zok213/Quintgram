# MIT_CNN
This is the CNN model training code used to recognize user drawings in the AI-based fairy tale creation web service for children, 'My AI Fairy-Tale.'

[https://github.com/uvipen/QuickDraw](https://github.com/uvipen/QuickDraw) We applied the DeepSpeed library to the CNN training code from this repository and used more data for training.

- CNN
    Convolutional Neural Network (CNN). A model primarily used for image or video classification.

    Extracts feature maps from input images for classification purposes.

        -→ Uses far fewer parameters than DNNs and is robust against input data transformations.
        
- [Deepspeed](https://github.com/microsoft/DeepSpeed)
    An optimization library that accelerates PyTorch's computation and development speed.
    Allows effective use of GPU local memory with minimal code changes.
    Recommended for use with multiple GPUs rather than a single GPU... 🥲
    Since the model is simple, it can be omitted if desired.
- Data
    - [https://github.com/googlecreativelab/quickdraw-dataset](https://github.com/googlecreativelab/quickdraw-dataset)
    - Dataset provided by Google Creative Lab.
    - A dataset containing 50 million drawings across 345 classes.
    
- Usage
    - You can adjust the number of classes by modifying the num_classes in `src/model.py` and the CLASSES section in `src/config.py` 
    - The number of data samples per class used for training can be adjusted by modifying the total_image_per_class parameter in  `src/dataset.py` and `[train.py](http://train.py)` 
    - Various parameters such as batch size and max_epoch can be adjusted in  `deepspeedconfig.json`

```
python traincopy.py # Trains the model without using DeepSpeed. The traincopy.py file is the original training code from the referenced GitHub repository.
deepspeed train.py --deepspeed_config deepspeedconfig.json # Trains the model using DeepSpeed.
python modelsave.py # Loads the checkpoint file generated during training and saves it as a model.
```