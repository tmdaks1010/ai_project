import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. 페이지 설정
st.set_page_config(page_title="세계 MBTI 데이터 분석기", layout="centered")

st.title("📊 전 세계 MBTI 데이터 분석기")
st.markdown("원하는 탭을 선택하여 국가별 분포 또는 MBTI별 상위 국가를 확인해보세요.")

# 2. 데이터 로드
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

try:
    df = load_data()
    mbti_columns = list(df.columns[1:]) # MBTI 16개 컬럼명 추출

    # 스트림릿 탭 기능으로 두 가지 기능 분리
    tab1, tab2 = st.tabs(["🗺️ 국가별 MBTI 보기", "🏆 MBTI별 높은 국가 TOP 10"])

    # ---------------------------------------------------------
    # TAB 1: 기존 기능 (국가 선택 시 해당 국가의 MBTI 비율)
    # ---------------------------------------------------------
    with tab1:
        country_list = df['Country'].unique()
        selected_country = st.selectbox("🧐 분석할 국가를 선택하세요:", country_list, key="tab1_select")

        country_data = df[df['Country'] == selected_country].iloc[0, 1:]
        country_df = pd.DataFrame({
            'MBTI': country_data.index,
            'Percentage': country_data.values * 100
        }).sort_values(by='Percentage', ascending=False).reset_index(drop=True)

        # 색상 세팅 (1등 파랑, 나머지 빨강 그라데이션)
        colors_tab1 = ['#1f77b4']
        num_remains_t1 = len(country_df) - 1
        for i in range(num_remains_t1):
            alpha = 0.3 + (0.7 * (1 - (i / (num_remains_t1 - 1 if num_remains_t1 > 1 else 1))))
            colors_tab1.append(f'rgba(214, 39, 40, {alpha})')

        fig1 = go.Figure(go.Bar(
            x=country_df['MBTI'],
            y=country_df['Percentage'],
            marker_color=colors_tab1,
            text=country_df['Percentage'].round(2).astype(str) + '%',
            textposition='auto',
            hovertemplate='<b>MBTI</b>: %{x}<br><b>비율</b>: %{y:.2f}%<extra></extra>'
        ))
        fig1.update_layout(
            title=f"{selected_country}의 MBTI 유형별 비율",
            xaxis_title="MBTI 유형", yaxis_title="비율 (%)", yaxis=dict(ticksuffix="%"),
            template="plotly_white", height=450
        )
        st.plotly_chart(fig1, use_container_width=True)

    # ---------------------------------------------------------
    # TAB 2: 신규 기능 (MBTI 선택 시 비율 높은 나라 TOP 10)
    # ---------------------------------------------------------
    with tab2:
        selected_mbti = st.selectbox("✨ 궁금한 MBTI 유형을 선택하세요:", mbti_columns, key="tab2_select")

        # 선택한 MBTI 컬럼을 기준으로 내림차순 정렬 후 상위 10개국 추출
        top10_df = df[['Country', selected_mbti]].sort_values(by=selected_mbti, ascending=False).head(10).reset_index(drop=True)
        # 퍼센트 단위 변환
        top10_df['Percentage'] = top10_df[selected_mbti] * 100

        # 색상 세팅 (1등 파랑, 나머지 빨강 그라데이션)
        colors_tab2 = ['#1f77b4']  # 1등은 파란색
        num_remains_t2 = len(top10_df) - 1 # 9개
        for i in range(num_remains_t2):
            # 순위가 내려갈수록(2등->10등) 빨간색이 점점 연해짐
            alpha = 0.3 + (0.7 * (1 - (i / (num_remains_t2 - 1 if num_remains_t2 > 1 else 1))))
            colors_tab2.append(f'rgba(214, 39, 40, {alpha})')

        # 플로틀리 막대그래프 그리기
        fig2 = go.Figure(go.Bar(
            x=top10_df['Country'],
            y=top10_df['Percentage'],
            marker_color=colors_tab2,
            text=top10_df['Percentage'].round(2).astype(str) + '%',
            textposition='auto',
            hovertemplate='<b>국가명</b>: %{x}<br><b>비율</b>: %{y:.2f}%<extra></extra>'
        ))
        fig2.update_layout(
            title=f"🌍 {selected_mbti} 비율이 가장 높은 국가 TOP 10",
            xaxis_title="국가",
            yaxis_title="해당 MBTI 비율 (%)",
            yaxis=dict(ticksuffix="%"),
            template="plotly_white",
            height=450
        )
        st.plotly_chart(fig2, use_container_width=True)
        
        # 순위 요약 가이드
        st.subheader(f"👑 {selected_mbti} 최고 존엄국")
        st.write(f"전 세계에서 **{selected_mbti}** 성향이 가장 짙은 나라는 **{top10_df.iloc[0]['Country']}** 👑 ({top10_df.iloc[0]['Percentage']:.2f}%) 입니다.")

except FileNotFoundError:
    st.error("❌ `countriesMBTI_16types.csv` 파일을 찾을 수 없습니다. 코드와 같은 폴더에 넣어주세요!")
