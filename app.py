import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

## Title
st.sidebar.title("Whatsapp Chat Analyzer")

## File Uploader
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocessor(data)
    
    
## Fetch Users
    user_lst = df['user'].unique().tolist()
    user_lst.remove('group notification')
    user_lst.sort()
    user_lst.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Choose user", user_lst)    
    
    if st.sidebar.button("Show Analysis"):
  
## 1st Part
          
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links) 

        ## monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        ## daily timeline
        st.title("Daily Timeline")
        daily_time = helper.daily_timeline(selected_user, df)
        fig,ax = plt.subplots()
        ax.plot(daily_time['only_date'], daily_time['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        
        ## 2nd Part
        
        if selected_user == 'Overall':
            st.title("Most Busy Users")
            busy_usr,new_df = helper.busy_user(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2) 
            
            with col1:
                ax.bar(busy_usr.index, busy_usr.values, color='red')   
                plt.xticks(rotation='vertical')
                st.pyplot(fig)  
            
            with col2:
                st.dataframe(new_df) 
        
        
        ## activity map
        st.title("Activity Map")
        col1, col2 = st.columns(2)
        
        with col1:
            st.header("Most Busy Day")
            busy_day = helper.weekly_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            
        with col2:
            st.header("Most Busy Month")
            busy_month = helper.monthly_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        
        st.title("Weekly Activity")
        user_heatmap = helper.activity_heatmap(selected_user, df) 
        fig, ax = plt.subplots()   
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)
                              
                
## 3rd Part
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        
        most_common_df = helper.most_cmn_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1], color='orange')
        plt.xticks(rotation='vertical')
        st.title("Most Common Words")
        st.pyplot(fig)
        
## 4th Part
        emoji_df = helper.emoji_helper(selected_user, df) 
        st.title("Emoji Analysis") 
        
        col1, col2 = st.columns(2) 
        
        with col1:
            st.dataframe(emoji_df) 
        
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)
            
            
                    