# AI Twitter Growth Bot

An AI-powered Twitter bot that helps grow your account through personalized content generation and strategic engagement.

## Features

- Automated personalized content generation using OpenAI
- Scheduled daily posts (3 times a day)
- Strategic community engagement (2 times a day)
- Topic-focused content generation
- Smart engagement with relevant tweets

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your API credentials:
   - Get Twitter API credentials from the Twitter Developer Portal
   - Get an OpenAI API key from OpenAI
   - Add these credentials to the `.env` file

3. Customize your topics:
   - Edit the `topics_of_interest` list in `twitter_bot.py`

## Usage

Run the bot:
```bash
python twitter_bot.py
```

The bot will:
- Post tweets at 9:00, 15:00, and 20:00 daily
- Engage with community content at 12:00 and 18:00 daily
- Generate content based on your specified topics
- Automatically like and retweet relevant content

## Customization

You can modify:
- Posting schedule in the `main()` function
- Engagement frequency and behavior in `engage_with_community()`
- Content generation prompts in `generate_content()`
- Topics of interest in the `TwitterBot` class

## Note

Make sure to comply with Twitter's terms of service and API rate limits.
