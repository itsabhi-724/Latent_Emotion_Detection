import streamlit as st
import Preprocessor,Helper
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
st.sidebar.title("Latent Emotion Detector ")

uploaded_file = st.sidebar.file_uploader("choose a file")
if uploaded_file is not None:
@@ -36,6 +38,42 @@
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
