# youtube コメント抽出用
from googleapiclient.discovery import build
from collections import Counter
import re

def main():
	# APIキーと動画IDを設定
	api_key = input('YOUR_API_KEY ＝ ')
	video_id = input('YOUR_VIDEO_ID = ')

	# YouTube APIクライアントを作成
	youtube = build('youtube', 'v3', developerKey=api_key)

	# 動画のコメントを取得
	request = youtube.commentThreads().list(
    	part="snippet",
    	videoId=video_id,
    	maxResults=100,  # 最大100件のコメントを取得
    	textFormat="plainText"
	)
	response = request.execute()

	# コメントから単語を抽出し、出現頻度を計算
	counter = Counter()
	for item in response['items']:
    	comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
    	words = re.findall(r'\b\w+\b', comment)
    	counter.update(words)

	# 出現頻度順に単語を表示
	for word, count in counter.most_common(20):
    	print(f'{word}: {count}')

if __name__ == "__main__":
	main()
