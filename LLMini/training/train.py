# training/train.py
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import tensorflow as tf
import numpy as np
from model.transformer import MiniGPT
from utils.config import *
from tokenizer.tokenization import BPETokenizer

# === Load and tokenize the corpus ===
tokenizer = BPETokenizer(vocab_size=VOCAB_SIZE)
if not Path("tokenizer.json").exists():
    tokenizer.train(["data/corpus.txt"], output_path="tokenizer.json")
else:
    tokenizer.load("tokenizer.json")

with open("data/corpus.txt", "r", encoding="utf-8") as f:
    text = f.read()

tokens = tokenizer.encode(text)
print(f"Tokenized {len(tokens):,} tokens.")

# === Prepare training sequences ===
input_seqs, target_seqs = [], []
for i in range(len(tokens) - CONTEXT_SIZE):
    input_seqs.append(tokens[i:i+CONTEXT_SIZE])
    target_seqs.append(tokens[i+1:i+1+CONTEXT_SIZE])

X = np.array(input_seqs, dtype=np.int32)
y = np.array(target_seqs, dtype=np.int32)

print(f"Created {len(X):,} training examples.")

# === Build dataset ===
dataset = tf.data.Dataset.from_tensor_slices((X, y))
dataset = dataset.shuffle(buffer_size=2048).batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)

# === Build model ===
model = MiniGPT(
    vocab_size=VOCAB_SIZE,
    context_size=CONTEXT_SIZE,
    embed_dim=EMBED_DIM,
    num_heads=NUM_HEADS,
    ff_dim=FFN_DIM,
    num_layers=NUM_LAYERS
)

model.compile(
    optimizer=tf.keras.optimizers.Adam(),
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=["accuracy"]
)

# === Train ===
model.fit(dataset, epochs=EPOCHS)

# === Save weights ===
model.save_weights("checkpoints/llmini_weights.h5")
print("Model weights saved to checkpoints/llmini_weights.h5")
