Here is the translated content of your `README.md` file:

# KoGPT2

## What is KoGPT2?
- A model trained on over 40GB of Korean corpus to improve the lacking Korean performance of GPT-2.
- [https://github.com/SKT-AI/KoGPT2](https://github.com/SKT-AI/KoGPT2)
- This project uses the `skt/kogpt2-base-v2` model.

## Tokenizer
- Uses the Character BPE tokenizer from the Huggingface [tokenizers](https://github.com/huggingface/tokenizers) package.
- The vocab size is 51,200, and it includes some commonly used emojis and emoticons.

    ```python
    > from transformers import PreTrainedTokenizerFast
    > tokenizer = PreTrainedTokenizerFast.from_pretrained("skt/kogpt2-base-v2",
      bos_token='</s>', eos_token='</s>', unk_token='<unk>',
      pad_token='<pad>', mask_token='<mask>')
    > tokenizer.tokenize("안녕하세요. 한국어 GPT-2 입니다.😤:)l^o")
    ['▁안녕', '하', '세', '요.', '▁한국어', '▁G', 'P', 'T', '-2', '▁입', '니다.', '😤', ':)', 'l^o']
    ```

## Data
- For KoGPT2, various data such as `Korean Wikipedia`, news, `Modu Corpus v1.0`, `Blue House National Petition` were used.
- The goal of this project is to train a model optimized for fairy tale generation using several `fairy tale data`.

    - Cheong Wa Dae - 100 Best Traditional Fairy Tales
    - Grimm's Fairy Tales Collection
    - Aesop's Fables Collection
    - tale.txt

  - Preprocessing
    - Remove the string between "(continued)" and "●" or "○".
    - Replace multiple spaces with a single space.
    - Delete strings enclosed in parentheses.
    - Delete address links.
    - Delete personal views of translators.

## Train
- Split learning model of fairy tale data (refer to koGPT2_Split for details).
- Full learning model of fairy tale data (final model selection).

## Usage

```python
# Model training command
python koGPT2/main.py

# Fairy tale generation execution command, requires trained model
python koGPT2/inference.py
```

Let me know if you need any further assistance or additional translations!
