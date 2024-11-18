import streamlit as st
import Preprocessor,Helper
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
st.sidebar.title("Latent Emotion Detector ")

uploaded_file = st.sidebar.file_uploader("choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = Preprocessor.preprocess(data)

    st.dataframe(df)

    #fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"overall")

    Selected_user = st.sidebar.selectbox("show analysis wrt",user_list)

    if st.sidebar.button("show Analysis"):
        num_messages,words,total_media,num_links = Helper.fetch_stats(Selected_user,df)
        st.title("Top Statistics")
        col1,col2,col3,col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(total_media)
        with col4:
            st.header("Links Shared")
            st.title(num_links)
        # Monthly timeline
        st.title("Monthly Timeline")
        timeline = Helper.monthly_timeline(Selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='purple')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily timeline
        st.title("Daily Timeline")
        daily_timeline = Helper.daily_timeline(Selected_user, df)

        # Check if daily_timeline is not empty
        if not daily_timeline.empty:

            daily_timeline['datetime'] = pd.to_datetime(daily_timeline['datetime'], format='%Y-%m-%d')

            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(daily_timeline['datetime'], daily_timeline['message'], color='blue', marker='o')

            # Format x-axis to show dates as dd-mm-yyyy
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))

            # Rotate x-axis labels and set axis labels
            plt.xticks(rotation=45)
            ax.set_xlabel('Date')
            ax.set_ylabel('Messages')
            ax.set_title(f"Daily Timeline for {Selected_user}")

            # Improve layout for readability
            fig.tight_layout()

            # Show plot
            st.pyplot(fig)
        else:
            st.write("No data to show for the selected user in Daily Timeline.")

        #finding the busiest users  in the group
        if Selected_user == 'overall':
            st.title('Most Busy User')
            x = Helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1,col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)


        #Word Cloud
        st.title('Wordcloud')
        df_wc = Helper.create_wordcloud(Selected_user,df)
        fig,ax =plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)


        # Emoji analysis

        #helper.emoji_helper returns a list of emojis and their counts
        emoji_df = Helper.emoji_helper(Selected_user, df)

        st.title("Emoji Analysis")

        # Define specific colors for the top 5 emojis
        color_mapping = {
            0: 'red',  # Color for the 1st top emoji
            1: 'blue',  # Color for the 2nd top emoji
            2: 'green',  # Color for the 3rd top emoji
            3: 'orange',  # Color for the 4th top emoji
            4: 'violet',  # Color for the 5th top emoji
        }
        # Create two columns for the display
        col1, col2 = st.columns(2)

        with col1:
             # Create a DataFrame for the top 5 emojis and their colors
             if not emoji_df.empty:
                 # Get top 5 emojis by count
                top_emojis = emoji_df.nlargest(5, 'Count')

                # Assign colors from the color mapping
                top_emojis['Color'] = [color_mapping[i] for i in range(len(top_emojis))]

                 # Display the emoji dataframe in the first column
                st.dataframe(top_emojis[['Emoji', 'Count', 'Color']])

        with col2:
            # Create a pie chart in the second column
            if not emoji_df.empty:
                fig, ax = plt.subplots()

                # Extract colors for the top 5 emojis
                colors = top_emojis['Color'].tolist()

                # Plotting the top 5 emojis by count
                ax.pie(top_emojis['Count'], autopct='%1.1f%%', colors=colors)
                st.pyplot(fig)
            else:
                st.write("No emojis found for the Selected User.")
