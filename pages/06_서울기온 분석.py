import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import os

# 1. 데이터 로드 및 전처리 함수
@st.cache_data
def load_data():
    # 현재 파일(pages/app.py)의 절대 경로를 기준 폴더로 설정
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 상위 폴더(..)에 위치한 'seoul.csv' 파일 경로 설정
    file_path = os.path.join(current_dir, '..', 'seoul.csv')
    file_path = os.path.abspath(file_path)
    
    # 파일 존재 여부 확인 후 명확한 에러 메시지 출력
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"'{file_path}' 위치에서 seoul.csv 파일을 찾을 수 없습니다. 파일이 상위 폴더에 있는지 다시 확인해주세요.")
    
    # 인코딩 에러(utf-8 에러) 해결을 위해 cp949 및 euc-kr 지원
    try:
        df = pd.read_csv(file_path, encoding='cp949')
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='euc-kr')
    
    # 컬럼명 앞뒤 공백 제거
    df.columns = df.columns.str.strip()
    
    # 날짜 데이터 전처리 (공백 및 탭 문자 제거)
    df['날짜'] = df['날짜'].astype(str).str.replace(r'\s+', '', regex=True)
    df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')
    
    # 기온 데이터와 날짜의 결측치 제거
    df = df.dropna(subset=['날짜', '최고기온(℃)', '최저기온(℃)'])
    
    # 분석에 필요한 파생 변수(연도, 월, 일) 생성
    df['연도'] = df['날짜'].dt.year
    df['월'] = df['날짜'].dt.month
    df['일'] = df['날짜'].dt.day
    return df

# 데이터 불러오기 실행
try:
    df = load_data()
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다:\n\n{e}")
    st.stop()

# 앱 제목
st.title("📅 서울 기온 분석 및 미래 예측")

# 2. 사용자 입력 (사이드바 제어)
st.sidebar.header("설정")
selected_month = st.sidebar.selectbox("월을 선택하세요", sorted(df['월'].unique()), index=9) # 기본값 10월
selected_day = st.sidebar.selectbox("일을 선택하세요", sorted(df[df['월'] == selected_month]['일'].unique()))

# 미래 예측 연도 입력창
max_year_in_data = int(df['연도'].max())
future_year = st.sidebar.number_input(
    f"예측할 미래 연도를 입력하세요 (데이터 최대 연도: {max_year_in_data}년)", 
    min_value=max_year_in_data + 1, 
    max_value=2100, 
    value=2030
)

# 3. 사용자 선택 날짜에 맞춰 데이터 필터링
filtered_df = df[(df['월'] == selected_month) & (df['일'] == selected_day)].sort_values('연도')

if filtered_df.empty:
    st.warning("선택한 날짜의 데이터가 존재하지 않습니다.")
else:
    # 4. 머신러닝(선형 회귀)을 이용한 기온 추세 학습 및 예측
    X = filtered_df[['연도']].values
    y_max = filtered_df['최고기온(℃)'].values
    y_min = filtered_df['최저기온(℃)'].values
    
    # 모델 정의 및 학습
    model_max = LinearRegression().fit(X, y_max)
    model_min = LinearRegression().fit(X, y_min)
    
    # 미래 기온 예측값 계산
    pred_max = model_max.predict([[future_year]])[0]
    pred_min = model_min.predict([[future_year]])[0]
    
    # 상단에 예측 결과값 요약 출력
    st.subheader(f"📊 {selected_month}월 {selected_day}일의 기온 분석 및 예측")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label=f"🔮 {future_year}년 예상 최고기온", value=f"{pred_max:.2f} °C")
    with col2:
        st.metric(label=f"🔮 {future_year}년 예상 최저기온", value=f"{pred_min:.2f} °C")
        
    # 그래프에 미래 점선을 함께 그리기 위해 예측 데이터 행 추가
    future_row = pd.DataFrame({
        '연도': [future_year],
        '최고기온(℃)': [pred_max],
        '최저기온(℃)': [pred_min]
    })
    plot_df = pd.concat([filtered_df, future_row], ignore_index=True)

    # 5. Plotly 라이브러리를 이용한 인터랙티브 그래프 (마우스 오버 기능 자동 탑재)
    fig = go.Figure()

    # 과거 최고기온 선 (핫핑크)
    fig.add_trace(go.Scatter(
        x=filtered_df['연도'], y=filtered_df['최고기온(℃)'],
        mode='lines+markers', name='최고기온 (과거)',
        line=dict(color='hotpink', width=2),
        hovertemplate='<b>%{x}년 최고기온</b><br>%{y:.1f} °C<extra></extra>'
    ))

    # 미래 예측 최고기온 선 (핫핑크 점선)
    fig.add_trace(go.Scatter(
        x=plot_df['연도'].iloc[-2:], y=plot_df['최고기온(℃)'].iloc[-2:],
        mode='lines+markers', name='최고기온 (예측)',
        line=dict(color='hotpink', width=2, dash='dash'),
        hovertemplate='<b>%{x}년 최고기온(예측)</b><br>%{y:.1f} °C<extra></extra>'
    ))

    # 과거 최저기온 선 (연한 파란색)
    fig.add_trace(go.Scatter(
        x=filtered_df['연도'], y=filtered_df['최저기온(℃)'],
        mode='lines+markers', name='최저기온 (과거)',
        line=dict(color='lightskyblue', width=2),
        hovertemplate='<b>%{x}년 최저기온</b><br>%{y:.1f} °C<extra></extra>'
    ))

    # 미래 예측 최저기온 선 (연한 파란색 점선)
    fig.add_trace(go.Scatter(
        x=plot_df['연도'].iloc[-2:], y=plot_df['최저기온(℃)'].iloc[-2:],
        mode='lines+markers', name='최저기온 (예측)',
        line=dict(color='lightskyblue', width=2, dash='dash'),
        hovertemplate='<b>%{x}년 최저기온(예측)</b><br>%{y:.1f} °C<extra></extra>'
    ))

    # 그래프 축 및 디자인 레이아웃 설정
    fig.update_layout(
        title=dict(text="날짜별 기온 분석", font=dict(size=20), x=0.5), # 제목 중앙 정렬
        xaxis_title="연도",
        yaxis_title="온도",
        hovermode="x unified", # 마우스를 올리면 같은 연도의 데이터가 세로선으로 모여서 보임
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    # 스트림릿 웹페이지에 차트 그리기
    st.plotly_chart(fig, use_container_width=True)
