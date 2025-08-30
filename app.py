import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from dotenv import load_dotenv

# .envファイルから環境変数をロード
load_dotenv() 

if not os.getenv("OPENAI_API_KEY"):
    st.error("環境変数 OPENAI_API_KEY が設定されていません。")

# LLMの初期化
# model_name="gpt-4o-mini" を使用しています。必要に応じて変更してください。
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

# 専門家に応じたシステムメッセージを生成する関数
def get_system_message(expert_type):
    if expert_type == "ITエンジニア":
        return "あなたはプログラミング、システム設計、ネットワーク、セキュリティなど、IT技術に関する深い専門知識を持つITエンジニアです。ユーザーの質問に対して、技術的な視点から正確で実用的な情報を提供してください。"
    elif expert_type == "心理カウンセラー":
        return "あなたは人間の感情、行動、心の健康に関する専門知識を持つ心理カウンセラーです。ユーザーの悩みや質問に対して、共感的な視点からアドバイスや考察を優しく提供してください。"
    elif expert_type == "旅行コンシェルジュ":
        return "あなたは国内外の旅行先に関する豊富な知識を持つ旅行コンシェルジュです。ユーザーの希望や予算に応じて、最適な旅行プランの提案、おすすめのスポット、現地の文化情報などを提供し、思い出に残る旅の計画をサポートしてください。"
    else:
        return "あなたは親切なAIアシスタントです。ユーザーの質問に丁寧にお答えします。"


# LLMからの回答を取得する関数
def get_llm_response(user_input: str, expert_type: str) -> str:
    """
    ユーザーの入力と選択された専門家タイプに基づいて、LLMからの回答を返します。
    """
    system_message_content = get_system_message(expert_type)
    messages = [
        SystemMessage(content=system_message_content),
        HumanMessage(content=user_input),
    ]
    try:
        result = llm.invoke(messages)
        return result.content
    except Exception as e:
        st.error(f"LLMとの通信中にエラーが発生しました")
        return "回答を生成できませんでした。"
    

# Streamlitアプリのタイトル
st.title("LLM機能を搭載したWebアプリ")

# アプリの概要と操作方法の表示
st.markdown("""
このWebアプリは、入力したテキストに対して、選択した専門家の視点からLLM（大規模言語モデル）が回答を生成します。
""")

st.markdown("---")

# 専門家選択のラジオボタン
expert_options = ["ITエンジニア", "心理カウンセラー", "旅行コンシェルジュ", "一般的なアシスタント"]
selected_expert = st.radio("LLMに振る舞わせる専門家を選択してください:", expert_options)

# 入力フォーム
user_input = st.text_area("ここに質問を入力してください", height=150)

# 回答生成ボタン
if st.button("回答を生成"):
    if user_input:
        with st.spinner("LLMが回答を生成中です..."):
            response = get_llm_response(user_input, selected_expert)
            if "回答を生成できませんでした。" in response: 
                st.error("エラーにより回答を生成できませんでした。もう一度お試しください。")
            else:
                st.subheader("LLMからの回答:")
                st.write(response)
    else:
        st.warning("質問を入力してください。")