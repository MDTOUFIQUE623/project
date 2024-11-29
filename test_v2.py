import os
from dotenv import load_dotenv
import tweepy
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_twitter_auth_v2():
    load_dotenv()
    
    logger.info("Testing Twitter API v2 connection...")
    try:
        # Get credentials
        api_key = os.getenv('TWITTER_API_KEY')
        api_secret = os.getenv('TWITTER_API_SECRET')
        access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        bearer_token = os.getenv('TWITTER_BEARER_TOKEN')

        # Print credentials (partially masked)
        logger.info(f"API Key: {api_key[:4]}...{api_key[-4:]}")
        logger.info(f"Access Token: {access_token[:4]}...{access_token[-4:]}")
        
        # Create client
        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
            bearer_token=bearer_token
        )
        
        # Test connection by getting own user info
        logger.info("Attempting to get user info...")
        response = client.get_me()
        
        if response.data:
            logger.info(f"Successfully authenticated as: @{response.data.username}")
            return True
        else:
            logger.error("Could not get user info")
            return False
            
    except tweepy.errors.Unauthorized as e:
        logger.error(f"Twitter Authentication Error: {str(e)}")
        logger.error("Please check if your Twitter API credentials are correct and have the right permissions")
        return False
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing Twitter API v2 authentication...\n")
    success = test_twitter_auth_v2()
    if success:
        print("\nAuthentication successful!")
    else:
        print("\nAuthentication failed. Please check the errors above.")
