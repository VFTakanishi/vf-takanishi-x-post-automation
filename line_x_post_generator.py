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
ポストの目的はVF高西の認知を広げてnoteやpodcastへ導き、個人的にオファーをもらえるようにすることです。
人間が日常的に使う会話調で、コピペできるようにテキストのみで提案してください。ポスト内容の意図は不要です。

以下のルールを厳守してください。
- 朝（6:30頃）: 認知獲得。毎回どこかに自動車、運転、整備の要素を入れる。※挨拶（VF高西です、など）は不要。
- 昼（11:30頃）: 完全にお役立ち情報。業界ニュース、法改正、暑さ寒さと車の注意点、整備の豆知識。
- 夕方（17:30頃）: 人柄、現場感、相談歓迎の空気づくり。noteやpodcastへの誘導を最後に添える。
- 事実確認を徹底し、経験していないエピソードや確認できないニュースへの言及は避ける。
- カレンダー・祝日・曜日は必ず正確に確認する。事実でないことを事実として書かない。
- 「〜が始まっている地域が多い」「〜が目立つ」のように、事実に基づいた柔らかい表現ならOK。
- 整備士ならではの視点・現場の経験を自然な形で入れる。
- 余計な強調表現（「一年で一番」「本当に」など）を削る。シンプルに言い切る。
- 締めのフレーズを使い回さない。
- 「実は」を多用しない。
- SNS上で語りかけている文脈を意識する。
- 改行を適度に入れて読みやすくする。

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
            {"role": "system", "content": "あなたはプロのX（旧Twitter）投稿作成アシスタントです。"},
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
