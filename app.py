from dotenv import load_dotenv

load_dotenv()
import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# 環境変数の読み込み
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")

# テーマの選択肢を関数より前に定義
theme_1 = "運動"
theme_2 = "サッカー"

def get_llm_response(user_message, selected_theme):
    """
    LLMからの回答を取得する処理
    """
    # モデルのオブジェクトを用意
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.5, api_key=OPENAI_API_KEY)

    # 選択テーマに応じて使用するプロンプトのシステムメッセージを分岐
    if selected_theme == theme_1:
        system_message = """
            あなたは運動の専門家です。専門家としてユーザーからの質問に回答してください。
            学術的な知識を用いて、具体的かつ実践的なアドバイスを提供してください。
        """
    else:
        system_message = """
            あなたはサッカー専門家です。専門家としてユーザーからの質問に回答してください。
            有名選手の実例をあげて説明してください。
        """
    
    # メッセージリストの用意
    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=user_message)
    ]

    # LLMからの回答取得
    response = llm.invoke(messages)  # ← .invoke() を使うのが新仕様で安定
    return getattr(response, "content", str(response))

# 案内文の表示
st.title("相談アプリ")
st.write("運動・サッカーに関する生成AIチャット相談アプリです。")

# 相談テーマ選択用のラジオボタン
selected_theme = st.radio(
    "【テーマ】",
    [theme_1, theme_2]
)

# 区切り線
st.divider()

# チャット欄
user_message = st.text_input(label="相談内容を入力してください")

# ボタン
if st.button("送信"):
    # 区切り線
    st.divider()
    # LLMからの回答取得
    response = get_llm_response(user_message, selected_theme)
    # LLMからの回答表示
    st.write(response)