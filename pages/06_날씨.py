import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 한글 폰트 설정 (스트림릿 클라우드 환경 고려)
# 스트림릿 클라우드는 기본적으로 한글 폰트가 없으므로 시스템 폰트를 사용하거나 무시하도록 설정합니다.
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False # 마이너스 기호 깨짐 방지

# 1. 데이터 로드 및 전처리
@st.cache_data
def load_data():
    # CSV 파일 읽기
    df = pd.read_csv('seoul.csv')
    
    # 컬럼명 공백 제거
    df.columns = df.columns.str.strip()
    
    # 날짜 데이터 전처리 (공백 및 탭 문자 제거)
    df['날짜'] = df['날짜'].astype(str).str.replace(r'\s+', '', regex=True)
    
    # datetime 형식으로 변환
    df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')
    
    # 결측치 제거 및 필요한 파생변수(연, 월, 일) 생성
    df = df.dropna(subset=['날짜'])
    df['연도'] = df['날짜'].dt.year
    df['월'] = df['날짜'].dt.month
    df['일'] = df['날짜'].dt.day
    
    return df

# 데이터 불러오기
try:
    df = load_data()
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

# 앱 제목
st.title("📅 역대 서울 기온 데이터 분석")

# 2. 사용자 입력 (월, 일 선택)
st.sidebar.header("날짜 선택")
selected_month = st.sidebar.selectbox("월을 선택하세요", sorted(df['월'].unique()), index=9) # 기본값 10월
selected_day = st.sidebar.selectbox("일을 선택하세요", sorted(df[df['월'] == selected_month]['일'].unique()))

# 3. 데이터 필터링
filtered_df = df[(df['월'] == selected_month) & (df['일'] == selected_day)].sort_values('연도')

# 선택된 날짜 표시
st.subheader(f"📊 {selected_month}월 {selected_day}일의 연도별 기온 변화")

if filtered_df.empty:
    st.warning("선택한 날짜의 데이터가 존재하지 않습니다.")
else:
    # 4. 시각화 (Matplotlib 꺾은선 그래프)
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 최고기온 (핫핑크: deeppink 또는 hotpink)
    ax.plot(filtered_df['연도'], filtered_df['최고기온(℃)'], marker='o', color='hotpink', label='Max Temp', linewidth=2)
    
    # 최저기온 (연한 파란색: lightskyblue 또는 lightblue)
    ax.plot(filtered_df['연도'], filtered_df['최저기온(℃)'], marker='o', color='lightskyblue', label='Min Temp', linewidth=2)
    
    # 그래프 속성 설정 (요청 사항 반영)
    ax.set_title("Temperature Analysis by Date", fontsize=16, pad=15) # 스트림릿 클라우드 한글 깨짐 방지용 영어 제목
    # 만약 로컬 환경이거나 한글 폰트 설정이 완료되었다면 아래 줄 주석을 해제하세요.
    # ax.set_title("날짜별 기온 분석", fontsize=16, pad=15)
    
    ax.set_xlabel("Year", fontsize=12) # 연도
    ax.set_ylabel("Temperature", fontsize=12) # 온도
    
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(loc='best')
    
    # 스트림릿에 그래프 출력
    st.pyplot(fig)
    
    # 데이터 테이블로도 확인하기 (선택 사항)
    with st.expander("상세 데이터 보기"):
        st.dataframe(filtered_df[['연도', '평균기온(℃)', '최저기온(℃)', '최고기온(℃)']].reset_index(drop=True))
