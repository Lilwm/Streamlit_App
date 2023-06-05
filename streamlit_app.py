import pip

pip.main(['install', 'praw'])

#import necessary libraries
import pandas as pd
import praw
import streamlit as st
import matplotlib.pyplot as plt
# Set up Reddit API credentials
reddit = praw.Reddit(client_id='3A5qZJ0WqF6PZrNOqXraZA',
                     client_secret='VCRBEIrJ3aHi0T_WbkAxQzHpPlXXag',
                     user_agent='TelecomApp')
#function to extract subreddits


def get_subreddits(no_of_posts):
  # Define keywords to track
  keywords = [
    'telecom fraud', 'phone scam', 'sim swap'
    'telecom scams', 'telco fraud'
  ]

  #extract subreddits
  subreddit = reddit.subreddit('all')
  #get posts from a subreddit
  posts = subreddit.search('telecom fraud', limit=no_of_posts)

  #extract important info from the subreddits
  post_list = []
  for post in posts:
    titles = any(post.title for keyword in keywords)
    body = any(post.selftext for keyword in keywords)
    posts_dict = {
      'title': post.title,
      'timestamp': post.created_utc,
      'username': post.author.name,
      'post text': post.selftext,
      'subreddit_name': post.subreddit.display_name
    }
    #add to the list
    if titles or body:
      post_list.append(posts_dict)

    # Create a DataFrame to store the posts
  df = pd.DataFrame(post_list)
  return df


#clean the data
def transform(df):
  df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
  return df


#get the data
df1 = get_subreddits(st.slider('Select posts to analyze:', 1, 200, 50))
transform(df1)

# display data
st.title('Telecom Fraud Trends')
st.subheader('fraud posts per month')
#resample df to get no of posts per day
df_resampled = df1.resample('M', on='timestamp').count()
st.line_chart(df_resampled['title']) 

# bar graph for posts per user
username = df1['username'].value_counts().reset_index()
username.columns = ['Username', 'count']

fig, ax = plt.subplots()
ax.bar(username['Username'], username['count'])
ax.set_xlabel('Usernames')
ax.set_ylabel('Number')
ax.set_title('Posts Per Username')

# Get the column labels from the axes object
labels = ax.get_xticklabels()

# Adjust the column labels as needed
for label in labels:
    label.set_rotation(45)
    label.set_horizontalalignment('right')

st.header('Number of posts  Per Username')
st.pyplot(fig)

# Display the posts in detail as a table
st.write(df1, height=250, width=550)
