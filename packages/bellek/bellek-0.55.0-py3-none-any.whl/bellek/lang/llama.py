# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/lang.llama.ipynb.

# %% auto 0
__all__ = ['prepare_llama2_for_training', 'prepare_llama2_for_inference', 'chat2text']

# %% ../../nbs/lang.llama.ipynb 3
def prepare_llama2_for_training(tokenizer, model):
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"  # Fix weird overflow issue with fp16 training
    model.config.pretraining_tp = 1
    model.config.use_cache = False

def prepare_llama2_for_inference(tokenizer, model):
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"  # Fix weird overflow issue with fp16 training
    model.config.use_cache = True

# %% ../../nbs/lang.llama.ipynb 4
def chat2text(example, key="conversations", tokenizer=None):
    if tokenizer is None:
        from transformers import AutoTokenizer

        tokenizer = AutoTokenizer.from_pretrained("NousResearch/Llama-2-7b-chat-hf")
    text = tokenizer.apply_chat_template(example[key], tokenize=False)
    return {"text": text}
