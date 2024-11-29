import os
from dotenv import load_dotenv
import tweepy
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_twitter_auth():
    load_dotenv()
    
    logger.info("Testing Twitter API connection...")
    try:
        # Get credentials
        api_key = os.getenv('TWITTER_API_KEY')
        api_secret = os.getenv('TWITTER_API_SECRET')
        access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

        # Create OAuth 1.0a User handler
        auth = tweepy.OAuthHandler(api_key, api_secret)
        auth.set_access_token(access_token, access_token_secret)

        # Create API object
        api = tweepy.API(auth)
        
        # Verify credentials
        logger.info("Verifying credentials...")
        user = api.verify_credentials()
        logger.info(f"Successfully authenticated as: @{user.screen_name}")
        return True
        
    except tweepy.errors.Unauthorized as e:
        logger.error(f"Twitter Authentication Error: {str(e)}")
        logger.error("Please check if your Twitter API credentials are correct and have the right permissions")
        return False
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing Twitter authentication...\n")
    success = test_twitter_auth()
    if success:
        print("\nAuthentication successful!")
    else:
        print("\nAuthentication failed. Please check the errors above.")
