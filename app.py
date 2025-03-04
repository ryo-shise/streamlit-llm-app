import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# ローカル環境用に .env を読み込む
load_dotenv()

# 環境に応じて OpenAI API キーを取得
api_key = os.getenv("OPENAI_API_KEY")  # デフォルトは .env から取得

# Streamlit Community Cloud では st.secrets を使用
if not api_key and "OPENAI_API_KEY" in st.secrets:
    api_key = st.secrets["OPENAI_API_KEY"]

# APIキーが取得できなかった場合のエラーハンドリング
if not api_key:
    st.error("OpenAI APIキーが設定されていません。")
    st.stop()  # これ以上処理を進めないようにする

# LLMの初期化
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.5, openai_api_key=api_key)

# 専門家の種類を選択するラジオボタン
expert_type = st.radio(
    "専門家の種類を選択してください:",
    ("食の専門家", "旅行の専門家")
)

# 入力フォーム
input_text = st.text_input("質問を入力してください:")

# プロンプトを生成する関数
def generate_prompt(input_text, expert_type):
    if expert_type == "食の専門家":
        system_message = "あなたは食の専門家です。ユーザーの質問に回答してください。"
    else:
        system_message = "あなたは旅行の専門家です。ユーザーの質問に回答してください。"

    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=input_text)
    ]

    return messages

# LLMからの回答を取得する関数
def get_llm_response(input_text, expert_type):
    messages = generate_prompt(input_text, expert_type)
    result = llm(messages)
    return result.content

# ボタンが押されたときの処理
if st.button("送信"):
    if input_text:
        response = get_llm_response(input_text, expert_type)
        st.write("LLMからの回答:")
        st.write(response)
    else:
        st.write("質問を入力してください。")
        