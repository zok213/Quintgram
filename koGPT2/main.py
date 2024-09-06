import os
import logging
from transformers import AutoModelWithLMHead, PreTrainedTokenizerFast
from koGPT2_trainer import train_kogpt2_model
import text_preprocessing

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """
    Main function to load data, preprocess text, initialize tokenizer and model,
    and train the KoGPT2 model.
    """
    try:
        # Define the path to the data directory
        data_path = 'D:/Gitrepo/MIT_PJT-main/koGPT2'
        
        # Step 1: Read and preprocess the text data
        logging.info("Reading and cleaning text data...")
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Data path {data_path} does not exist.")
        
        raw_text = text_preprocessing.read_txt_files(data_path)
        cleaned_text = text_preprocessing.clean_text(raw_text)
        logging.info("Text data has been successfully preprocessed.")
        
        # Step 2: Initialize the tokenizer and model
        logging.info("Loading the tokenizer and model...")
        tokenizer = PreTrainedTokenizerFast.from_pretrained("skt/kogpt2-base-v2",
                                                            bos_token='</s>', eos_token='</s>', 
                                                            unk_token='<unk>', pad_token='<pad>', 
                                                            mask_token='<mask>') 
        
        model = AutoModelWithLMHead.from_pretrained("skt/kogpt2-base-v2")
        logging.info("Tokenizer and model successfully loaded.")

        # Step 3: Train the model
        logging.info("Starting the training process...")
        trained_model = train_kogpt2_model(cleaned_text, tokenizer, model)
        logging.info("Model training completed.")

    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    main()
