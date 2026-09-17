import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    layout="wide"
)

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")

# 데이터 불러오기 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)
    
    # 장르: 세로막대 기호(|)로 분리되어 있는 경우 첫 번째 장르만 추출
    df['genre'] = df['genre'].astype(str).str.split('|').str[0]
    
    return df

df = load_data()

# -------------------------------------------------------------------
# 첫 번째 그래프: 장르별 영화 편수 (도넛 그래프)
# -------------------------------------------------------------------
st.subheader("1. 장르별 영화 편수")

# 장르별 영화 편수 집계
genre_counts = df['genre'].value_counts().reset_index()
genre_counts.columns = ['장르', '영화 수']

# 플롯리 도넛 그래프 생성
fig1 = px.pie(
    genre_counts,
    names='장르',
    values='영화 수',
    hole=0.4,
    title='장르별 영화 편수 및 비중'
)

# 마우스오버 시 편수와 비율이 보이도록 설정
fig1.update_traces(
    textinfo='percent+label',
    hovertemplate='<b>장르:</b> %{label}<br><b>영화 수:</b> %{value}편<br><b>비율:</b> %{percent}'
)

st.plotly_chart(fig1, use_container_width=True)

# '이 그래프로 알 수 있는 것' 섹션
st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")
st.write("박스오피스 상위권 영화 중 어떤 장르가 가장 큰 비중을 차지하는지, 장르별 편수 분포를 한눈에 확인할 수 있습니다.")
st.markdown("---")

# -------------------------------------------------------------------
# 두 번째 그래프: 장르 및 영화별 총 관객 수 (트리맵)
# -------------------------------------------------------------------
st.subheader("2. 장르별 영화 및 총 관객 수")

# 플롯리 트리맵 생성 (장르 -> 영화명 계층 구조)
fig2 = px.treemap(
    df,
    path=[px.Constant("전체"), 'genre', 'movieNm'],
    values='total_audi',
    title='장르 및 영화별 총 관객 수 분포'
)

# 마우스오버 시 영화명과 총 관객 수가 정확히 보이도록 툴팁 설정
fig2.update_traces(
    hovertemplate='<b>%{label}</b><br>총 관객 수: %{value:,.0f}명'
)

st.plotly_chart(fig2, use_container_width=True)

# '이 그래프로 알 수 있는 것' 섹션
st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")
st.write("각 장르 내에서 어떤 영화가 흥행(총 관객 수)을 이끌었는지와 전체 관객 수 대비 해당 영화 및 장르의 상위 점유 규모를 시각적으로 한눈에 비교할 수 있습니다.")
st.markdown("---")
