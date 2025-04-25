# LLMini

A miniature GPT-style language model, built from scratch in TensorFlow/Keras, trained on a set of Project Gutenberg books.

## Project Overview

This project demonstrates:
- Building a Transformer-based decoder model
- Tokenizing text with Byte-Pair Encoding (BPE)
- Training a language model end-to-end
- Text generation via sampling

Designed as a demonstration of deep learning and AI engineering skills.

---

## Project Structure

| Folder | Purpose |
|--------|---------|
| `model/` | Transformer decoder architecture (`MiniGPT`) |
| `tokenizer/` | Custom BPE tokenizer (subword learning) |
| `training/` | Training loop, dataset preparation |
| `inference/` | Prompt-based text generation |
| `scripts/` | Auxiliary scripts like corpus preparation |
| `utils/` | Shared constants and configuration |
| `data/` | Input texts and cleaned corpus |
| `checkpoints/` | Saved model weights |

---

## How to Run


### Open in Colab
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Amheht/LLMini/blob/main/miniGPT.ipynb)

### OR 1. Prepare Corpus
```bash
python scripts/prepare_corpus.py
