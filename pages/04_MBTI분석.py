import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. 페이지 설정
st.set_page_config(page_title="세계 MBTI 분포 시각화", layout="centered")

st.title("📊 국가별 MBTI 분포 분석기")
st.markdown("국가를 선택하면 해당 국가의 MBTI 16가지 유형 비율을 인터랙티브한 그래프로 보여줍니다.")

# 2. 데이터 로드
@st.cache_data
def load_data():
    # 업로드한 파일명과 동일하게 설정
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

try:
    df = load_data()

    # 3. 사이드바 또는 메인 화면에서 국가 선택
    country_list = df['Country'].unique()
    selected_country = st.selectbox("🧐 분석할 국가를 선택하세요:", country_list)

    # 4. 선택한 국가의 데이터 추출 및 정렬
    country_data = df[df['Country'] == selected_country].iloc[0, 1:]
    
    # 가독성을 위해 퍼센트(%) 단위로 변환하고 내림차순 정렬
    country_df = pd.DataFrame({
        'MBTI': country_data.index,
        'Percentage': country_data.values * 100
    }).sort_values(by='Percentage', ascending=False).reset_index(drop=True)

    # 5. 조건별 색상 지정 (1등: 파란색, 나머지: 빨간색 그라데이션)
    # 1등을 제외한 나머지 데이터의 개수
    num_remains = len(country_df) - 1
    
    # 1등은 선명한 파란색(Deep Sky Blue)
    colors = ['#1f77b4'] 
    
    # 나머지는 점진적으로 흐려지는 빨간색 그라데이션 컬러칩 (Plotly 스타일)
    # 2등(가장 진한 빨강) ~ 16등(연한 핑크빛 빨강)
    for i in range(num_remains):
        # 0에서 1 사이의 비율 계산 (뒤로 갈수록 연해짐)
        alpha = 0.3 + (0.7 * (1 - (i / (num_remains - 1 if num_remains > 1 else 1))))
        colors.append(f'rgba(214, 39, 40, {alpha})')

    # 6. 플로틀리(Plotly) 막대그래프 생성
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=country_df['MBTI'],
        y=country_df['Percentage'],
        marker_color=colors,
        text=country_df['Percentage'].round(2).astype(str) + '%', # 막대 위에 텍스트 표시
        textposition='auto',
        hovertemplate='<b>MBTI</b>: %{x}<br><b>비율</b>: %{y:.2f}%<extra></extra>'
    ))

    # 그래프 레이아웃 깔끔하게 다듬기
    fig.update_layout(
        title=f"🇲🇳 🇺🇸 🇰🇷 {selected_country}의 MBTI 유형별 비율 (1위 강조)",
        xaxis_title="MBTI 유형",
        yaxis_title="비율 (%)",
        yaxis=dict(ticksuffix="%"),
        template="plotly_white",
        margin=dict(l=20, r=20, t=60, b=20),
        height=500
    )

    # 7. 스트림릿에 그래프 출력
    st.plotly_chart(fig, use_container_width=True)

    # 8. 소소한 데이터 요약 텍스트
    st.subheader(f"💡 {selected_country} 핵심 요약")
    top_mbti = country_df.iloc[0]['MBTI']
    top_pct = country_df.iloc[0]['Percentage']
    lowest_mbti = country_df.iloc[-1]['MBTI']
    lowest_pct = country_df.iloc[-1]['Percentage']
    
    st.write(f"- {selected_country}에서 가장 많은 유형은 **{top_mbti}** ({top_pct:.2f}%) 입니다.")
    st.write(f"- 가장 적은 유형은 **{lowest_mbti}** ({lowest_pct:.2f}%) 입니다.")

except FileNotFoundError:
    st.error("❌ `countriesMBTI_16types.csv` 파일을 찾을 수 없습니다. 코드와 같은 폴더에 넣어주세요!")
