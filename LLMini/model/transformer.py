# model/transformer.py
import tensorflow as tf
from tensorflow.keras import layers

class TokenAndPositionEmbedding(layers.Layer):
    def __init__(self, context_size, vocab_size, embed_dim):
        super().__init__()
        self.token_embed = layers.Embedding(input_dim=vocab_size, output_dim=embed_dim)
        self.pos_embed = layers.Embedding(input_dim=context_size, output_dim=embed_dim)

    def call(self, x):
        positions = tf.range(start=0, limit=tf.shape(x)[-1], delta=1)
        embedded_tokens = self.token_embed(x)
        embedded_positions = self.pos_embed(positions)
        return embedded_tokens + embedded_positions

class CausalSelfAttention(layers.Layer):
    def __init__(self, embed_dim, num_heads):
        super().__init__()
        self.attn = layers.MultiHeadAttention(num_heads=num_heads, key_dim=embed_dim)
        self.dropout = layers.Dropout(0.1)
        self.norm = layers.LayerNormalization()

    def causal_mask(self, x):
        seq_len = tf.shape(x)[1]
        return tf.linalg.band_part(tf.ones((seq_len, seq_len)), -1, 0)

    def call(self, x, training=False):
        mask = self.causal_mask(x)
        attn_out = self.attn(query=x, value=x, key=x, attention_mask=mask)
        x = self.norm(x + self.dropout(attn_out, training=training))
        return x

class TransformerBlock(layers.Layer):
    def __init__(self, embed_dim, num_heads, ff_dim):
        super().__init__()
        self.attn = CausalSelfAttention(embed_dim, num_heads)
        self.ffn = tf.keras.Sequential([
            layers.Dense(ff_dim, activation='relu'),
            layers.Dense(embed_dim),])
        self.dropout = layers.Dropout(0.1)
        self.norm = layers.LayerNormalization()

    def call(self, x, training=False):
        x = self.attn(x, training=training)
        ffn_out = self.ffn(x)
        return self.norm(x + self.dropout(ffn_out, training=training))


class MiniGPT(tf.keras.Model):
    def __init__(self, vocab_size, context_size, embed_dim, num_heads, ff_dim, num_layers):
        super().__init__()
        self.embed = TokenAndPositionEmbedding(context_size, vocab_size, embed_dim)
        self.blocks = [TransformerBlock(embed_dim, num_heads, ff_dim) for _ in range(num_layers)]
        self.norm = layers.LayerNormalization()
        self.out = layers.Dense(vocab_size)

    def call(self, x, training=False):
        x = self.embed(x)
        for block in self.blocks:
            x = block(x, training=training)
        x = self.norm(x)
        return self.out(x)
