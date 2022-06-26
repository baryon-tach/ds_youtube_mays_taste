import requests
import pandas as pd
import re #--for searching
import math #-- for rounding
from functools import reduce #-- for converting two-dimensional list into a one dimensional list

class yt:

    def __init__(self, channel_id, api_key, url, url_video_stats):

        self.channel_id = channel_id
        self.api_key = api_key
        self.url = url
        self.url_video_stats = url_video_stats


    def get_all_results(self, url): #to get a list of all of the videos
        allvids = []
        page_tokens = ["",]
        numberofresults = int(requests.get(url).json()['pageInfo']['totalResults'])
        pages = math.ceil(numberofresults/50)
        for page in range(pages-1):
            token = page_tokens[page]
            t_url = (url + '&pageToken={}').format(token)
            tresponse = requests.get(t_url).json()
            allvids.append(tresponse['items'])
            if "nextPageToken" in tresponse:
                page_tokens.append(tresponse['nextPageToken'])
            else:
                page_tokens.append("")
        #convert into one dimensional list
        ed_allvids = reduce(lambda x,y:x+y, allvids)
        return ed_allvids


    def video_stats(self,video_id): #getting each individual video's details
        vs_url = (self.url_video_stats + '?id={}&part=statistics&key={}').format(video_id,self.api_key)
        vs_response = requests.get(vs_url).json()

        counts = vs_response['items'][0]['statistics']

        view_count = counts['viewCount']
        like_count = counts['likeCount']
        comment_count = counts['commentCount']

        return view_count, like_count, comment_count


    def video_df(self):
        df = pd.DataFrame(columns=['video_id','video_title','upload_date','view_count','like_count','comment_count'])

        for video in self.get_all_results(self.url):
            if video['id']['kind']=='youtube#video':
                video_id = video['id']['videoId']
                video_title = video['snippet']['title']
                upload_date = str(video['snippet']['publishTime'])
                upload_date = re.split('T', upload_date, flags=re.IGNORECASE)[0]
                view_count, like_count, comment_count = self.video_stats(video_id)

                df = df.append({'video_id':video_id, 'video_title':video_title,
                                'upload_date':upload_date, 'view_count':view_count,
                                'like_count':like_count,'comment_count':comment_count},
                                 ignore_index=True)
        return df
