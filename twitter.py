# 280 = tweet limit
from tensorflow import keras
from tensorflow.keras import layers

import numpy as np
import random
import io

###############################################
# PREPARE THE DATA
###############################################
# path = keras.utils.get_file('twitter.txt', "")
text = open("twitter.txt", encoding="utf-8").read().lower()

text = text.replace("\n", " ") # removing newlines for a nicer display
print("Length: ", len(text)) # making sure it's reading in

chars = sorted(list(set(text)))
print("Total Chars: ", len(chars))
char_indicies = dict((c, i) for i, c in enumerate(chars))
indicies_char = dict((i, c) for i, c in enumerate(chars))

# cut the text in semi-redundant sequences of maxlen characters
maxlen = 40
step = 3
sentences = []
next_chars = []
for i in range(0, len(text) - maxlen, step):
    sentences.append(text[i : i + maxlen])
    next_chars.append(text[i + maxlen])
print("Number of sequences ", len(sentences))

x = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        x[i, t, char_indicies[char]] = 1
    y[i, char_indicies[next_chars[i]]] = 1

###############################################
# Build the model: a single LTSM layer
###############################################
model = keras.Sequential(
    [
        keras.Input(shape=(maxlen, len(chars))),
        layers.LSTM(128),
        layers.Dense(len(chars), activation="softmax")
    ]
)
optimizer = keras.optimizers.RMSprop(learning_rate=0.01)
model.compile(loss="categorical_crossentropy", optimizer=optimizer)

###############################################
# Prepare the text sampling function
###############################################
def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype("float64")
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

###############################################
# Train the model
###############################################
epochs = 40
batch_size = 128

for epoch in range(epochs):
    model.fit(x, y, batch_size=batch_size, epochs=1)
    print()
    print("Generating text after epoch: %d % epoch")

    start_index = random.randint(0, len(text) - maxlen - 1)
    for diversity in [0.2, 0.5, 1.0, 1.2]:
        print("...Diversity: ", diversity)

        generated = ""
        sentence = text[start_index : start_index + maxlen]
        print("...Generating with seed: " + sentence + "''")

        for i in range(400):
            x_pred = np.zeros((1, maxlen, len(chars)))
            for t, char in enumerate(sentence):
                x_pred[0, t, char_indicies[char]] = 1.0
            preds = model.predict(x_pred, verbose=0)[0]
            next_index = sample(preds, diversity)
            next_char = indicies_char[next_index]
            sentence = sentence[1:] + next_char
            generated += next_char
        
        print("...Generated...", generated)
        print()