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

genre_counts = df['genre'].value_counts().reset_index()
genre_counts.columns = ['장르', '영화 수']

fig1 = px.pie(
    genre_counts,
    names='장르',
    values='영화 수',
    hole=0.4,
    title='장르별 영화 편수 및 비중'
)

fig1.update_traces(
    textinfo='percent+label',
    hovertemplate='<b>장르:</b> %{label}<br><b>영화 수:</b> %{value}편<br><b>비율:</b> %{percent}'
)

st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")
st.write("박스오피스 상위권 영화 중 어떤 장르가 가장 큰 비중을 차지하는지, 장르별 편수 분포를 한눈에 확인할 수 있습니다.")
st.markdown("---")

# -------------------------------------------------------------------
# 두 번째 그래프: 장르 및 영화별 총 관객 수 (트리맵)
# -------------------------------------------------------------------
st.subheader("2. 장르별 영화 및 총 관객 수")

fig2 = px.treemap(
    df,
    path=[px.Constant("전체"), 'genre', 'movieNm'],
    values='total_audi',
    title='장르 및 영화별 총 관객 수 분포'
)

fig2.update_traces(
    hovertemplate='<b>%{label}</b><br>총 관객 수: %{value:,.0f}명'
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")
st.write("각 장르 내에서 어떤 영화가 흥행(총 관객 수)을 이끌었는지와 전체 관객 수 대비 해당 영화 및 장르의 상위 점유 규모를 시각적으로 한눈에 비교할 수 있습니다.")
st.markdown("---")

# -------------------------------------------------------------------
# 세 번째 그래프: 총 관객 수 분포 (히스토그램)
# -------------------------------------------------------------------
st.subheader("3. 총 관객 수 분포")

fig3 = px.histogram(
    df,
    x='total_audi',
    nbins=20,
    title='영화별 총 관객 수 분포 (히스토그램)',
    labels={'total_audi': '총 관객 수 (명)', 'count': '영화 수'},
    hover_data=['movieNm']
)

fig3.update_traces(
    hovertemplate='<b>관객 수 구간:</b> %{x}명<br><b>영화 수:</b> %{y}편'
)

st.plotly_chart(fig3, use_container_width=True)

# 최다 관객 영화 계산
top_movie_row = df.loc[df['total_audi'].idxmax()]
top_movie_name = top_movie_row['movieNm']
top_movie_audi = top_movie_row['total_audi']

st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")
st.write(
    f"대부분의 영화가 **하위 관객 수 구간(약 100만~300만 명대)**에 밀집해 있는 오른꼬리가 긴 분포 형태를 보이며, "
    f"가장 관객 수가 많은 영화는 **{top_movie_name}** ({top_movie_audi:,.0f}명)입니다."
)
st.markdown("---")
