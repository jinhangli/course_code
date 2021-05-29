# -*- coding: utf-8 -*-
# @Time    : 2020-06-23 16:43
# @Author  : jinhang
# @File    : tweet_analysis.py
import pandas as pd
import preprocessing
import simpleanalysis
import emoji
from collections import OrderedDict
import plotanalysis
import ast

# setting for display
pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('max_colwidth', 100)


def data_clean_frequency_analysis(data, texts, emoji_path, hashtag_path, word_path, english_word_path, langs_path):
    """

    :param data:
    :param texts:
    :param emoji_path:
    :param hashtag_path:
    :param word_path:
    :param english_word_path:
    :param langs_path:
    :return:
    """
    emoji_dict_in_text = {}
    hashtags = []
    words = []
    english_words = []
    languages = dict()
    for i in range(0, len(texts)):
        print(i)
        # print(texts[i])
        emoji_dict_in_text_per, text_without_emoji = preprocessing.extract_remove_emojis(texts[i])
        for emoji_term in emoji_dict_in_text_per:
            if emoji_term not in emoji_dict_in_text:
                emoji_dict_in_text[emoji_term] = emoji_dict_in_text_per[emoji_term]
            else:
                emoji_dict_in_text[emoji_term][0] += emoji_dict_in_text_per[emoji_term][0]

        cleaned_text = preprocessing.clean_text(text_without_emoji)
        cleaned_text = preprocessing.remove_emoticons_and_contractions(cleaned_text)
        # print(cleaned_text)

        data.at[i, 'text'] = cleaned_text
        data.at[i, 'emoji_dict'] = str(emoji_dict_in_text_per)
        lang = data.at[i, 'lang']
        if lang == 'und':
            lang = preprocessing.language_detection(cleaned_text)
        else:
            lang = preprocessing.language_translation(lang)
        data.at[i, 'lang'] = lang

        if lang not in languages:
            languages[lang] = 1
        else:
            languages[lang] += 1

        if lang == "English":
            hashtags_per, words_per = preprocessing.tokenization_english(cleaned_text)
            english_words.extend(words_per)
        else:
            hashtags_per, words_per = preprocessing.tokenization_overall(cleaned_text)
        hashtags.extend(hashtags_per)
        words.extend(words_per)
    languages, types, values = simpleanalysis.language_statistics(languages=languages, write_path=langs_path)
    print("language types: {}, values:{}".format(types, values))

    emojis_voc_length, emojis_freq_list = simpleanalysis.emoji_frequency(emoji_dict_in_text)
    hashtags_freq_dict, hashtags_voc_length, hashtags_freq_list = simpleanalysis.word_frequency(hashtags)
    words_freq_dict, words_voc_length, words_freq_list = simpleanalysis.word_frequency(words)
    english_words_freq_dict, english_words_voc_length, english_words_freq_list = simpleanalysis.word_frequency(
        english_words)

    print(emojis_voc_length)
    print(hashtags_voc_length)
    print(words_voc_length)
    print(english_words_voc_length)

    simpleanalysis.write_frequency_list_to_file(emojis_freq_list, emoji_path)
    simpleanalysis.write_frequency_list_to_file(hashtags_freq_list, hashtag_path)
    simpleanalysis.write_frequency_list_to_file(words_freq_list, word_path)
    simpleanalysis.write_frequency_list_to_file(english_words_freq_list, english_word_path)


if __name__ == '__main__':
    ####################################################
    # deal with original data tweets                  ##
    # get cleaned des and emoji and language          ##
    # word, emoji, language, hashtag frequency analysis#
    ####################################################
    '''
    user_emojis_tweet_path = "data/UserEmojisTweets.csv"
    user_without_emojis_tweet_path = "data/UserWithoutEmojisTweets.csv"
    test_emoji_path = 'data/TweetTest1000.csv'

    tweets_columns = ['tweet_number_per_user', 'text', 'id', 'len', 'created_at', 'source',
                      'favorite_count', 'retweet_count', 'author_user_id', 'contributors',
                      'coordinates', 'entities', 'favorited', 'id_str',
                      'in_reply_to_screen_name', 'in_reply_to_status_id',
                      'in_reply_to_status_id_str', 'in_reply_to_user_id',
                      'in_reply_to_user_id_str', 'is_quote_status', 'lang', 'place',
                      'retweeted', 'truncated']

    data_path = user_emojis_tweet_path
    data = pd.read_csv(data_path, sep=',', dtype='unicode', lineterminator='\n', index_col=0)
    data.text.fillna('', inplace=True)
    texts = data.text

    user_tweet_emoji_path = "result/tweets/emoji_vocabulary_user_tweet_emoji.txt"
    user_tweet_hashtag_path = "result/tweets/hashtag_vocabulary_user_tweet_emoji.txt"
    user_tweet_word_path = "result/tweets/word_vocabulary_user_tweet_emoji.txt"
    user_tweet_english_word_path = "result/tweets/english_word_vocabulary_user_tweet_emoji.txt"
    user_tweet_langs_path = 'result/tweets/lang_in_user_tweet_emoji.json'

    without_user_tweet_emoji_path = "result/tweets/emoji_vocabulary_user_tweet_non_emoji.txt"
    without_user_tweet_hashtag_path = "result/tweets/hashtag_vocabulary_user_tweet_non_emoji.txt"
    without_user_tweet_word_path = "result/tweets/word_vocabulary_user_tweet_non_emoji.txt"
    without_user_tweet_english_word_path = "result/tweets/english_word_vocabulary_user_tweet_non_emoji.txt"
    without_user_tweet_langs_path = 'result/tweets/lang_in_user_tweet_non_emoji.json'

    data_clean_frequency_analysis(data, texts, user_tweet_emoji_path, user_tweet_hashtag_path,
                                  user_tweet_word_path, user_tweet_english_word_path,
                                  user_tweet_langs_path)
    data.to_csv("cleaned_data/UserEmojisTweets.csv")
    print(len(texts))
    # print(data)
    '''
    ####################################################
    # get and analysis new tweets                     ##
    ####################################################
    # user_emojis_tweet_path = "cleaned_data/UserEmojisTweets.csv"
    # user_without_emojis_tweet_path = "cleaned_data/UserWithoutEmojisTweets.csv"
    # test_emoji_path = 'cleaned_data/TweetTest1000.csv'
    #
    # tweet_data = pd.read_csv(user_emojis_tweet_path, sep=',', dtype='unicode', lineterminator='\n', index_col=0)
    # cleaned_tweet_columns = ['tweet_number_per_user', 'text', 'id', 'len', 'created_at', 'source',
    #                          'favorite_count', 'retweet_count', 'author_user_id', 'favorited',
    #                          'id_str', 'in_reply_to_screen_name', 'in_reply_to_status_id_str',
    #                          'in_reply_to_user_id_str', 'is_quote_status', 'lang', 'place',
    #                          'retweeted', 'truncated', 'hashtags', 'emoji_dict']

    '''plot language distribution'''
    # plotanalysis.value_count_bar(tweet_data.lang, rot_value=70,
    #                              title_value='Top 10 language distribution of tweets\n'
    #                                          '(%s tweets from users with emoji in the '
    #                                          'descriptions)' % len(tweet_data),
    #                              xlabel_value='language', ylabel_value='count',
    #                              path='result/tweets/lang_user_tweet_emoji.png', number=10, percentage=True)

    '''draw english word cloud'''
    # word_voc_user_tweet_non_emoji_path = 'result/tweets/english_word_vocabulary_user_tweet_emoji.txt'
    # wc_word_voc_user_tweet_non_emoji_path = 'word_cloud_files/wc_english_word_vocabulary_user_tweet_emoji.png'
    # with open(word_voc_user_tweet_non_emoji_path) as f:
    #     next(f)
    #     term_frequency_dict = dict([ast.literal_eval(line) for line in f])
    #
    # print(term_frequency_dict)
    # plotanalysis.draw_wordcloud(term_frequency_dict, wc_word_voc_user_tweet_non_emoji_path)

    '''emoji distribution plot'''
    '''need to add emoji to the plot manually'''
    # emoji_user_des_non_emoji_path = 'result/tweets/emoji_vocabulary_user_tweet_emoji.txt'
    # emoji_distribution_path = 'result/tweets/emoji_distribution_user_tweets_emoji.png'
    # with open(emoji_user_des_non_emoji_path) as f:
    #     next(f)
    #     term_frequency_dict = OrderedDict([ast.literal_eval(line) for line in f])
    #
    # plotanalysis.emoji_dict_distribution_bar(term_frequency_dict, title_value='Top 10 emoji distribution in 3747264 '
    #                                                                           'tweets \n(posted by 20,000 users with '
    #                                                                           'emoji in the description)',
    #                                          xlabel_value='Emojis', ylabel_value='Counts', dis_number_value=10,
    #                                          path=emoji_distribution_path)

    # cleaned_tweets = tweet_data.text
    # english_tweets = tweet_data.loc[tweet_data.lang == 'English']
    # english_tweets.reset_index(drop=True, inplace=True)
    # print(english_tweets)

    # path = "cleaned_data/DescriptionTest100.csv"
    # data_sentiment_store(des_data, cleaned_dec, path)

    # Deal with emojis
    # tweet = emoji.demojize(tweet)
    # tweet = tweet.replace(":", " ")
    # tweet = ' '.join(tweet.split())
