import streamlit as st

# 1. 페이지 설정
st.set_page_config(
    page_title="MBTI별 추천 음식",
    page_icon="🍕",
    layout="centered"
)

# 2. MBTI별 데이터 설정
mbti_food_data = {
    "ISTJ": {"food": "국밥 (설렁탕/돼지국밥)", "desc": "전통적이고 든든하며, 배신하지 않는 확실하고 효율적인 한 끼!", "emoji": "🍲"},
    "ISFJ": {"food": "집밥 스타일 백반", "desc": "정성이 가득 담겨있고 마음을 따뜻하고 편안하게 해주는 집밥.", "emoji": "🍱"},
    "INFJ": {"food": "정갈한 한식 코스 요리 또는 평양냉면", "desc": "깊은 맛과 철학이 느껴지며, 깔끔하고 정성스러운 음식.", "emoji": "🥢"},
    "INTJ": {"food": "분자요리 또는 파인다이닝", "desc": "분석적이고 완벽주의적인 성향에 맞는, 실험적이고 정교한 요리.", "emoji": "🍽️"},
    "ISTP": {"food": "수제 버거와 감자튀김", "desc": "복잡한 형식 없이 손으로 들고 바로 먹을 수 있는 효율적이고 확실한 맛.", "emoji": "🍔"},
    "ISFP": {"food": "예쁜 디저트 (마카롱/크로플)", "desc": "시각적인 아름다움과 달콤한 감성을 동시에 충족시키는 음식.", "emoji": "🧇"},
    "INFP": {"food": "감성 브런치 또는 퓨전 요리", "desc": "낭만적이고 독창적인 분위기 속에서 즐기는 이야기 가득한 요리.", "emoji": "🥞"},
    "INTP": {"food": "라멘 또는 밀키트 요리", "desc": "독창적이면서도 조리 과정이 논리적이고 미니멀한 음식.", "emoji": "🍜"},
    "ESTP": {"food": "매운 떡볶이 또는 마라탕", "desc": "지루한 맛은 가라! 짜릿하고 강렬한 자극을 주는 트렌디한 음식.", "emoji": "🌶️"},
    "ESFP": {"food": "삼겹살 구이와 소주", "desc": "여럿이 모여 시끌벅적하게 구워 먹으며 즐길 수 있는 최고의 파티 음식.", "emoji": "🥓"},
    "ENFP": {"food": "멕시칸 타코 또는 마라훠궈", "desc": "다채로운 재료와 소스로 매번 새로운 조합을 만들 수 있는 흥미로운 음식.", "emoji": "🌮"},
    "ENTP": {"food": "이색 세계 요리 (인도 커리/태국 똠양꿍)", "desc": "평범한 건 거부한다! 호기심을 자극하는 이국적이고 독특한 맛.", "emoji": "🍛"},
    "ESTJ": {"food": "스테이크와 와인", "desc": "확실한 보상! 성공적이고 체계적인 하루를 마무리하는 클래식한 고급 요리.", "emoji": "🥩"},
    "ESFJ": {"food": "이탈리안 파스타와 피자", "desc": "친구, 가족들과 함께 나눠 먹으며 정을 나누기 가장 좋은 대중적인 요리.", "emoji": "🍕"},
    "ENFJ": {"food": "정성 가득한 수제 만두 또는 전골", "desc": "주변 사람들을 대접하기 좋고, 함께 먹으면 마음까지 따뜻해지는 음식.", "emoji": "🥟"},
    "ENTJ": {"food": "고급 오마카세", "desc": "리더의 품격에 어울리는, 셰프가 주도하는 완벽하고 효율적인 최고의 코스.", "emoji": "🍣"},
}

# 3. UI 메인 타이틀
st.title("✨ MBTI별 찰떡궁합 추천 음식 ✨")
st.write("당신의 MBTI를 선택하시면 가장 잘 어울리는 음식을 추천해 드립니다.")
st.markdown("---")

# 4. 메인 화면 중앙에 MBTI 선택 창 배치
# 빈 열을 좌우에 두어 선택 창이 가운데로 모이게 조절합니다.
left_col, center_col, right_col = st.columns([1, 2, 1])

with center_col:
    mbti_list = list(mbti_food_data.keys())
    selected_mbti = st.selectbox("당신의 MBTI는 무엇인가요?", mbti_list)

st.markdown("---")

# 5. 결과 화면 출력
if selected_mbti:
    food_info = mbti_food_data[selected_mbti]
    
    st.subheader(f"🔮 {selected_mbti} 유형을 위한 추천")
    
    # 결과 레이아웃
    with st.container():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown(f"<h1 style='text-align: center; font-size: 80px; margin: 0;'>{food_info['emoji']}</h1>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"### 추천 음식: **{food_info['food']}**")
            st.write(f"**이유:** {food_info['desc']}")

st.markdown("---")
st.caption("재미로 보는 MBTI별 추천 요리 앱입니다. 오늘 메뉴 선택에 도움이 되셨길 바랍니다! 😉")
