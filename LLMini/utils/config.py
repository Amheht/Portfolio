# utils/config.py

# What: Vocabulary size.
# Why?: Number of unique tokens the model can recognize.
VOCAB_SIZE = 2048

# WHAT: Size of the token sequence fed to the model during training.
# WHY?: Size of each sample the model trains on at once.
CONTEXT_SIZE = 64

# What: Dimensionality of each token's embedding vector.
# Why?: How big is the learned 'meaning vector' for each token.
EMBED_DIM = 256

# What: Number of heads in multi-head attention.
# Why?: Number of different perspectives the model has when attending words.
NUM_HEADS = 4

# What: Number of transformer layers.
# Why?: Number of times the model transforms and refines the token information.
NUM_LAYERS = 4

# WHAT: Size of hidden layer inside each transformer's FFN.
# WHY?: How much processing power each token gets inside a block.
FFN_DIM = 1024

# WHAT: Number of sequences fed to the model at once during training.
# WHY?: Number of examples the model processes at one time during training.
BATCH_SIZE = 32

# WHAT: Number of full passes over the entire dataset during training.
# WHY?: Number of times the model sees all the training data.
EPOCHS = 10

# What: Max number of tokens model can handle in input or generated sequence.
# Why?: The longest sentence/chunk the model can understand at once.
MAX_SEQUENCE_LENGTH = 64
