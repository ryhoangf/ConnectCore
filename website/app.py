import google.generativeai as genai
from datetime import datetime
from flask import Flask, request, jsonify
from local_settings import API_KEY  # local_settingsからAPIキーを取得

# Flaskアプリケーションの初期化
app = Flask(__name__)

# APIキーの設定
genai.configure(api_key=API_KEY)

# モデルの初期化は一度だけ行う
model = genai.GenerativeModel('gemini-1.5-flash')

def analyze_sentiment_and_suggest_emojis(message):
    PROMPT = f"""
    You are an AI that analyzes the sentiment of the given message and suggests appropriate emoticons and emojis.
    Analyze the following message and determine if it is positive, negative, or neutral.
    Then suggest some emojis that match the sentiment.
    Please suggest emoticons specific to Japan and emojis specific to Vietnam.
    For example happy ":) :] =] =) :D =D :‑) :^) :‑] :3 =3 ;) :>"
    
    Message: "{message}"
    
    Your response should be in JSON format with the following structure:
    {{
        "sentiment": "positive" | "negative" | "neutral",
        "suggested_emojis": ["emoji1", "emoji2", "emoji3"]
        "suggested emoticons":["emoticon1", "emoticon2"]
    }}
    """
    
    # モデルにプロンプトを渡して感情分析と絵文字提案を行う
    response = model.generate_content(PROMPT)
    
    # 結果をJSONとしてパースする（必要に応じて）
    result = response.text.strip()
    
    return result
"""# テストメッセージ
message = "つらい"

# 感情分析と絵文字の提案を行う
result = analyze_sentiment_and_suggest_emojis(message)

# 結果を表示する
print(result)
"""

# 新しいエンドポイントの追加
@app.route('/suggest_emojis', methods=['POST'])
def suggest_emojis():
    # リクエストからメッセージを取得
    message_content = request.form.get('message_content', '')

    if not message_content:
        return jsonify({'error': 'Message content is required.'}), 400

    # メッセージに基づいて感情分析と絵文字の提案を実行
    result = analyze_sentiment_and_suggest_emojis(message_content)

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
