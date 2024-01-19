# pylint: disable=import-outside-toplevel

# https://colab.research.google.com/drive/1Cngzh5VFrpDqtHcaCYFpW10twsuwGvGy?usp=sharing#scrollTo=D6xY7NlxbIIN

import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--low-cpu-memory", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    import torch
    from transformers import GPTNeoXForCausalLM, GPTNeoXTokenizerFast

    model = GPTNeoXForCausalLM.from_pretrained(
        "EleutherAI/gpt-neox-20b",
        torch_dtype=torch.float32,
        low_cpu_mem_usage=args.low_cpu_memory,
    )
    tokenizer = GPTNeoXTokenizerFast.from_pretrained("EleutherAI/gpt-neox-20b")
    input_text = "translate English to German: How old are you?"
    print(f"Input text: {input_text}")
    gen_tokens = model.generate(
        tokenizer(input_text, return_tensors="pt").input_ids,
        do_sample=True,
        temperature=0.1,
        max_length=200,
        pad_token_id=tokenizer.eos_token_id,
    )
    gen_text = tokenizer.batch_decode(gen_tokens)[0]
    print(f"Generated text: {gen_text}")
    return 0


if __name__ == "__main__":
    main()
