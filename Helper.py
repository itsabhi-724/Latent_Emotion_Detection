from urlextract import URLExtract

extract = URLExtract()

def fetch_stats(Selected_user,df):

    if Selected_user !='overall':
        df = df[df['user'] == Selected_user]
    #fetch number of messages
    num_messages = df.shape[0]

    #fetch number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    num_media_images = df[df['message'].str.contains('image omitted', case=False, na=False)].shape[0]
    num_media_videos = df[df['message'].str.contains('video omitted', case=False, na=False)].shape[0]

    # Total media count
    total_media = num_media_images + num_media_videos

    # number of links
    Links = []
    for message in df['message']:
        Links.extend(extract.find_urls(message))


    return num_messages, len(words),total_media,len(Links)

def most_busy_users(df):
    x = df['user'].value_counts().head()
    return x


