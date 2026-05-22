import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import urllib.request
import os

# 1. 스트림릿 클라우드 한글 깨짐 방지를 위한 폰트 다운로드 설정
@st.cache_data
def load_korean_font():
    font_url = "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Regular.ttf"
    font_path = "NanumGothic.ttf"
    
    # 폰트 파일이 없으면 다운로드
    if not os.path.exists(font_path):
        urllib.request.urlretrieve(font_url, font_path)
    
    # Matplotlib에 폰트 등록
    fe = fm.FontEntry(rc_context=False, name='NanumGothic', fname=font_path)
    fm.fontManager.ttflist.append(fe)
    plt.rcParams['font.family'] = 'NanumGothic'
    plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# 폰트 적용
load_korean_font()

# 2. 가상의 서울시 행정구별 연령대 인구 데이터 생성
@st.cache_data
def get_sample_data():
    age_groups = ['0-9세', '10대', '20대', '30대', '40대', '50대', '60대', '70대 이상']
    data = {
        '강남구': [40000, 55000, 80000, 95000, 90000, 85000, 60000, 45000],
        '송파구': [50000, 60000, 85000, 100000, 95000, 88000, 65000, 50000],
        '마포구': [25000, 30000, 75000, 70000, 55000, 50000, 35000, 30000],
        '종로구': [10000, 12000, 25000, 22000, 23000, 26000, 24000, 20000],
        '관악구': [20000, 25000, 110000, 85000, 60000, 55000, 45000, 38000]
    }
    return pd.DataFrame(data, index=age_groups)

df = get_sample_data()

# 3. 스트림릿 UI 구성
st.title("서울시 주요 행정구별 인구 통계")

# 행정구 선택 사이드바 (또는 메인 화면)
selected_gu = st.selectbox("행정구를 선택하세요", df.columns)

# 선택된 구의 데이터 가져오기
gu_data = df[selected_gu]

# 4. Matplotlib을 이용한 꺾은선 그래프 그리기
fig, ax = plt.subplots(figsize=(10, 6))

# 그래프 바탕색 설정 (연한 보라색 #F3E8FF)
fig.patch.set_facecolor('#F3E8FF')  # 전체 이미지 바탕색
ax.set_facecolor('#F3E8FF')         # 그래프 플롯 영역 바탕색

# 꺾은선 그래프 그리기 (색상: 빨간색, 마커 추가)
ax.plot(gu_data.index, gu_data.values, color='red', marker='o', linewidth=2)

# 그래프 서식 및 제목 설정
ax.set_title(f"서울시의 인구통계 ({selected_gu})", fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel("연령대", fontsize=12, labelpad=10)
ax.set_ylabel("인구수 (명)", fontsize=12, labelpad=10)
ax.grid(True, linestyle='--', alpha=0.5, color='#9333EA') # 보라색 톤의 그리드

# 스트림릿에 그래프 출력
st.pyplot(fig)
