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

# 중복 영화명으로 인한 Plotly 트리맵 계층 생성 에러 방지
df_treemap = df.groupby(['genre', 'movieNm'], as_index=False)['total_audi'].sum()

fig2 = px.treemap(
    df_treemap,
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

# -------------------------------------------------------------------
# 네 번째 그래프: 개봉일 스크린수 vs 총 관객 수 (산점도)
# -------------------------------------------------------------------
st.subheader("4. 개봉일 스크린수와 총 관객 수의 관계")

fig4 = px.scatter(
    df,
    x='first_scrn',
    y='total_audi',
    color='genre',
    title='개봉일 스크린수 vs 총 관객 수',
    labels={
        'first_scrn': '개봉일 스크린수 (개)',
        'total_audi': '총 관객 수 (명)',
        'genre': '장르'
    },
    hover_name='movieNm',
    hover_data={'first_scrn': ':,', 'total_audi': ':,', 'genre': True}
)

fig4.update_traces(
    hovertemplate='<b>%{hovertext}</b><br>장르: %{customdata[2]}<br>개봉일 스크린수: %{x:,.0f}개<br>총 관객 수: %{y:,.0f}명'
)

st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")
st.write("개봉일 스크린수가 많을수록 대체로 총 관객 수가 증가하는 양의 상관관계를 보이며, 장르별 선호도나 입소문에 따른 흥행 차이도 함께 확인할 수 있습니다.")
st.markdown("---")

# -------------------------------------------------------------------
# 다섯 번째 그래프: 영화 10편 이상 장르의 총 관객 수 분포 (박스플롯)
# -------------------------------------------------------------------
st.subheader("5. 주요 장르별 총 관객 수 분포")

# 영화가 10편 이상인 장르 필터링
genre_counts_series = df['genre'].value_counts()
top_genres = genre_counts_series[genre_counts_series >= 10].index
df_filtered = df[df['genre'].isin(top_genres)]

fig5 = px.box(
    df_filtered,
    x='genre',
    y='total_audi',
    color='genre',
    title='영화 10편 이상 장르별 총 관객 수 분포 (박스플롯)',
    labels={
        'genre': '장르',
        'total_audi': '총 관객 수 (명)'
    },
    hover_name='movieNm',
    points='outliers'
)

fig5.update_traces(
    hovertemplate='<b>%{hovertext}</b><br>총 관객 수: %{y:,.0f}명'
)

st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")
st.write("주요 장르별 관객 수의 중앙값과 흥행 변동성(IQR)을 비교할 수 있으며, 박스 상단 밖의 이상치 점으로 각 장르의 기록적인 대흥행작을 확인할 수 있습니다.")
st.markdown("---")

# -------------------------------------------------------------------
# 여섯 번째 그래프: 개봉일 스크린수 vs 총 관객 수 (개봉 첫 주 관객 크기 버블 차트)
# -------------------------------------------------------------------
st.subheader("6. 개봉일 스크린수, 총 관객 수, 개봉 첫 주 관객 수의 관계 (버블 차트)")

fig6 = px.scatter(
    df,
    x='first_scrn',
    y='total_audi',
    size='first_week_audi',
    color='genre',
    size_max=40,
    title='개봉일 스크린수 vs 총 관객 수 (버블 크기: 개봉 첫 주 관객 수)',
    labels={
        'first_scrn': '개봉일 스크린수 (개)',
        'total_audi': '총 관객 수 (명)',
        'genre': '장르',
        'first_week_audi': '개봉 첫 주 관객 수 (명)'
    },
    hover_name='movieNm',
    hover_data={'first_scrn': ':,', 'total_audi': ':,', 'first_week_audi': ':,', 'genre': True}
)

fig6.update_traces(
    hovertemplate='<b>%{hovertext}</b><br>장르: %{customdata[3]}<br>개봉일 스크린수: %{x:,.0f}개<br>총 관객 수: %{y:,.0f}명<br>개봉 첫 주 관객 수: %{customdata[2]:,.0f}명'
)

st.plotly_chart(fig6, use_container_width=True)

st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")
st.write("개봉일 스크린수와 최종 관객 수뿐만 아니라 버블 크기를 통해 초반 흥행 동력(개봉 첫 주 관객 수)이 최종 성적에 미치는 영향력을 3차원적(X, Y, 크기)으로 분석할 수 있습니다.")
st.markdown("---")

# -------------------------------------------------------------------
# 일곱 번째 그래프: 제작 국가별 장르 분포 (선버스트 차트)
# -------------------------------------------------------------------
st.subheader("7. 제작 국가 및 장르별 영화 편수 (선버스트 차트)")

df_sunburst = df.groupby(['nation', 'genre'], as_index=False).size()
df_sunburst.columns = ['nation', 'genre', 'movie_count']

fig7 = px.sunburst(
    df_sunburst,
    path=['nation', 'genre'],
    values='movie_count',
    title='제작 국가 > 장르별 영화 편수 분포'
)

fig7.update_traces(
    hovertemplate='<b>%{label}</b><br>영화 수: %{value}편<br>비율: %{percentParent:.1%}'
)

st.plotly_chart(fig7, use_container_width=True)

st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")
st.write("제작 국가별 영화 출시 규모와 각 국가 내에서 주를 이루는 대표 장르 구성 비율을 원형 계층 구조로 명확하게 비교할 수 있습니다.")
st.markdown("---")

# -------------------------------------------------------------------
# 여덟 번째 그래프: 나만의 질문 (산점도)
# -------------------------------------------------------------------
st.subheader("8. 개봉일 상영횟수가 많은 영화는 총 관객 수도 많은가?")

fig8 = px.scatter(
    df,
    x='first_show',
    y='total_audi',
    color='genre',
    title='개봉일 상영횟수 vs 총 관객 수',
    labels={
        'first_show': '개봉일 상영횟수 (회)',
        'total_audi': '총 관객 수 (명)',
        'genre': '장르'
    },
    hover_name='movieNm',
    hover_data={'first_show': ':,', 'total_audi': ':,', 'genre': True}
)

fig8.update_traces(
    hovertemplate='<b>%{hovertext}</b><br>장르: %{customdata[2]}<br>개봉일 상영횟수: %{x:,.0f}회<br>총 관객 수: %{y:,.0f}명'
)

st.plotly_chart(fig8, use_container_width=True)

st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")
st.write("개봉 첫날 상영횟수가 확보될수록 최종 관객 수가 증가하는 뚜렷한 뚜렷한 양의 상관관계를 보여주며, 초반 상영 기회 선점이 영화 흥행의 중요한 요소임을 확인할 수 있습니다.")
st.markdown("---")
