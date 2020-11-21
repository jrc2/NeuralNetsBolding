# 280 = tweet limit
import os
from tensorflow import keras
from tensorflow.keras import layers

import numpy as np
import random
import io

import csv

###############################################
# Model Version
###############################################
model_version = 1
model_name = f"model {model_version}"

###############################################
# Prepare The Data
###############################################
# Read in tweets from a text file
# text = open("tweets.txt", encoding="utf-8").read().lower()

# Read in as new CSV format
text = ""
with open ("test2.csv", newline="\n", encoding="utf-8") as CsvFile:
    reader = csv.reader(CsvFile, delimiter=",")
    for row in reader:
        text = text + row[1]

text = text.replace("\n", " ")
print("Length: ", len(text))

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
# Build The Model
###############################################

model = keras.Sequential(
    [
        keras.Input(shape=(maxlen, len(chars))),
        layers.LSTM(128, return_sequences=True),
        layers.LSTM(128, return_sequences=True),
        layers.Dropout(0.2),
        layers.LSTM(128, return_sequences=True),
        layers.LSTM(128),
        layers.Dense(len(chars), activation="softmax")
    ]
)

optimizer = keras.optimizers.RMSprop(learning_rate=0.01)
model.compile(loss="categorical_crossentropy", optimizer=optimizer)

###############################################
# Prepare the text sampling function
# We don't want the next character to be the one with the highest probability
# Because then  we'll get the same results every time
# So, we sample with a temperature parameter
#
# Temperature helps us not get the same text generate every time
# low temperature = text similar to trained data
# high temperature = more creative generation
# too high of a temperature = gibberish
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
epochs = 50
batch_size = 128

for epoch in range(epochs):
    model.fit(x, y, batch_size=batch_size, epochs=1)
    print()
    print(f"Generating text after epoch: {epoch}")

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

print(f"...End Of Run - Completed {epochs} Epochs")
# Additional print line to create space at bottom of terminal
print()

# model.save(f"models/{model_name}")

# Saving and loading models
# Saves a model in order to resume where it left off and avoid long traning times
# Saveing also means you can share your model and others can recreate your work.
# When publishing research models and techniques, most machine learning practictioners share:
# - code to create the model,
# - the trained weights, or parameters, for the model
# def get_model():
#     # Create a simple model.
#     inputs = keras.Input(shape=(32,))
#     outputs = keras.layers.Dense(1)(inputs)
#     model = keras.Model(inputs, outputs)
#     model.compile(optimizer=optimizer, loss="categorical_crossentropy")
#     return model


# model = get_model()

# Train the model.
# test_input = np.random.random((128, 32))
# test_target = np.random.random((128, 1))
# model.fit(test_input, test_target)

# Calling `save('my_model')` creates a SavedModel folder `my_model`.
# model.save("my_model")

# It can be used to reconstruct the model identically.
# reconstructed_model = keras.models.load_model("my_model")

# Let's check:
# np.testing.assert_allclose(
#     model.predict(test_input), reconstructed_model.predict(test_input)
# )

# The reconstructed model is already compiled and has retained the optimizer
# state, so training can resume:
# reconstructed_model.fit(test_input, test_target)

#########################################
# LAYERS FOR MODEL
########################################
# layers.LSTM(128, return_sequences=True),
# dropout helps prevent overfitting
# randomly sets input to 0 with a frequency of, lets say, 0.2 (whatever you pass in)
# layers.Dropout(0.2),
# layers.LSTM(128),
# layers.Dropout(0.2),
