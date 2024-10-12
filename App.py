import streamlit as st
import Preprocessor,Helper
import matplotlib.pyplot as plt
st.sidebar.title("Latent Emotion Detecter ")

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
