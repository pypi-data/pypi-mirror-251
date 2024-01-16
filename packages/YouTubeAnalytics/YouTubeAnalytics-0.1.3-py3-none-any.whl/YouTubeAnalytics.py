from pyyoutube import Api
from datetime import datetime, timedelta
class YouTubeAnalytics:
    def __init__(self, api_key):
        self.api = Api(api_key=api_key)
    def get_channel_videos(self, channel_id, days_limit=None):
        channel_info = self.api.get_channel_info(channel_id=channel_id)
        if channel_info is None:
            print("Failed to get channel info")
            return None
        uploads_id = channel_info.items[0].to_dict()["contentDetails"]["relatedPlaylists"]["uploads"]
        playlist_items = self.api.get_playlist_items(playlist_id=uploads_id, count=None)
        video_stats = []
        for item in playlist_items.items:
            video_id = item.snippet.resourceId.videoId
            video_info = self.api.get_video_by_id(video_id=video_id).items[0]
            published_at = datetime.strptime(video_info.snippet.publishedAt, "%Y-%m-%dT%H:%M:%SZ")
            if days_limit is None or published_at > datetime.now() - timedelta(days=days_limit):
                video_stats.append({
                    "title": video_info.snippet.title,
                    "viewCount": video_info.statistics.viewCount
                })
        return video_stats