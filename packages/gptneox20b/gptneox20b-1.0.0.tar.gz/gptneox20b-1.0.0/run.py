# https://colab.research.google.com/drive/1Cngzh5VFrpDqtHcaCYFpW10twsuwGvGy?usp=sharing#scrollTo=D6xY7NlxbIIN

from transformers import GPTNeoXForCausalLM, GPTNeoXTokenizerFast
import torch

def main():
    print("blah blah blah")
    model = GPTNeoXForCausalLM.from_pretrained("EleutherAI/gpt-neox-20b", torch_dtype=torch.float32)
    print("ho ho ho")
    tokenizer = GPTNeoXTokenizerFast.from_pretrained("EleutherAI/gpt-neox-20b")

    input_text = "translate English to German: How old are you?"
    print("blah blah blah")

    gen_tokens = model.generate(
        tokenizer(input_text, return_tensors="pt").input_ids,
        do_sample=True,
        temperature=0.1,
        max_length=200,
        pad_token_id=tokenizer.eos_token_id
    )
    gen_text = tokenizer.batch_decode(gen_tokens)[0]
    print(gen_text)

if __name__ == "__main__":
    main()
