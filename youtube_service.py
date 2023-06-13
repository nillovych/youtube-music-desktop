from google_service import service


class YouTubeService:
    def get_search_results(self, query):
        response = service.search().list(
            q=query,
            part='snippet',
            type='video',
            maxResults=10
        ).execute()

        results = []
        for item in response['items']:
            results.append({
                'title': item['snippet']['title'],
                'channel': item['snippet']['channelTitle'],
                'thumbnail': item['snippet']['thumbnails']['default']['url'],
                'video_id': item['id']['videoId']
            })
        return results
