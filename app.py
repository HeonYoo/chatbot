import os
import openai
import streamlit as st

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 챗봇의 응답을 처리하는 함수
def response(user_input_message, state_message_history):
  
  # 채팅 메세지 히스토리에 사용자 메세지 추가
  state_message_history.append({'role': 'user',
                                'content': user_input_message})
    
  # 채팅 완성 API를 호출

  respond = openai.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=state_message_history,
    temperature=0.2,
    openai_api_key=OPENAI_API_KEY
  )
  
  # 응답 JSON에서 출력 텍스트를 추출
  ai_respond_message = respond.choices[0].message.content

  # 챗봇 메세지 히스토리에 어시스트 메세지 추가
  state_message_history.append((user_input_message, ai_respond_message))

  print(ai_respond_message)
  return state_message_history

context = """
    너는 경제 용어 및 사건에 익숙하지 않은 사회 초년생들이 경제 뉴스를 보다 쉽게 이해할 수 있도록 돕는 선생님이야. 경제기사를 읽던 사용자가 모르는 (경제 관련) 용어나 사건을 질문하면 그에 대해 간략하게 설명한 후, 그 용어가 경제에서 주로 사용되는 맥락 혹은 그 사건이 현 경제에 끼친 영향력에 대해 친절하게 설명해줘.
  """
  
system_message = [{
  'role': 'system',
  'content': context
}]

# 화면 구성하기
st.title("경제 뉴스 리딩 메이트")
st.title("나는 _:blue[경제 뉴스 리딩 메이트]_ 야. :sunglasses:")
st.title("뉴스를 읽다가 이해하기 어려운 부분이 있으면 언제든지 물어봐줘! 내가 도와줄게 :)")
st.title("")

content = st.text_input('리딩 메이트가 어떻게 설명할 지 고민중입니다..')

if st.button('시작하기'):
  with st.spinner("머리 굴리는 중..."):
    result = response(content, system_message)
    st.write("궁금증이 풀릴 시간이야!", result)
