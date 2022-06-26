from module import yt


api_key = '######################' #input api_key
channel_id = '################' #input channel_id

#DO NOT CHANGE THE BELOW
url = f'''
https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_id}&order=date&maxResults=50&key={api_key}
'''
url_video_stats = f'''https://www.googleapis.com/youtube/v3/videos'''





if __name__ == "__main__":
#class yt requires four arguments (channel_id, api_key, url, and url_video_stats)
    mays_taste = yt(channel_id,api_key,url,url_video_stats)
    mays_taste.video_df().to_csv('mays_taste_yt.csv', sep="$")
