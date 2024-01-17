# YouTubeAnalytics

YouTubeAnalyticsは、YouTubeチャンネルのビデオ統計を取得するためのPythonパッケージです。このパッケージは、YouTube Data API V3を使用して、特定のチャンネルのビデオのタイトルと視聴回数を取得します。

## インストール

このパッケージはPyPIからインストールできます：

pip install YouTubeAnalytics

## 使用方法

まず、YouTubeAnalyticsクラスをインポートし、APIキーを使用してインスタンスを作成します：

```python
from YTAnalytics import YouTubeAnalytics
yt_analytics = YouTubeAnalytics(api_key="your_api_key")
```


次に、get_channel_videosメソッドを使用して、特定のチャンネルのビデオ統計を取得します：

このメソッドは、指定したチャンネルの全てのビデオのタイトルと視聴回数を含むリストを返します。また、days_limitパラメータを指定することで、過去特定の日数のビデオのみを取得することも可能です：
```python
video_stats = yt_analytics.get_channel_videos(channel_id="your_channel_id")

video_stats = yt_analytics.get_channel_videos(channel_id="your_channel_id", days_limit=30)
```

この場合、過去30日間にアップロードされたビデオのみが取得されます。

## 注意事項

このパッケージはYouTube Data API V3を使用しています。そのため、使用するにはYouTube Data API V3のAPIキーが必要です。APIキーは、Google Cloud Consoleから取得できます。

また、このパッケージを使用する際は、YouTubeの利用規約と著作権法を遵守してください。具体的な使用方法や制限については、YouTube Data APIの公式ドキュメンテーションを参照してください。

## ライセンス

このパッケージはMITライセンスの下で公開されています。詳細はLICENSEファイルをご覧ください。


