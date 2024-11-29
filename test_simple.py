import tweepy
import os
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Load environment variables
    load_dotenv()
    
    # Get credentials
    api_key = os.getenv('TWITTER_API_KEY')
    api_secret = os.getenv('TWITTER_API_SECRET')
    access_token = os.getenv('TWITTER_ACCESS_TOKEN')
    access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    
    logger.info("Loaded credentials:")
    logger.info(f"API Key: {api_key[:4]}...{api_key[-4:]}")
    logger.info(f"API Secret: {api_secret[:4]}...{api_secret[-4:]}")
    logger.info(f"Access Token: {access_token[:4]}...{access_token[-4:]}")
    logger.info(f"Access Token Secret: {access_token_secret[:4]}...{access_token_secret[-4:]}")
    
    try:
        # Create OAuth 1.0a handler
        auth = tweepy.OAuthHandler(api_key, api_secret)
        auth.set_access_token(access_token, access_token_secret)
        
        # Create API object with wait_on_rate_limit enabled
        api = tweepy.API(auth, wait_on_rate_limit=True)
        
        # Verify credentials
        logger.info("\nAttempting to verify credentials...")
        me = api.verify_credentials()
        logger.info(f"Successfully authenticated as: @{me.screen_name}")
        return True
    except tweepy.errors.Unauthorized as e:
        logger.error(f"\nTwitter Authentication Error: {str(e)}")
        logger.error("Please check your Twitter Developer Portal settings:")
        logger.error("1. OAuth 1.0a is enabled")
        logger.error("2. App permissions include Read and Write")
        logger.error("3. App type is set to 'Automated App or Bot'")
        logger.error("4. Callback URL is set to https://example.com/callback")
        return False
    except Exception as e:
        logger.error(f"\nUnexpected error: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        print("\nAuthentication failed. Please check the logs above for details.")
