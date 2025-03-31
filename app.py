from flask import Flask, render_template, request, jsonify
import tweepy
from textblob import TextBlob
import sqlite3
import json
from config import Config
import time
from datetime import datetime, timedelta
import requests
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
app.config.from_object(Config)

# Rate limiting
last_request_time = {}
MIN_TIME_BETWEEN_REQUESTS = 5  # seconds

def init_db():
    conn = sqlite3.connect(app.config['SQLITE_DB_PATH'])
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS searches
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         platform TEXT NOT NULL,
         query TEXT NOT NULL,
         results TEXT NOT NULL,
         timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS api_requests
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         platform TEXT NOT NULL,
         timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)
    ''')
    conn.commit()
    conn.close()

def can_make_request(platform):
    conn = sqlite3.connect(app.config['SQLITE_DB_PATH'])
    c = conn.cursor()
    
    c.execute('DELETE FROM api_requests WHERE timestamp < datetime("now", "-15 minutes")')
    
    c.execute('SELECT COUNT(*) FROM api_requests WHERE platform = ? AND timestamp > datetime("now", "-15 minutes")', (platform,))
    count = c.fetchone()[0]
    
    current_time = time.time()
    platform_last_time = last_request_time.get(platform)
    
    if platform_last_time and (current_time - platform_last_time) < MIN_TIME_BETWEEN_REQUESTS:
        return False
    
    limit = 150 if platform == 'twitter' else 50 if platform == 'reddit' else 100
    if count >= limit:
        return False
        
    c.execute('INSERT INTO api_requests (platform) VALUES (?)', (platform,))
    conn.commit()
    conn.close()
    
    last_request_time[platform] = current_time
    return True

def get_twitter_client():
    return tweepy.Client(bearer_token=app.config['TWITTER_BEARER_TOKEN'])

def get_reddit_posts(query):
    headers = {'User-Agent': app.config['REDDIT_USER_AGENT']}
    auth = requests.auth.HTTPBasicAuth(app.config['REDDIT_CLIENT_ID'], app.config['REDDIT_CLIENT_SECRET'])
    data = {'grant_type': 'client_credentials'}
    
    res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)
    token = res.json().get('access_token')
    
    headers['Authorization'] = f'bearer {token}'
    res = requests.get(f'https://oauth.reddit.com/r/all/search?q={query}&limit=10', headers=headers)
    return res.json()['data']['children']

def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    return 'positive' if polarity > 0 else 'negative' if polarity < 0 else 'neutral', polarity

def generate_word_cloud(texts):
    text = ' '.join(texts)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.savefig('static/images/wordcloud.png', bbox_inches='tight')
    plt.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    platform = request.form.get('platform', 'twitter')
    query = request.form.get('query')
    
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    if not can_make_request(platform):
        return jsonify({'error': 'Rate limit exceeded for ' + platform}), 429

    try:
        results = []
        if platform == 'twitter':
            client = get_twitter_client()
            tweets = client.search_recent_tweets(query=query, max_results=10, tweet_fields=['created_at'])
            if tweets.data:
                results = [{
                    'text': tweet.text,
                    'sentiment': analyze_sentiment(tweet.text)[0],
                    'polarity': analyze_sentiment(tweet.text)[1],
                    'created_at': tweet.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'platform': 'twitter'
                } for tweet in tweets.data]
        
        elif platform == 'reddit':
            posts = get_reddit_posts(query)
            results = [{
                'text': post['data']['title'] + ' ' + post['data'].get('selftext', ''),
                'sentiment': analyze_sentiment(post['data']['title'] + ' ' + post['data'].get('selftext', ''))[0],
                'polarity': analyze_sentiment(post['data']['title'] + ' ' + post['data'].get('selftext', ''))[1],
                'created_at': datetime.fromtimestamp(post['data']['created_utc']).strftime('%Y-%m-%d %H:%M:%S'),
                'platform': 'reddit'
            } for post in posts]

        if not results:
            return jsonify({'success': True, 'results': [], 'stats': {'positive': 0, 'negative': 0, 'neutral': 0, 'total': 0}})

        # Save to database
        conn = sqlite3.connect(app.config['SQLITE_DB_PATH'])
        c = conn.cursor()
        c.execute('INSERT INTO searches (platform, query, results) VALUES (?, ?, ?)',
                 (platform, query, json.dumps(results)))
        conn.commit()
        conn.close()

        # Generate statistics and word cloud
        sentiments = [r['sentiment'] for r in results]
        stats = {
            'positive': sentiments.count('positive'),
            'negative': sentiments.count('negative'),
            'neutral': sentiments.count('neutral'),
            'total': len(results)
        }
        generate_word_cloud([r['text'] for r in results])

        return jsonify({
            'success': True,
            'results': results,
            'stats': stats,
            'wordcloud': '/static/images/wordcloud.png'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True)