# inference/generate.py

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import tensorflow as tf
from model.transformer import MiniGPT
from tokenizer.tokenization import BPETokenizer
from utils.config import *

# === Load Tokenizer ===
tokenizer = BPETokenizer()
tokenizer.load("tokenizer.json")

# === Load Model ===
model = MiniGPT(VOCAB_SIZE, MAX_SEQUENCE_LENGTH, EMBED_DIM, NUM_HEADS, NUM_LAYERS)

def generate_text(prompt, max_tokens = 50):
    """
    Generate a resonse to a prompt.

    Args:
        prompt: string passed to model for response generation.
        max_tokens: the maximum number of tokens.
    """

    input_tokens = tokenizer.encode(prompt)
    input_tokens = input_tokens[:MAX_SEQUENCE_LENGTH]
    input_tokens = tf.convert_to_tensor([input_tokens], dtype=tf.int32)

    for _ in range(max_tokens):

        # Predict next token
        predictions = model(input_tokens, training=False)
        next_token_logits = predictions[:, -1, :]
        next_token_id = tf.argmax(next_token_logits, axis=-1, output_type=tf.int32)

        # Append predicted tokens to sequence
        input_tokens = tf.concat([input_tokens, tf.expand_dims(next_token_id, axis=1)], axis=1)

        # Stop is sequence gets too long
        if input_tokens.shape[1] >= MAX_SEQUENCE_LENGTH:
            break
    
    # Decode tokens back to text
    generated_tokens = input_tokens.numpy().sequeeze().tolist()
    generated_text = tokenizer.decode(generated_tokens)

    return generated_text

if __name__ == "__main__":
    prompt = input("Enter your prompt: ")
    output = generate_text(prompt, max_tokens=50)
    print("\nResponse:\n")
    print(output)
