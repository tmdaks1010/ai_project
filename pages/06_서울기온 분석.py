import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

# 1. 데이터 로드 및 전처리
@st.cache_data
def load_data():
    df = pd.read_csv('seoul.csv')
    df.columns = df.columns.str.strip()
    df['날짜'] = df['날짜'].astype(str).str.replace(r'\s+', '', regex=True)
    df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')
    df = df.dropna(subset=['날짜', '최고기온(℃)', '최저기온(℃)'])
    
    df['연도'] = df['날짜'].dt.year
    df['월'] = df['날짜'].dt.month
    df['일'] = df['날짜'].dt.day
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

# 앱 제목
st.title("📅 서울 기온 분석 및 미래 예측")

# 2. 사용자 입력 (사이드바)
st.sidebar.header("설정")
selected_month = st.sidebar.selectbox("월을 선택하세요", sorted(df['월'].unique()), index=9) # 기본값 10월
selected_day = st.sidebar.selectbox("일을 선택하세요", sorted(df[df['월'] == selected_month]['일'].unique()))

# 미래 예측 연도 선택
max_year_in_data = int(df['연도'].max())
future_year = st.sidebar.number_input(
    f"예측할 미래 연도를 입력하세요 (최대 데이터 연도: {max_year_in_data})", 
    min_value=max_year_in_data + 1, 
    max_value=2100, 
    value=2030
)

# 3. 데이터 필터링
filtered_df = df[(df['월'] == selected_month) & (df['일'] == selected_day)].sort_values('연to')

if filtered_df.empty:
    st.warning("선택한 날짜의 데이터가 존재하지 않습니다.")
else:
    # 4. 선형 회귀를 이용한 기온 예측
    X = filtered_df[['연도']].values
    y_max = filtered_df['최고기온(℃)'].values
    y_min = filtered_df['최저기온(℃)'].values
    
    # 모델 학습 및 미래 예측
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
        
    # 기존 데이터에 예측 데이터 임시 병합 (그래프 표시용)
    future_row = pd.DataFrame({
        '연도': [future_year],
        '최고기온(℃)': [pred_max],
        '최저기온(℃)': [pred_min]
    })
    plot_df = pd.concat([filtered_df, future_row], ignore_index=True)

    # 5. Plotly를 활용한 인터랙티브 그래프 그리기 (마우스 오버 툴팁)
    fig = go.Figure()

    # 과거 최고 기온 데이터
    fig.add_trace(go.Scatter(
        x=filtered_df['연도'], y=filtered_df['최고기온(℃)'],
        mode='lines+markers', name='최고기온 (과거)',
        line=dict(color='hotpink', width=2),
        hovertemplate='<b>%{x}년 최고기온</b><br>%{y:.1f} °C<extra></extra>'
    ))

    # 미래 예측 최고 기온 (점선으로 표시)
    fig.add_trace(go.Scatter(
        x=plot_df['연도'].iloc[-2:], y=plot_df['최고기온(℃)'].iloc[-2:],
        mode='lines+markers', name='최고기온 (예측)',
        line=dict(color='hotpink', width=2, dash='dash'),
        hovertemplate='<b>%{x}년 최고기온(예측)</b><br>%{y:.1f} °C<extra></extra>'
    ))

    # 과거 최저 기온 데이터
    fig.add_trace(go.Scatter(
        x=filtered_df['연도'], y=filtered_df['최저기온(℃)'],
        mode='lines+markers', name='최저기온 (과거)',
        line=dict(color='lightskyblue', width=2),
        hovertemplate='<b>%{x}년 최저기온</b><br>%{y:.1f} °C<extra></extra>'
    ))

    # 미래 예측 최저 기온 (점선으로 표시)
    fig.add_trace(go.Scatter(
        x=plot_df['연도'].iloc[-2:], y=plot_df['최저기온(℃)'].iloc[-2:],
        mode='lines+markers', name='최저기온 (예측)',
        line=dict(color='lightskyblue', width=2, dash='dash'),
        hovertemplate='<b>%{x}년 최저기온(예측)</b><br>%{y:.1f} °C<extra></extra>'
    ))

    # 레이아웃 설정 (요청 사항 반영)
    fig.update_layout(
        title=dict(text="날짜별 기온 분석", font=dict(size=20), x=0.5), # 제목 중앙 정렬
        xaxis_title="연도",
        yaxis_title="온도",
        hovermode="x unified", # 마우스를 올렸을 때 같은 연도의 최고/최저 기온을 한눈에 비교
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    # 스트림릿에 Plotly 차트 출력
    st.plotly_chart(fig, use_container_width=True)

