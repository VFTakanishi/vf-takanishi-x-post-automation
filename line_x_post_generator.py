import os
import datetime
import openai
from linebot import LineBotApi
from linebot.models import TextSendMessage
from dotenv import load_dotenv

load_dotenv()

# 環境変数からAPIキーなどを取得
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_USER_ID = os.getenv("LINE_USER_ID") # 送信先のユーザーID

openai.api_key = OPENAI_API_KEY
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

def generate_x_posts(today_date):
    prompt = f"""
あなたはVF高西という自動車整備士です。X（旧Twitter）のポストを1日分（朝・昼・夕方の3つ）考えてください。
ポストの目的は私「VF高西」の認知を広げてnoteやpodcastへ導きたいのと、個人的にオファーをもらえるようにしたい。
アルゴリズムやバズ情報を取得、寄せて自動でポストを考えて提案してください。

【時間帯別の投稿内容】
- 朝: 認知獲得。ただし毎回どこかに自動車、運転、整備の要素を入れる。
  例：タイヤは溝だけでなく年数も確認しよう。ゴムが劣化すると弾性が無くなってグリップしなくなったり突然バーストの恐れがあります。
  例：事故防ぐ運転はただ一つ、車間距離を開けよう。
- 昼：完全にお役立ち情報。業界ニュース、法改正、暑さ寒さと車の注意点、整備の豆知識
  ※重要：現在販売中の10,000円の有料記事（信用できない整備士を見抜く魔法の質問集）への導線として、記事の核心部分をあえて隠し、プロフィールの固定ポストへ誘導する「寸止め」の形にする。
- 夕方：人柄、現場感、相談歓迎の空気づくり

【重要：文章のトーン＆マナー】
- 人間が日常的に使う会話調にする。
- 悪い例（不自然な表現）：「エアコンの効きって、派手な知識より最初の落ち着きのほうが大事だったりします。慌てないだけで、その後の判断ミスはかなり減らせます。」「言葉にしづらい違和感も大事なことって、整備をしていると本当によくあります。深刻になってからより、なんか気になるの段階で話してもらえるほうが、やっぱり早いです。」←このような意味不明で不自然な文章は絶対に避ける。
- 良い例：実際のポストを拾って学習し、同じように自然な文章を考える。

【その他のルール】
- そのままコピペできるようにテキストで、ポスト内容の意図は不要で、下書きのみ提案して。
- 内容は少なくとも1週間の間で重複しないように。
  例：今週日曜日のポスト内容は次の日曜日までは提案しない。
- 朝の挨拶（「VF高西です」など）は不要。

今日の日付は {today_date} です。

--- 形式 ---
【朝のポスト案】
（内容）

【昼のポスト案】
（内容）

【夕方のポスト案】
（内容）
"""

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "あなたはプロのX（旧Twitter）投稿作成アシスタントです。自然な日本語の会話調を厳守します。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1500,
    )
    return response.choices[0].message.content.strip()

def send_line_message(user_id, message_text):
    try:
        line_bot_api.push_message(user_id, TextSendMessage(text=message_text))
        print(f"LINEメッセージを送信しました: {user_id}")
    except Exception as e:
        print(f"LINEメッセージの送信に失敗しました: {e}")

if __name__ == "__main__":
    # 日本時間 (JST) での現在時刻を取得
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
    today_str = now.strftime("%Y年%m月%d日（%A）")
    
    print(f"{today_str} の1日分のXポスト案を生成中...")
    posts = generate_x_posts(today_str)
    print("生成完了:\n", posts)

    if LINE_USER_ID and LINE_CHANNEL_ACCESS_TOKEN:
        send_line_message(LINE_USER_ID, posts)
    else:
        print("LINEの環境変数が設定されていません。")
