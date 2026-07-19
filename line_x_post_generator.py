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

【重要：昼のポスト戦略（有料記事への導線）】
昼のポストは、10,000円の有料記事の「核心部分」をあえて隠し、読者の知的好奇心を刺激してプロフィールの固定ポストへ誘導します。
記事タイトル：「信用できない整備士を見抜く魔法の質問集！チューニングショップ整備士が本音で教える、車で損しないための話」

昼のポストのルール：
- 「1ポスト1トピック」を徹底する。1つのポストで複数のチェックポイントを出さない。
- 以下のトピックから1つだけ選び、核心部分（なぜそうなのか？どうすればいいのか？）は書かずに「寸止め」する。
  1. アライメントの質問（「基準値」という言葉の裏にあるリスク）。
  2. オイルの特徴への質問（ロジカルな回答があるか）。
  3. ECUリミッター設定の聞き方（店がデータを理解しているかの判別）。
  4. ECUの純正戻しができるかどうかの重要性。
  5. タイヤの空気圧への質問から見えるショップの知見。
  6. セミバケの構造の違いを説明できるか。
  7. 実際に経験した「選んではいけないパーツやメーカー」の教訓（特定名は出さず、選ばない理由の入り口だけ）。
  8. ショップに好かれる客になるための、意外な心得。
- 炎上を防ぐため、特定の店を攻撃せず「こういう答えが返ってくる店なら安心・信頼できる」というポジティブな見極め方にする。
- 読者が「自分の車は大丈夫か？」と気になり、解決策を有料記事で確認したくなるように書く。
- 最後に必ず「もっと詳しく知りたい人は、プロフィールの固定ポストを見てください」という一文を添える。

【全体のルール】
- 朝（6:30頃）: 認知獲得。自動車、運転、整備の要素を入れる。※挨拶は不要。
- 昼（11:30頃）: 上記の有料記事の内容を1トピックだけ「寸止め」で紹介し、固定ポストへ誘導する。
- 夕方（17:30頃）: 人柄、現場感、相談歓迎の空気づくり。noteやpodcastへの誘導を最後に添える。
- 事実確認を徹底し、経験していないエピソードや確認できないニュースへの言及は避ける。
- 整備士ならではの視点・現場の経験を自然な形で入れる。
- 余計な強調表現を削り、シンプルに言い切る。
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
