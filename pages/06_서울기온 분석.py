import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import os

# 1. 데이터 로드 및 전처리
@st.cache_data
def load_data():
    # 현재 파일(pages/app.py)의 절대 경로를 찾습니다.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # ❗ 중요: 'pages' 폴더보다 한 단계 위(상위 폴더)에 있는 'seoul.csv'를 가리키도록 설정합니다.
    file_path = os.path.join(current_dir, '..', 'seoul.csv')
    
    # 경로가 올바르게 잡혔는지 절대 경로로 깔끔하게 정돈합니다.
    file_path = os.path.abspath(file_path)
    
    # 파일 존재 여부 확인 후 명확한 예외 처리
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"'{file_path}' 위치에서 seoul.csv 파일을 찾을 수 없습니다. 파일이 상위 폴더에 있는지 다시 한번 확인해주세요.")
    
    # CSV 파일 읽기
    df = pd.read_csv(file_path)
    
    # 컬럼명 공백 제거
    df.columns = df.columns.str.strip()
    
    # 날짜 데이터 전처리 (공백 및 탭 문자 제거)
    df['날짜'] = df['날짜'].astype(str).str.replace(r'\s+', '', regex=True)
    df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')
    
    # 기온 데이터와 날짜의 결측치 제거
    df = df.dropna(subset=['날짜', '최고기온(℃)', '최저기온(℃)'])
    
    # 파생 변수 생성
    df['연도'] = df['날짜'].dt.year
    df['월'] = df['날짜'].dt.month
    df['일'] = df['날짜'].dt.day
    return df

# --- 이하 코드(사용자 입력, 예측, Plotly 그래프 부분)는 이전과 동일합니다 ---
try:
    df = load_data()
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다:\n\n{e}")
    st.stop()

# 앱 제목
st.title("📅 서울 기온 분석 및 미래 예측")

# 2. 사용자 입력 (사이드바)
st.sidebar.header("설정")
selected_month = st.sidebar.selectbox("월을 선택하세요", sorted(df['월'].unique()), index=9)
selected_day = st.sidebar.selectbox("일을 선택하세요", sorted(df[df['월'] == selected_month]['일'].unique()))

# 미래 예측 연도 선택
max_year_in_data = int(df['연도'].max())
future_year = st.sidebar.number_input(
    f"예측할 미래 연도를 입력하세요 (데이터 최대 연도: {max_year_in_data}년)", 
    min_value=max_year_in_data + 1, 
    max_value=2100, 
    value=2030
)

# 3. 데이터 필터링
filtered_df = df[(df['월'] == selected_month) & (df['일'] == selected_day)].sort_values('연도')

if filtered_df.empty:
    st.warning("선택한 날짜의 데이터가 존재하지 않습니다.")
else:
    # 4. 선형 회귀를 이용한 기온 예측
    X = filtered_df[['연도']].values
    y_max = filtered_df['최고기온(℃)'].values
    y_min = filtered_df['최저기온(℃)'].values
    
    model_max = LinearRegression().fit(X, y_max)
    model_min = LinearRegression().fit(X, y_min)
    
    pred_max = model_max.predict([[future_year]])[0]
    pred_min = model_min.predict([[future_year]])[0]
    
    # 예측 결과 화면 출력
    st.subheader(f"📊 {selected_month}월 {selected_day}일의 기온 분석 및 예측")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label=f"🔮 {future_year}년 예상 최고기온", value=f"{pred_max:.2f} °C")
    with col2:
        st.metric(label=f"🔮 {future_year}년 예상 최저기온", value=f"{pred_min:.2f} °C")
        
    # 데이터 병합 (그래프용)
    future_row = pd.DataFrame({
        '연도': [future_year],
        '최고기온(℃)': [pred_max],
        '최저기온(℃)': [pred_min]
    })
    plot_df = pd.concat([filtered_df, future_row], ignore_index=True)

    # 5. Plotly 그래프 그리기
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=filtered_df['연도'], y=filtered_df['최고기온(℃)'],
        mode='lines+markers', name='최고기온 (과거)',
        line=dict(color='hotpink', width=2),
        hovertemplate='<b>%{x}년 최고기온</b><br>%{y:.1f} °C<extra></extra>'
    ))

    fig.add_trace(go.Scatter(
        x=plot_df['연도'].iloc[-2:], y=plot_df['최고기온(℃)'].iloc[-2:],
        mode='lines+markers', name='최고기온 (예측)',
        line=dict(color='hotpink', width=2, dash='dash'),
        hovertemplate='<b>%{x}년 최고기온(예측)</b><br>%{y:.1f} °C<extra></extra>'
    ))

    fig.add_trace(go.Scatter(
        x=filtered_df['연도'], y=filtered_df['최저기온(℃)'],
        mode='lines+markers', name='최저기온 (과거)',
        line=dict(color='lightskyblue', width=2),
        hovertemplate='<b>%{x}년 최저기온</b><br>%{y:.1f} °C<extra></extra>'
    ))

    fig.add_trace(go.Scatter(
        x=plot_df['연도'].iloc[-2:], y=plot_df['최저기온(℃)'].iloc[-2:],
        mode='lines+markers', name='최저기온 (예측)',
        line=dict(color='lightskyblue', width=2, dash='dash'),
        hovertemplate='<b>%{x}년 최저기온(예측)</b><br>%{y:.1f} °C<extra></extra>'
    ))

    fig.update_layout(
        title=dict(text="날짜별 기온 분석", font=dict(size=20), x=0.5),
        xaxis_title="연도",
        yaxis_title="온도",
        hovermode="x unified",
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    st.plotly_chart(fig, use_container_width=True)
