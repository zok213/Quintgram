import torch
import torch.nn as nn
from transformers import GPT2LMHeadModel, PreTrainedTokenizerFast
from fastai.text.all import *

# Define TransformersTokenizer globally to avoid pickle issues
class TransformersTokenizer(Transform):
    def __init__(self, tokenizer): 
        self.tokenizer = tokenizer
    def encodes(self, x): 
        toks = self.tokenizer.tokenize(x)
        return tensor(self.tokenizer.convert_tokens_to_ids(toks))
    def decodes(self, x): 
        return TitledStr(self.tokenizer.decode(x.cpu().numpy()))

class DropOutput(Callback):
    def after_pred(self): 
        self.learn.pred = self.pred[0]

def train_kogpt2_model(lines: List[str], tokenizer: PreTrainedTokenizerFast, model: GPT2LMHeadModel):
    """
    Trains a GPT2LMHeadModel on the given lines and returns the trained model
    :param lines: List of strings, representing training data
    :param tokenizer: PreTrainedTokenizerFast, tokenizer used to encode the training data
    :param model: GPT2LMHeadModel, pre-trained model used as the basis for transfer learning
    :return: trained GPT2LMHeadModel
    """

    train = lines[:int(len(lines) * 0.8)]
    test = lines[int(len(lines) * 0.8):]
    splits = [[0], [1]]

    tls = TfmdLists([train, test], TransformersTokenizer(tokenizer), splits=splits, dl_type=LMDataLoader)
    batch, seq_len = 2, 256  
    dls = tls.dataloaders(bs=batch, seq_len=seq_len)

    learn = Learner(dls, model, loss_func=CrossEntropyLossFlat(), 
                    cbs=[DropOutput], metrics=Perplexity()).to_fp16()

    if torch.cuda.is_available():
        learn.model = learn.model.cuda()

    lr_min, lr_valley = learn.lr_find(suggest_funcs=(minimum, valley))
    print(f"Recommended Learning Rate: {lr_min}, Valley: {lr_valley}")

    learn.fit_one_cycle(5, lr_min)

    learn.export('./models/koGPT2_model_0322_4.pkl')

    return learn.model

