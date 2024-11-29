import os
from dotenv import load_dotenv
import tweepy
from openai import OpenAI
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_connections():
    load_dotenv()
    
    logger.info("Testing Twitter API connection...")
    try:
        # Test Twitter credentials individually
        bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
        api_key = os.getenv('TWITTER_API_KEY')
        api_secret = os.getenv('TWITTER_API_SECRET')
        access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

        logger.info("Checking if credentials are loaded:")
        logger.info(f"Bearer Token present: {bool(bearer_token)}")
        logger.info(f"API Key present: {bool(api_key)}")
        logger.info(f"API Secret present: {bool(api_secret)}")
        logger.info(f"Access Token present: {bool(access_token)}")
        logger.info(f"Access Token Secret present: {bool(access_token_secret)}")

        # Initialize Twitter client
        client = tweepy.Client(
            bearer_token=bearer_token,
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
            wait_on_rate_limit=True
        )
        
        # Test Twitter connection by getting user info
        logger.info("Attempting to get user info...")
        user = client.get_me()
        logger.info(f"Successfully connected to Twitter API! Username: @{user.data.username}")
        
    except tweepy.errors.Unauthorized as e:
        logger.error(f"Twitter Authentication Error: {str(e)}")
        logger.error("Please check if your Twitter API credentials are correct and have the right permissions")
        return False
    except Exception as e:
        logger.error(f"Error connecting to Twitter API: {str(e)}")
        return False

    logger.info("\nTesting OpenAI API connection...")
    try:
        # Initialize OpenAI client
        openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Test OpenAI connection with a simple completion
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Write a short test tweet about technology"}],
            max_tokens=50
        )
        
        test_tweet = response.choices[0].message.content
        logger.info(f"Successfully connected to OpenAI API!")
        logger.info(f"Sample generated tweet: {test_tweet}")
        
    except Exception as e:
        logger.error(f"Error connecting to OpenAI API: {str(e)}")
        return False

    return True

if __name__ == "__main__":
    print("Testing bot connections...\n")
    success = test_connections()
    if success:
        print("\nAll connections successful! You can now run the main bot.")
    else:
        print("\nSome connections failed. Please check the errors above.")
