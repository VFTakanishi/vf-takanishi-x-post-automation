import os
import json
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

# 過去のトピックを保存するファイル
HISTORY_FILE = os.path.join(os.path.dirname(__file__), "post_history.json")

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def generate_x_posts(today_date, recent_topics):
    prompt = f"""
あなたはVF高西という自動車整備士です。X（旧Twitter）のポストを1日分（朝・昼・夕方の3つ）考えてください。
ポストの目的は私「VF高西」の認知を広げてnoteやpodcastへ導きたいのと、個人的にオファーをもらえるようにしたい。

【最新のXアルゴリズム・バズ傾向の適用】
- 会話を誘発する: 「いいね」よりも「リプライ」が27倍評価されます。最後に読者に質問を投げかけてください。
- ブックマーク（保存）を狙う: 「保存」は12倍評価されます。昼のお役立ち情報は保存したくなる具体性を持たせてください。
- リンクは本文に入れない: 本文に外部リンクを入れるとリーチが約50%減るため、noteやpodcastのリンクは「リプライ欄」に貼る前提で本文を構成してください。
- ハッシュタグは0〜1個: 多すぎるとスパム判定されます。
- 短く簡潔に: 280文字以内で、最初の1文で「あるある」や「気づき」を入れて惹きつけます。

【時間帯別の投稿内容】
- 朝: 認知獲得。日常の会話調で、必ずどこかに自動車、運転、整備の要素を入れる。
  例：タイヤの溝、いつ見た？って聞くと大体の人が「車検の時」って答えるんだよね。でも実は溝より怖いのが『年数』。ゴムって数年でカチカチになって、ある日突然グリップを失うから本当に怖い。ヒビ割れが見えたら要注意。みんなのタイヤ、何年目か知ってる？
- 昼：完全にお役立ち情報。業界ニュース、法改正、暑さ寒さと車の注意点、整備の豆知識
  ※重要：現在販売中の10,000円の有料記事（信用できない整備士を見抜く魔法の質問集）への導線として、記事の核心部分をあえて隠し、プロフィールの固定ポストへ誘導する「寸止め」の形にする。
- 夕方：人柄、現場感、相談歓迎の空気づくり。プロとしての自信を見せる。

【超重要：文章のトーン＆マナー】
- 人間が日常的に使う会話調にする。一人称は「俺」か省略（「私」は使わない）。文末は「〜だよ」「〜なんだよね」「〜してね」など口語。
- 悪い例（不自然な表現）：「エアコンの効きって、派手な知識より最初の落ち着きのほうが大事だったりします。慌てないだけで、その後の判断ミスはかなり減らせます。」「言葉にしづらい違和感も大事なことって、整備をしていると本当によくあります。深刻になってからより、なんか気になるの段階で話してもらえるほうが、やっぱり早いです。」←このような意味不明で不自然な文章は絶対に避ける。

【その他のルール】
- そのままコピペできるようにテキストで、ポスト内容の意図は不要で、下書きのみ提案して。
- 朝の挨拶（「VF高西です」など）は不要。

【重複回避ルール】
内容は少なくとも1週間の間で重複しないようにしてください。
以下のトピックは直近1週間で使用済みのため、**絶対に避けて**ください：
{', '.join(recent_topics) if recent_topics else 'なし'}

今日の日付は {today_date} です。

--- 形式 ---
【朝】
（ポスト本文）

【昼】
（ポスト本文）

【夕方】
（ポスト本文）
"""

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "あなたはプロのX（旧Twitter）投稿作成アシスタント兼、現役自動車整備士です。自然な日本語の会話調を厳守し、アルゴリズムに最適化した投稿を作成します。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1500,
    )
    return response.choices[0].message.content.strip()

def extract_topics(posts_text):
    # GPTを使って投稿からトピックを抽出
    prompt = f"以下の3つのポストの核となるトピック（例：タイヤの寿命、エアコンフィルター、異音の相談など）を、カンマ区切りで3つ抽出してください。\n\n{posts_text}"
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=50
        )
        return [t.strip() for t in response.choices[0].message.content.split(',')]
    except:
        return ["不明なトピック"]

def send_line_message(user_id, message_text):
    try:
        # メッセージの冒頭に案内を追加
        full_message = f"【本日のXポスト案】\n\n{message_text}\n\n※そのままコピペして使えます。\n※note/podcastのURLは、各ポストの「リプライ（ツリー）」に繋げてください（本文に入れるとリーチが下がります）。"
        line_bot_api.push_message(user_id, TextSendMessage(text=full_message))
        print(f"LINEメッセージを送信しました: {user_id}")
    except Exception as e:
        print(f"LINEメッセージの送信に失敗しました: {e}")

if __name__ == "__main__":
    # 日本時間 (JST) での現在時刻を取得
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
    today_str = now.strftime("%Y年%m月%d日（%A）")
    
    # 履歴の読み込みと1週間以内のトピック抽出
    history = load_history()
    recent_topics = []
    valid_history = []
    
    for entry in history:
        try:
            entry_date = datetime.datetime.fromisoformat(entry['date'])
            if (now - entry_date).days < 7:
                recent_topics.extend(entry.get('topics', []))
                valid_history.append(entry)
        except:
            pass
    
    print(f"{today_str} の1日分のXポスト案を生成中...")
    posts = generate_x_posts(today_str, recent_topics)
    print("生成完了:\n", posts)
    
    # 新しいトピックを抽出して履歴に保存
    new_topics = extract_topics(posts)
    valid_history.append({
        'date': now.isoformat(),
        'topics': new_topics
    })
    save_history(valid_history)

    if LINE_USER_ID and LINE_CHANNEL_ACCESS_TOKEN:
        send_line_message(LINE_USER_ID, posts)
    else:
        print("LINEの環境変数が設定されていません。")
