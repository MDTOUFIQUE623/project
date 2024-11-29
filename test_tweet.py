from twitter_bot import TwitterBot

def test_single_tweet():
    bot = TwitterBot()
    success = bot.post_tweet()
    if success:
        print("\nTweet posted successfully! Check your Twitter profile.")
    else:
        print("\nFailed to post tweet. Check the logs for details.")

if __name__ == "__main__":
    test_single_tweet()
