import streamlit as st
import folium
from streamlit_folium import st_folium

# 1. 페이지 설정
st.set_page_config(
    page_title="Seoul Top 10 Tourist Attractions",
    page_icon="📍",
    layout="wide"
)

# 2. 타이틀 및 소개
st.title("🎬 외국인이 선호하는 서울 주요 관광지 TOP 10")
st.markdown("스트림릿과 폴리움(Folium)을 활용하여 외국인 관광객들이 가장 사랑하는 서울의 명소들을 지도에 표시했습니다.")

# 3. 데이터 정의 (명소 이름, 위도, 경도, 설명)
seoul_attractions = [
    {"name": "경복궁", "lat": 37.5796, "lng": 126.9770, "desc": "조선 왕조의 정궁, 한복 체험과 수문장 교대식이 인기"},
    {"name": "N서울타워", "lat": 37.5512, "lng": 126.9882, "desc": "남산 정상에서 서울 시내를 한눈에 조망하는 랜드마크"},
    {"name": "명동 쇼핑거리", "lat": 37.5630, "lng": 126.9841, "desc": "K-뷰티, 패션 브랜드 및 다채로운 길거리 음식의 천국"},
    {"name": "북촌한옥마을", "lat": 37.5829, "lng": 126.9835, "desc": "600년 역사의 전통 한옥이 잘 보존된 도심 속 살아있는 박물관"},
    {"name": "인사동 쌈지길", "lat": 37.5743, "lng": 126.9847, "desc": "한국의 전통 공예품, 갤러리, 전통 찻집이 모여있는 문화의 거리"},
    {"name": "홍대 걷고싶은거리", "lat": 37.5562, "lng": 126.9227, "desc": "젊은 에너지와 버스킹 공연, 독특한 인디 문화의 중심지"},
    {"name": "동대문디자인플라자 (DDP)", "lat": 37.5665, "lng": 127.0092, "desc": "자하 하디드가 설계한 세계 최대 규모의 3차원 비정형 건축물"},
    {"name": "이태원 관광특구", "lat": 37.5345, "lng": 126.9942, "desc": "세계 각국의 다양한 요리와 나이트라이프를 즐길 수 있는 이색적인 공간"},
    {"name": "광장시장", "lat": 37.5701, "lng": 127.0010, "desc": "빈대떡, 마약김밥 등 한국의 넷플릭스 출연 길거리 음식을 맛보는 전통시장"},
    {"name": "여의도 한강공원", "lat": 37.5284, "lng": 126.9331, "desc": "‘한강 라면’과 배달 음식을 즐기며 여유를 만끽하는 수변 공원"}
]

# 4. 화면 레이아웃 분할 (좌측: 설명 테이블, 우측: 지도)
col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("📌 관광지 목록 및 특징")
    # 깔끔한 테이블 형식으로 데이터 출력
    for idx, place in enumerate(seoul_attractions, 1):
        st.markdown(f"**{idx}. {place['name']}**")
        st.caption(place['desc'])
        st.write("---")

with col2:
    st.subheader("🗺️ 서울 관광 지도")
    
    # 서울 중심부를 기준으로 Folium 지도 초기화
    m = folium.Map(location=[37.5665, 126.9780], zoom_start=12, tiles="OpenStreetMap")
    
    # 마커 추가
    for idx, place in enumerate(seoul_attractions, 1):
        popup_content = f"<b>{idx}. {place['name']}</b><br><span style='font-size:12px;'>{place['desc']}</span>"
        
        folium.Marker(
            location=[place['lat'], place['lng']],
            popup=folium.Popup(popup_content, max_width=300),
            tooltip=f"{idx}. {place['name']}",
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(m)
    
    # 스트림릿 웹 화면에 지도 렌더링
    st_folium(m, width="100%", height=600, returned_objects=[])
