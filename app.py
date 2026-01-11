import streamlit as st
import time
import urllib.parse
import random

# 1. 페이지 설정
st.set_page_config(page_title="AI MV Director", layout="wide")

# 2. 스타일 설정 (입력창 흰색 강제 고정)
st.markdown("""
<style>
    .stTextInput input, .stTextArea textarea {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    [data-testid="stSidebar"] {
        background-color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

# 3. 이미지 생성 함수
def generate_real_ai_image(prompt):
    encoded_prompt = urllib.parse.quote(prompt)
    random_seed = random.randint(1, 99999)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&nologo=true&seed={random_seed}&model=flux"
    return url

# 4. 사이드바 UI
with st.sidebar:
    st.title("🎬 AI MV Builder")
    st.caption("Developed by You")
    
    st.subheader("1. 노래 정보")
    song_title = st.text_input("노래 제목", value="Oh Boy")
    artist = st.text_input("아티스트", value="Red Velvet")
    
    st.subheader("2. 시나리오")
    default_scenario = """
    하이틴 로맨스, 샌프란시스코 언덕길 배경. 
    1. 가파른 언덕길에서 자전거 타는 소년과 부딪힐 뻔한 소녀.
    2. 햇빛을 등지고 서 있는 소년의 클로즈업. 레몬색 바람막이.
    3. 교실 책상 위, 머리만 남은 부서진 귀여운 동물 키링.
    4. 학교 체육관 앞, 나무 뒤에서 소년을 몰래 훔쳐보는 소녀.
    5. 밤, 침대 위에서 핸드폰 문자를 보며 이불을 차는 설레는 소녀.
    """
    scenario = st.text_area("장면 설명", value=default_scenario, height=300)
    
    st.info("⚠️ 5초 간격으로 이미지가 생성됩니다.")
    generate_btn = st.button("🚀 스토리보드 생성 시작", type="primary")

# 5. 메인 화면 로직
st.header(f"Project: {song_title} ({artist})")

if generate_btn:
    st.success("AI 감독이 작업을 시작했습니다!")
    st.divider()
    
    scenes_text = [s.strip() for s in scenario.split('\n') if s.strip() and s[0].isdigit()]
    
    if not scenes_text:
        st.error("시나리오 형식을 확인해주세요 (1. 내용, 2. 내용...)")
    else:
        for i, scene_desc in enumerate(scenes_text):
            st.markdown(f"### Scene {i+1}")
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.info(f"📄 내용: {scene_desc}")
                # 간단한 프롬프트 생성 로직
                base = "cinematic film still, 4k, realistic lighting, "
                prompt = base + "High teen romance movie vibe, pastel tone, " + scene_desc
                st.code(prompt, language="bash")

            with col2:
                with st.spinner(f"Scene {i+1} 그리는 중..."):
                    img_url = generate_real_ai_image(prompt)
                    st.image(img_url, caption=f"Scene {i+1}", use_container_width=True)
                    time.sleep(5) # Rate Limit 방지
            
            st.divider()
else:
    st.info("👈 왼쪽 사이드바의 버튼을 눌러주세요.")
