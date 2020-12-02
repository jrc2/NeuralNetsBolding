def is_string_empty(some_string):
    if some_string.strip() == "":
        return True
    return False

def is_file_name_valid(file_name):
    if (file_name[-3:] == ".h5"):
        return True
    return False

def is_valid_integer(num):
    try:
        int(num)
        return True
    except:
        return False

def prompt_for_csv_filename():
    csv_file_name = input("Enter the CSV filename: ")
    while (is_string_empty(csv_file_name) == True):
        print("Please enter a valid filename: ")
        csv_file_name = input("Enter the CSV filename: ")
    return csv_file_name

def prompt_for_usernames():
    usernames = input("Enter a list of usernames separated by a comma: ")
    while (is_string_empty(usernames)):
        print("Please enter (a) valid account name(s): ")
        usernames = input("Enter a list of usernames separated by a comma: ")
    return usernames.split(", ")

def prompt_for_number_of_tweet_days():
    number_of_days_as_string = input("Enter number of days of tweets to get: ")
    while (is_valid_integer(number_of_days_as_string) == False):
        print("Please enter a valid number: ")
        number_of_days_as_string = input("Enter number of days of tweets to get: ")
    
    number_of_days = int(number_of_days_as_string)
    return number_of_days

def prompt_for_tweet_length():
    tweet_length_as_string = input("Enter tweet length: ")
    while (is_valid_integer(tweet_length_as_string) == False):
        print("Please enter a valid number: ")
    tweet_length = int(tweet_length_as_string)
    return tweet_length

def prompt_for_model_file_name():
    model_file_name = input("Enter the save file name for model: ")
    while (is_file_name_valid(model_file_name) == False):
        model_file_name = input("Enter the save file name for model: ")
    return model_file_name

def prompt_for_tweet_seed():
    starting_sentence = input("Enter the tweet seed: ")
    while (is_string_empty(starting_sentence)):
        print("Please enter (a) valid account name(s): ")
        starting_sentence = input("Enter the tweet seed: ")

def prompt_user_options():
    print("Choose one of the following options:")
    print("----------------------------")
    print("1 - generate a dataset")
    print("2 - train and save model")
    print("3 - generate a tweet")
    print("----------------------------")
    option = input("Enter your option: ")
    valid_options = ["1", "2", "3"]
    while (option not in valid_options):
        print("Please enter a valid option: ")
        option = input("Enter your option: ")
        
    csv_file_name = prompt_for_csv_filename()
    print(csv_file_name)

    if (option == "1"):
        usernames = prompt_for_usernames()
        print(usernames)

        number_of_tweets = prompt_for_number_of_tweet_days()
        print(number_of_tweets)

        print("Generating a dataset...")
    elif (option == "2"):
        model_file_name = prompt_for_model_file_name()
        print(model_file_name)

        print("Training and saving model...")
    else:
        save_file_name = prompt_for_model_file_name()
        tweet_seed = prompt_for_tweet_seed()
        tweet_length = prompt_for_tweet_length()

        print("Generate tweet and send")

prompt_user_options()