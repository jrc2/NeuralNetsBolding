from tensorflow import keras
from tensorflow.keras import layers

import numpy as np
import ast

import csv

import twitter_controller as twitter


def build_model():
    print("Building model...")
    model = keras.Sequential()
    model.add(layers.LSTM(256, return_sequences=True, input_shape=(tweet_sequence_length, len(chars))))
    model.add(layers.Dropout(0.2))
    model.add(layers.LSTM(512, return_sequences=True))
    model.add(layers.Dropout(0.2))
    model.add(layers.LSTM(256, return_sequences=True))
    model.add(layers.Dropout(0.2))
    model.add(layers.LSTM(128, return_sequences=True))
    model.add(layers.Dropout(0.2))
    model.add(layers.LSTM(64, return_sequences=False))
    model.add(layers.Dropout(0.2))
    model.add(layers.Dense(len(chars), activation="softmax"))
    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["acc"])
    print("Model built!\n")

    return model
  

###############################################
# Prepare the text sampling function
# We don't want the next character to be the one with the highest probability
# Because then  we"ll get the same results every time
# So, we sample with a temperature parameter
#
# Temperature helps us not get the same text generate every time
# low temperature = text similar to trained data
# high temperature = more creative generation
# too high of a temperature = gibberish
###############################################
def sample(predictions, temperature=0.5):
    predictions = np.asarray(predictions).astype("float64")
    predictions = np.log(predictions) / temperature
    exp_predictions = np.exp(predictions)
    predictions = exp_predictions / np.sum(exp_predictions)
    probabilities = np.random.multinomial(1, predictions, 1)
    return np.argmax(probabilities)


def train_model(model, num_epochs, should_save_model=False, model_save_name=""):
    print("Training mode...")
    batch_size = 128

    model.fit(inputs, labels, batch_size=batch_size, epochs=num_epochs)
    print(f"Finished training! Completed {num_epochs} epochs\n")

    if should_save_model:
        print(f"Saving model as {model_save_name}")
        model.save(model_save_name)
        print("Model saved!\n")
    else:
        print("Not saving model\n")

    return model


def generate_tweet(model, seed, tweet_length, post_to_twitter=False):
    diversity = 1.0

    generated_tweet = ""
    print("Generating Tweet based on: " + seed)

    for i in range(tweet_length):
        prediction = np.zeros((1, tweet_sequence_length, len(chars)))
        for t, char in enumerate(seed):
            prediction[0, t, chars_mapped_to_indicies[char]] = 1.0
        predictions = model.predict(prediction, verbose=0)[0]
        next_index = sample(predictions, diversity)
        next_char = indicies_mapped_to_chars[next_index]
        seed = seed[1:] + next_char
        generated_tweet += next_char

    print(generated_tweet + "\n")
    
    if (post_to_twitter):
        print("Posting Tweet...")
        twitter.post_tweet(generated_tweet)
        print("Tweet posted!\n")

    return generated_tweet


def get_tweets_from_csv(csv_file_name):
    print(f"Loading Tweets from {csv_file_name}")
    tweets = ""
    with open (csv_file_name, newline="\n") as csv_file:
        reader = csv.reader(csv_file, delimiter=",")
        for row in reader:
            binary_tweet = ast.literal_eval(row[1])
            tweets = tweets + binary_tweet.decode("utf-8")
            
    print("Tweets loaded!\n")
    
    return tweets


def set_inputs_and_labels(tweets):
    print("Setting inputs and labels")
    global inputs
    global labels
    step = 3
    tweet_sequences = []
    next_chars = []
    for i in range(0, len(tweets) - tweet_sequence_length, step):
        tweet_sequences.append(tweets[i : i + tweet_sequence_length])
        next_chars.append(tweets[i + tweet_sequence_length])

    inputs = np.zeros((len(tweet_sequences), tweet_sequence_length, len(chars)), dtype=np.bool)
    labels = np.zeros((len(tweet_sequences), len(chars)), dtype=np.bool)

    for i, tweet_sequence in enumerate(tweet_sequences):
        for t, char in enumerate(tweet_sequence):
            inputs[i, t, chars_mapped_to_indicies[char]] = 1
        labels[i, chars_mapped_to_indicies[next_chars[i]]] = 1
        
    print("Inputs and labels set!\n")




inputs = None
labels = None
chars = None
chars_mapped_to_indicies = None
indicies_mapped_to_chars = None
tweet_sequence_length = 40

#####
# MUST DO THIS BEFORE ANYTHING ELSE
#####
tweets = get_tweets_from_csv("tweets.csv")

chars = sorted(list(set(tweets)))
chars_mapped_to_indicies = dict((c, i) for i, c in enumerate(chars))
indicies_mapped_to_chars = dict((i, c) for i, c in enumerate(chars))

set_inputs_and_labels(tweets)
#####
# END STUFF YOU MUST DO FIRST
#####

#model = build_model()
#model = train_model(model, 1)
model = keras.models.load_model("my_model3.h5", compile=False)

generate_tweet(model, "COVID", 280)