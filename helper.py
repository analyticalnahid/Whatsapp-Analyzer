from urlextract import URLExtract
from collections import Counter
import emoji
import pandas as pd
from wordcloud import WordCloud 
extract = URLExtract()


## 1st Part
def fetch_stats(selected_user, df):
    
    ## fetch users
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    num_msg = df.shape[0]
    
    ## fetch words
    words = []
    for message in df['message']:
        words.extend(message.split())
    
    ## fetch media
    num_media_msg = df[df['message'] == '<Media omitted>\n'].shape[0]
    
    ## fetch links
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))
           
    return num_msg, len(words), num_media_msg, len(links)


## 2nd Part
def busy_user(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0]) * 100,2).reset_index().rename(columns={'index':'name','user':'percent'})
    return x,df

## 3rd Part
def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white') 
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc


def most_cmn_words(selected_user, df):
    
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
     
    temp = df[df['user'] != 'group notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    words = []
     
    for message in temp['message']:
        for word in message.lower().split():
            if word not in emoji.UNICODE_EMOJI_ENGLISH:
                words.append(word)
                
    words_df = pd.DataFrame(Counter(words).most_common(10))    
    return words_df     
         

## 4th Part
def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        
    emojis = []
    
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI_ENGLISH]) 
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))   
    
    return emoji_df  


def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        
    timeline = df.groupby(['year', 'month_nam', 'month']).count()['message'].reset_index()
    
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    
    return timeline    

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        
    daily_time = df.groupby('only_date').count()['message'].reset_index()
    return daily_time

def weekly_activity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    return df['day_name'].value_counts()    

def monthly_activity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    return df['month'].value_counts() 

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap