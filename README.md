# Social Media Sentiment Analysis

This project is a web application that allows users to analyze the sentiment of posts from Twitter and Reddit. It provides real-time sentiment analysis, word cloud generation, and interactive visualizations. Users can select a platform, enter a query, and view the sentiment breakdown, frequent keywords, and related posts.

Hosted here: https://social-semantic-analysis.onrender.com

## Features
- **Multiplatform Sentiment Analysis**:
  - Supports Twitter, Reddit.
  - Analyzes sentiment (positive, negative, neutral) using TextBlob.
- **Real-time Analysis**:
  - Fetches recent posts from selected platforms.
  - Displays sentiment statistics and individual post analysis.
- **Word Cloud**:
  - Generates a word cloud of the most frequent words in the analyzed posts.
- **Interactive UI**:
  - Clean and responsive interface with loading states.
  - Displays sentiment statistics, word clouds, keyword charts, and related posts.

## Technologies Used
- **Backend**:
  - Flask (Python web framework)
  - Tweepy (Twitter API client)
  - Requests (for Reddit API)
  - TextBlob (sentiment analysis)
  - SQLite (database for storing search results)
- **Frontend**:
  - HTML/CSS/JavaScript
- **Visualization**:
  - WordCloud (for generating word clouds)
  - Matplotlib (for rendering word clouds)
- **Environment**:
  - Python 3.8+
  - Virtualenv (recommended for dependency management)

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for cloning the repository)
- API keys for:
  - Twitter (Bearer Token)
  - Reddit (Client ID, Client Secret)
  - News API (API Key)

## Setup Instructions

### Install Dependencies
Install the required Python packages listed in requirements.txt

### Set Up API Keys
Create a `.env` file in the project root and add your API keys:
```
SECRET_KEY=your-secret-key
TWITTER_BEARER_TOKEN=your-twitter-bearer-token
REDDIT_CLIENT_ID=your-reddit-client-id
REDDIT_CLIENT_SECRET=your-reddit-client-secret
REDDIT_USER_AGENT=your-app-name/v1.0
NEWS_API_KEY=your-news-api-key
SQLITE_DB_PATH=instance/sentiment.db
```

#### How to Get API Keys:
- **Twitter**:
  1. Go to https://developer.twitter.com/.
  2. Create a project and app in the Developer Portal.
  3. Get the Bearer Token (free tier allows 500,000 tweets/month read access).
- **Reddit**:
  1. Go to https://www.reddit.com/prefs/apps.
  2. Create a new script app.
  3. Note the Client ID and Client Secret (free tier allows 600 requests/10 minutes).



## Usage
1. **Select a Platform**:
   - Choose from Twitter, Reddit, or News API using the dropdown menu.
2. **Enter a Query**:
   - Type a topic or keyword (e.g., "technology", "politics") in the search bar.
3. **Analyze**:
   - Click the "Analyze" button to fetch and analyze posts.
4. **View Results**:
   - **Statistics**: See the sentiment breakdown (positive, negative, neutral).
   - **Word Cloud**: Visualize frequent words.
   - **Posts**: See individual posts with their sentiment and timestamps.

## Project Structure
```
social-media-sentiment-analysis/
├── instance/
│   └── sentiment.db          # SQLite database
├── static/
│   ├── css/
│   │   └── style.css         # Stylesheet
│   ├── js/
│   │   └── main.js           # Frontend JavaScript
│   └── images/
│       └── wordcloud.png     # Generated word cloud image
├── templates/
│   ├── base.html             # Base HTML template
│   └── index.html            # Main page template
├── app.py                    # Main Flask application
├── config.py                 # Configuration file
├── .env                      # Environment variables (API keys)
└── README.md                 # Project documentation
```

## API Keys Setup
- Ensure all API keys are added to the `.env` file as shown above.
- The app uses `python-dotenv` to load these variables. If the `.env` file is missing or incorrectly formatted, the app will fail to authenticate with the APIs.

## Limitations
- **Free Tier Constraints**:
  - Twitter: 500,000 tweets/month read access.
  - Reddit: 600 requests/10 minutes.
- **Real-time Analysis**:
  - Uses a pull-based approach due to free tier limitations. True streaming requires paid API tiers.
- **Performance**:
  - Word cloud is overwritten each time; use unique filenames for production.

## Future Improvements
- Add support for more platforms (e.g., Instagram, YouTube).
- Implement true real-time streaming with paid API tiers.
- Display extracted entities (from spaCy NER) in the UI.
- Extend the related posts feature to Reddit and News API.
- Add user authentication and search history.
- Improve performance with caching (e.g., Redis).
