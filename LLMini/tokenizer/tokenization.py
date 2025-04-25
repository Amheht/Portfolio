# tokenizer/tokenization.py
from tokenizers import Tokenizer, models, trainers, pre_tokenizers, normalizers
from pathlib import Path

class BPETokenizer:
    def __init__(self, vocab_size = 8192):
        self.vocab_size = vocab_size
        self.tokenizer = None

    def train(self, files, output_path = "tokenizer.json"):
        """
        
        Trains a Byte-Pair Encoding (BPE) tokenizer on the given text files.

        Args:
            files (list of str): Paths to text files.
            output_path (str): Path to save the trained tokenizer JSON.   
        """

        # Initialize tokenizer model
        bpe_model = models.BPE()
        tokenizer = Tokenizer(bpe_model)

        # Basic normalization & pre-tokenization
        tokenizer.normalizer  = normalizers.Sequence([
            normalizers.NFD(),
            normalizers.Lowercase(),
            normalizers.StripAccents()
        ])
        tokenizer.pre_tokenizer = pre_tokenizers.Whitespace()

        # Configure trainer
        trainer = trainers.BpeTrainer(
            vocab_size = self.vocab_size,
            show_progress = True,
            special_tokens = ["<pad>","<unk>", "<bos>", "<eos>"]
        )

        # Train the model
        tokenizer.train(files, trainer)
        tokenizer.save(output_path)
        self.tokenizer = tokenizer

    def load(self, path):
        """
        Load a previously saved tokenizer from path.
        """
        self.tokenizer = Tokenizer.from_file(path)

    def encode(self, text):
        """
        Encode a string into a list of token IDs.
        """
        return self.tokenizer.encode(text).ids

    def decode(self, ids):
        """
        Decode a list of token IDs back into text.
        """
        return self.tokenizer.decode(ids)
    
    def get_vocab_size(self):
        return self.tokenizer.get_vocab_size()
    
    def pad_id(self):
        return self.tokenizer.token_to_id("<pad>")
    
    def eos_id(self):
        return self.tokenizer.token_to_id("<eos>")
