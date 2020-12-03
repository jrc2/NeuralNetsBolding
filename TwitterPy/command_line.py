import tweet_generator as generator
import twitter_controller as twitter


###########################################################
# Command line interface for the Tweet generator program. #
# by John Chittam and Andrew Young                        #
###########################################################


def is_string_empty(some_string):
    if some_string.strip() == "":
        return True
    return False


def is_file_name_valid(file_name):
    if (file_name[-3:] == ".h5" and len(file_name) >= 4):
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
    tweet_length = 0
    
    while(tweet_length < 1 or tweet_length > 280):
        try:
            tweet_length_as_string = input("Length must be a number between 1 and 280. Enter tweet length: ")
            tweet_length = int(tweet_length_as_string)
        except:
            tweet_length_as_string = input("Length must be a number between 1 and 280. Enter tweet length: ")
    
    return tweet_length  
  
  
def prompt_for_tweet_post():
    to_send_string = input("Would you like to post the generated Tweet? (yes/no) ")
    while to_send_string.lower() != "yes" and to_send_string.lower() != "no":
        to_send_string = input("Enter only 'yes' or 'no'. Would you like to post the generated Tweet? ")
        
    if to_send_string.lower() == "yes":
        return True
      
    return False


def prompt_for_model_file_name():
    model_file_name = input("Enter the save file name for model: ")
    while (is_file_name_valid(model_file_name) == False):
        print("File name must end with '.h5' and be >= 4 characters")
        model_file_name = input("Enter the save file name for model: ")
    return model_file_name


def prompt_for_tweet_seed():
    seed = input("Enter the tweet seed (40 characters works best): ")
    while (is_string_empty(seed) or len(seed) > 40):
        print("Tweet seed cannot be empty and must be <= 40 characters")
        seed = input("Enter the tweet seed: ")
        
    return seed


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

    if (option == "1"): # Generate dataset
        usernames = prompt_for_usernames()
        number_of_days = prompt_for_number_of_tweet_days()
        twitter.save_tweets(usernames, number_of_days, csv_file_name)
    elif (option == "2"): # Train and save model
        model_file_name = prompt_for_model_file_name()
        generator.build_train_save_model(csv_file_name, model_file_name)
    else: # Generate a Tweet
        model_file_name = prompt_for_model_file_name()
        tweet_seed = prompt_for_tweet_seed()
        tweet_length = prompt_for_tweet_length()
        to_post = prompt_for_tweet_post()
        
        generator.generate_tweet(csv_file_name, model_file_name, tweet_seed, tweet_length, to_post)
        

prompt_user_options()