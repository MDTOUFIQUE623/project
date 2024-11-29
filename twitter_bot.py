import os
import random
import time
import json
import schedule
import tweepy
import openai
from datetime import datetime, timedelta
from dotenv import load_dotenv
import logging
from typing import List, Dict
import re

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('twitter_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TwitterBot:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Initialize API clients
        self.setup_api_clients()
        
        # Load configuration
        self.load_config()
        
        # Initialize state tracking
        self.engagement_history = {}
        self.post_history = []
        self.load_state()

        # Define content strategies with engagement focus
        self.content_types = [
            "growth_hack", "expert_tip", "thought_leadership",
            "industry_insight", "success_story", "career_advice",
            "tech_prediction", "tool_review", "learning_path",
            "code_wisdom", "productivity_hack", "tech_opinion",
            "quick_tutorial", "resource_share", "challenge",
            "poll", "discussion", "hot_take"
        ]
        
        # Personal brand topics
        self.topics_of_interest = [
            "software development", "tech entrepreneurship",
            "AI/ML engineering", "full-stack development",
            "system architecture", "cloud solutions",
            "coding best practices", "tech career growth",
            "developer mindset", "tech innovation",
            "startup tech", "modern web dev",
            "backend engineering", "API development",
            "database optimization", "scalable systems",
            "tech leadership", "code quality",
            "developer tools", "automation",
            "tech interviews", "software testing",
            "continuous learning", "tech community",
            "open source", "side projects",
            "tech mentorship", "coding challenges",
            "tech stack choices", "system design"
        ]

        # Engagement-focused hashtags
        self.primary_hashtags = [
            "#TechTwitter", "#CodeNewbie", "#100DaysOfCode",
            "#Developer", "#SoftwareEngineer", "#WebDev",
            "#Programming", "#CodingLife", "#TechTalent",
            "#DevCommunity", "#CodeLife", "#TechCareer"
        ]
        
        self.tech_hashtags = [
            "#Python", "#JavaScript", "#React", "#NodeJS",
            "#AWS", "#Cloud", "#Docker", "#Kubernetes",
            "#AI", "#MachineLearning", "#DataScience",
            "#FullStack", "#BackEnd", "#DevOps"
        ]
        
        self.growth_hashtags = [
            "#CareerGrowth", "#TechGrowth", "#LearnToCode",
            "#DevLife", "#CodingTips", "#TechAdvice",
            "#BuildInPublic", "#DevJourney", "#CodeMentor"
        ]

        # Engagement hooks
        self.engagement_hooks = [
            "🤔 What's your take on this?",
            "💭 Share your experience!",
            "👇 Drop your favorite tool below",
            "🔄 RT if you agree",
            "❤️ Like if you've experienced this",
            "💡 What would you add?",
            "🎯 Tag someone who needs to see this",
            "📊 Which approach do you prefer?",
            "🚀 Share your success stories!",
            "💪 How do you handle this challenge?"
        ]

        # Time-based content strategies
        self.time_based_content = {
            "morning": [
                "☀️ Morning motivation for devs",
                "🎯 Set your coding goals",
                "💡 Start your day with this tech tip"
            ],
            "afternoon": [
                "⚡ Quick productivity hack",
                "🔍 Deep dive into tech",
                "💻 Coding challenge time"
            ],
            "evening": [
                "📚 Evening learning session",
                "🤔 Reflect on your code",
                "🌟 Share your daily win"
            ]
        }

    def setup_api_clients(self):
        """Initialize Twitter and OpenAI API clients"""
        try:
            self.client = tweepy.Client(
                bearer_token=os.getenv('TWITTER_BEARER_TOKEN'),
                consumer_key=os.getenv('TWITTER_API_KEY'),
                consumer_secret=os.getenv('TWITTER_API_SECRET'),
                access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
                access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
                wait_on_rate_limit=True
            )
            openai.api_key = os.getenv('OPENAI_API_KEY')
            logger.info("API clients initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing API clients: {str(e)}")
            raise

    def load_config(self):
        """Load configuration from environment variables"""
        self.daily_post_count = int(os.getenv('DAILY_POST_COUNT', 3))
        self.engagement_count = int(os.getenv('ENGAGEMENT_COUNT', 2))
        self.engagement_ratio = float(os.getenv('ENGAGEMENT_RATIO', 0.6))
        self.max_hashtags = int(os.getenv('MAX_HASHTAGS', 3))
        self.content_temperature = float(os.getenv('CONTENT_TEMPERATURE', 0.7))
        self.min_engagement_followers = int(os.getenv('MIN_ENGAGEMENT_FOLLOWERS', 100))
        self.max_retries = int(os.getenv('MAX_RETRIES', 3))
        self.tweet_length = int(os.getenv('TWEET_LENGTH', 240))

    def load_state(self):
        """Load bot state from file"""
        try:
            if os.path.exists('bot_state.json'):
                with open('bot_state.json', 'r') as f:
                    state = json.load(f)
                    self.engagement_history = state.get('engagement_history', {})
                    self.post_history = state.get('post_history', [])
                logger.info("Bot state loaded successfully")
        except Exception as e:
            logger.error(f"Error loading bot state: {str(e)}")

    def save_state(self):
        """Save bot state to file"""
        try:
            state = {
                'engagement_history': self.engagement_history,
                'post_history': self.post_history
            }
            with open('bot_state.json', 'w') as f:
                json.dump(state, f)
            logger.info("Bot state saved successfully")
        except Exception as e:
            logger.error(f"Error saving bot state: {str(e)}")

    def generate_mock_content(self) -> str:
        """Generate engaging mock content for testing"""
        content_type = random.choice(self.content_types)
        topic = random.choice(self.topics_of_interest)
        
        # Select hashtags strategically
        primary_tag = random.choice(self.primary_hashtags)
        tech_tag = random.choice(self.tech_hashtags)
        growth_tag = random.choice(self.growth_hashtags)
        hashtags = f"{primary_tag} {tech_tag} {growth_tag}"
        
        # Add engagement hook
        engagement_hook = random.choice(self.engagement_hooks)
        
        # Get time-appropriate intro
        hour = datetime.now().hour
        if 5 <= hour < 12:
            time_intro = random.choice(self.time_based_content["morning"])
        elif 12 <= hour < 17:
            time_intro = random.choice(self.time_based_content["afternoon"])
        else:
            time_intro = random.choice(self.time_based_content["evening"])
        
        templates = [
            f"{time_intro}\n\n💡 {topic} pro tip:\n• Start small\n• Build consistently\n• Share progress\n\n{engagement_hook}\n\n{hashtags}",
            f"🔥 Want to excel in {topic}?\n\n3 game-changing practices:\n1️⃣ Code daily\n2️⃣ Read documentation\n3️⃣ Build projects\n\n{engagement_hook}\n\n{hashtags}",
            f"🚀 {topic} wisdom:\n\nWhat I wish I knew earlier:\n• Test early\n• Document well\n• Seek feedback\n\n{engagement_hook}\n\n{hashtags}",
            f"{time_intro}\n\nMy top 3 tools for {topic}:\n🛠️ [Tool 1]\n⚡ [Tool 2]\n🔧 [Tool 3]\n\n{engagement_hook}\n\n{hashtags}",
            f"💎 {topic} golden rule:\n\nDon't just write code.\nWrite code that tells a story.\n\n{engagement_hook}\n\n{hashtags}",
            f"📈 Boost your {topic} skills:\n\nKey focus areas:\n• Core concepts\n• Best practices\n• Real projects\n\n{engagement_hook}\n\n{hashtags}",
            f"⚡ Quick {topic} tip:\n\nAlways remember:\nCode for humans first,\ncomputers second.\n\n{engagement_hook}\n\n{hashtags}",
            f"🎯 {topic} challenge:\n\nBuild something useful today.\nShare your progress.\nSupport others.\n\n{engagement_hook}\n\n{hashtags}"
        ]
        
        return random.choice(templates)

    def generate_content(self) -> str:
        """Generate personalized content using OpenAI or fallback to mock content"""
        try:
            content_type = random.choice(self.content_types)
            topic = random.choice(self.topics_of_interest)
            
            try:
                prompt = f"""Generate a Twitter post ({content_type}) about {topic}.
                Make it engaging, informative, and conversational.
                Include relevant hashtags (max {self.max_hashtags}).
                Keep it under {self.tweet_length} characters.
                Focus on providing value to tech-savvy audience."""
                
                response = openai.Completion.create(
                    engine="gpt-3.5-turbo-instruct",
                    prompt=prompt,
                    max_tokens=100,
                    temperature=self.content_temperature,
                    n=1
                )
                
                content = response.choices[0].text.strip()
            except Exception as e:
                logger.warning(f"OpenAI generation failed, falling back to mock content: {str(e)}")
                content = self.generate_mock_content()
            
            logger.info(f"Generated content: {content}")
            return content
        except Exception as e:
            logger.error(f"Error generating content: {str(e)}")
            return None

    def format_tweet(self, content: str) -> str:
        """Format and clean up tweet content"""
        try:
            # Remove extra whitespace and newlines
            content = ' '.join(content.split())
            
            # Ensure proper hashtag formatting
            content = re.sub(r'(?<!&)#', ' #', content)
            
            # Truncate if too long
            if len(content) > self.tweet_length:
                content = content[:self.tweet_length-3] + "..."
            
            return content
        except Exception as e:
            logger.error(f"Error formatting tweet: {str(e)}")
            return content

    def post_tweet(self) -> bool:
        """Post a tweet with generated content"""
        for _ in range(self.max_retries):
            try:
                content = self.generate_content()
                if not content:
                    continue
                
                formatted_content = self.format_tweet(content)
                response = self.client.create_tweet(text=formatted_content)
                
                if response.data:
                    tweet_id = response.data['id']
                    self.post_history.append({
                        'id': tweet_id,
                        'content': formatted_content,
                        'timestamp': datetime.now().isoformat()
                    })
                    self.save_state()
                    logger.info(f"Successfully posted tweet: {formatted_content}")
                    return True
                
            except Exception as e:
                logger.error(f"Error posting tweet: {str(e)}")
                time.sleep(5)  # Wait before retry
        
        return False

    def engage_with_community(self):
        """Smart engagement with relevant tweets"""
        try:
            # Search for relevant tweets
            for topic in self.topics_of_interest:
                query = f"{topic} -is:retweet -is:reply lang:en"
                tweets = self.client.search_recent_tweets(
                    query=query,
                    max_results=10,
                    tweet_fields=['author_id', 'public_metrics']
                )
                
                if not tweets.data:
                    continue
                
                for tweet in tweets.data:
                    # Check if we've already engaged with this tweet
                    if tweet.id in self.engagement_history:
                        continue
                    
                    # Like and retweet if meets criteria
                    metrics = tweet.public_metrics
                    if metrics['like_count'] > self.min_engagement_followers:
                        self.client.like(tweet.id)
                        self.client.retweet(tweet.id)
                        
                        self.engagement_history[tweet.id] = {
                            'type': 'like_retweet',
                            'timestamp': datetime.now().isoformat()
                        }
                        logger.info(f"Engaged with tweet {tweet.id}")
                        
                        # Save state after each engagement
                        self.save_state()
                        
                        # Rate limiting
                        time.sleep(60 / self.engagement_count)
                        
        except Exception as e:
            logger.error(f"Error in community engagement: {str(e)}")

def main():
    try:
        bot = TwitterBot()
        logger.info("Twitter Bot initialized successfully")
        
        # Schedule tweets throughout the day
        post_times = [
            "09:00", "13:00", "17:00"  # Adjust these times as needed
        ]
        
        for time_str in post_times:
            schedule.every().day.at(time_str).do(bot.post_tweet)
        
        # Schedule engagement every 4 hours
        schedule.every(4).hours.do(bot.engage_with_community)
        
        logger.info("Starting bot schedule...")
        while True:
            schedule.run_pending()
            time.sleep(60)
            
    except Exception as e:
        logger.error(f"Error in main bot execution: {str(e)}")
        raise

if __name__ == "__main__":
    main()
