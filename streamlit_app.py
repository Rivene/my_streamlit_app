# # # main.py
# # import streamlit as st

# # st.text('hello Streamlit!')

# # youtube_trend_conversation.py
# import streamlit as st
# import requests
# from wordcloud import WordCloud
# import matplotlib.pyplot as plt
# import pandas as pd
# import re
# from collections import Counter
# # :열쇠와_잠긴_자물쇠: 유튜브 API 키 (← 본인의 키로 변경)
# API_KEY = "AIzaSyCHDXTtIcfegyjBplVooLoeBud1dkchfGA"
# # :앞쪽_화살표: 채널 ID 입력 받기
# st.set_page_config(page_title="YouTube 트렌드 & 대화 주제 분석기", page_icon=":클래퍼:", layout="wide")
# st.title("🎬: 유튜브 인기 트렌드 분석 & 대화 주제 추천")
# st.write("유튜브 채널의 인기 영상을 분석해 키워드와 대화 주제를 알려드립니다.")
# channel_id = st.text_input("📺: 유튜브 채널 ID", help="예: UC_x5XG1OV2P6uZZ5FSM9Ttw")
# video_count = st.slider("🎞: 분석할 영상 개수", 5, 20, 10)
# # :빗자루: 텍스트 정제

# def clean_text(text):
#     text = re.sub(r"[^\uAC00-\uD7A3a-zA-Z0-9\s]", "", text)
#     return text.lower()

# # :대문자_abcd: 키워드 추출 (한글 2글자 이상만)
# def extract_keywords(texts, top_n=30):
#     all_words = []
#     for text in texts:
#         # 한글 2글자 이상만 추출
#         words = re.findall(r'[가-힣]{2,}', clean_text(text))
#         all_words.extend(words)
#     return Counter(all_words).most_common(top_n)

# # :구름: 워드클라우드 생성 (한글 폰트 지정)
# def create_wordcloud(freq_dict):
#     wc = WordCloud(font_path="nanumgothic.ttf", background_color="white", width=800, height=400)
#     wc.generate_from_frequencies(freq_dict)
#     return wc
# # :시계_반대_방향_화살표: 채널 → 업로드 리스트 ID
# def get_upload_playlist_id(channel_id):
#     url = f"https://www.googleapis.com/youtube/v3/channels?part=contentDetails&id={channel_id}&key={API_KEY}"
#     res = requests.get(url).json()
#     try:
#         return res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
#     except:
#         return None
# # :받은_편지함_트레이: 업로드 리스트 → 영상 정보
# def get_videos_from_playlist(playlist_id, max_results):
#     url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={playlist_id}&maxResults={max_results}&key={API_KEY}"
#     res = requests.get(url).json()
#     videos = []
#     for item in res.get("items", []):
#         snippet = item["snippet"]
#         videos.append({
#             "video_id": snippet["resourceId"]["videoId"],
#             "title": snippet["title"],
#             "description": snippet["description"],
#             "url": f"https://www.youtube.com/watch?v={snippet['resourceId']['videoId']}"
#         })
#     return videos
# # :말풍선: 대화 주제 생성
# def generate_conversation_topics(keywords):
#     prompts = []
#     for keyword, _ in keywords[:10]:
#         if "게임" in keyword:
#             prompts.append(f"🎮: 요즘 '{keyword}' 관련 콘텐츠 많이 보이던데, 즐겨 하세요?")
#         elif "여행" in keyword or "휴가" in keyword:
#             prompts.append(f"✈️: '{keyword}' 관련 영상이 인기인데, 최근에 어디 다녀오셨어요?")
#         elif "음악" in keyword or "노래" in keyword:
#             prompts.append(f"🎵: '{keyword}' 영상이 많은데, 어떤 음악 좋아하세요?")
#         elif "다이어트" in keyword or "헬스" in keyword:
#             prompts.append(f"💪: '{keyword}' 관련한 영상이 많네요. 건강관리 어떻게 하세요?")
#         elif "드라마" in keyword or "영화" in keyword:
#             prompts.append(f"🎬: '{keyword}' 영상이 핫한데, 혹시 최근 본 거 있으세요?")
#         else:
#             prompts.append(f"🗣️: '{keyword}' 요즘 핫한 주제 같아요. 어떻게 생각하세요?")
#     return prompts[:5]
# # :로켓: 분석 시작
# if st.button(": 트렌드 분석 시작"):
#     if not channel_id:
#         st.error("채널 ID를 입력해주세요.")
#     else:
#         with st.spinner("YouTube 채널 정보 불러오는 중..."):
#             playlist_id = get_upload_playlist_id(channel_id)
#         if not playlist_id:
#             st.error("채널 ID가 잘못되었거나 영상이 없습니다.")
#         else:
#             with st.spinner("인기 영상 분석 중..."):
#                 videos = get_videos_from_playlist(playlist_id, video_count)
#             if not videos:
#                 st.warning("영상을 가져올 수 없습니다.")
#             else:
#                 titles = [v["title"] for v in videos]
#                 descriptions = [v["description"] for v in videos]
#                 texts = titles + descriptions
#                 keywords = extract_keywords(texts)
#                 keyword_df = pd.DataFrame(keywords)
#                 keyword_df.columns = ["키워드", "빈도"]
#                 # :구름: 워드클라우드
#                 st.subheader("☁️: 워드클라우드")
#                 fig, ax = plt.subplots(figsize=(10, 5))
#                 wc = create_wordcloud(dict(keywords))
#                 ax.imshow(wc, interpolation="bilinear")
#                 ax.axis("off")
#                 st.pyplot(fig)
#                 # :막대_차트: 키워드 바 차트
#                 st.subheader("📊: 키워드 빈도수")
#                 st.bar_chart(keyword_df.set_index("키워드"))
#                 # :말풍선: 대화 주제 추천
#                 st.subheader("💬: 추천 대화 주제")
#                 topics = generate_conversation_topics(keywords)
#                 for i, t in enumerate(topics, 1):
#                     st.write(f"**{i}.** {t}")
#                 # :필름_프레임: 영상 목록
#                 st.subheader("🎥: 인기 영상 목록")
#                 for v in videos:
#                     st.markdown(f"- [{v['title']}]({v['url']})")
#                 # :받은_편지함_트레이: 다운로드
#                 st.subheader("📥: 결과 다운로드")
#                 csv = keyword_df.to_csv(index=False)
#                 st.download_button("📄:글씨가_쓰여진_페이지: 키워드 CSV 다운로드", csv, "youtube_trend_keywords.csv", mime="text/csv")
#                 txt = "\n".join(topics)
#                 st.download_button("💬: 대화 주제 TXT 다운로드", txt, "youtube_conversation_topics.txt", mime="text/plain")


import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 시각화 라이브러리 
# py -m pip install plotly 

# 페이지 설정
st.set_page_config(
    page_title="판매 데이터 분석 대시보드",
    page_icon="📊",
    layout="wide"
)

@st.cache_data
def generate_sample_data():
    """샘플 판매 데이터 생성"""
    np.random.seed(42)
    
    # 날짜 범위
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    dates = pd.date_range(start_date, end_date, freq='D')
    
    # 제품 카테고리
    categories = ['전자제품', '의류', '가구', '도서', '스포츠']
    regions = ['서울', '부산', '대구', '인천', '광주']
    
    data = []
    for date in dates:
        for category in categories:
            for region in regions:
                sales = np.random.normal(1000, 300)
                quantity = np.random.poisson(50)
                data.append({
                    'date': date,
                    'category': category,
                    'region': region,
                    'sales': max(0, sales),
                    'quantity': quantity
                })
    
    return pd.DataFrame(data)

def main():
    st.title("📊 판매 데이터 분석 대시보드")
    
    # 사이드바
    st.sidebar.title("필터 옵션")
    
    # 데이터 로드
    df = generate_sample_data()
    
    # 날짜 필터
    date_range = st.sidebar.date_input(
        "기간 선택",
        value=[df['date'].min(), df['date'].max()],
        min_value=df['date'].min(),
        max_value=df['date'].max()
    )
    
    # 카테고리 필터
    categories = st.sidebar.multiselect(
        "카테고리 선택",
        options=df['category'].unique(),
        default=df['category'].unique()
    )
    
    # 지역 필터
    regions = st.sidebar.multiselect(
        "지역 선택",
        options=df['region'].unique(),
        default=df['region'].unique()
    )
    
    # 데이터 필터링
    if len(date_range) == 2:
        filtered_df = df[
            (df['date'] >= pd.Timestamp(date_range[0])) &
            (df['date'] <= pd.Timestamp(date_range[1])) &
            (df['category'].isin(categories)) &
            (df['region'].isin(regions))
        ]
    else:
        filtered_df = df[
            (df['category'].isin(categories)) &
            (df['region'].isin(regions))
        ]
    
    # 주요 지표
    st.subheader("📈 주요 지표")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_sales = filtered_df['sales'].sum()
        st.metric("총 매출", f"₩{total_sales:,.0f}")
    
    with col2:
        total_quantity = filtered_df['quantity'].sum()
        st.metric("총 판매량", f"{total_quantity:,}")
    
    with col3:
        avg_sales = filtered_df['sales'].mean()
        st.metric("평균 일일 매출", f"₩{avg_sales:,.0f}")
    
    with col4:
        unique_days = filtered_df['date'].nunique()
        st.metric("분석 기간", f"{unique_days}일")
    
    # 차트 섹션
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 카테고리별 매출")
        category_sales = filtered_df.groupby('category')['sales'].sum().reset_index()
        fig_pie = px.pie(category_sales, values='sales', names='category', 
                        title="카테고리별 매출 비율")
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.subheader("🌍 지역별 매출")
        region_sales = filtered_df.groupby('region')['sales'].sum().reset_index()
        fig_bar = px.bar(region_sales, x='region', y='sales', 
                        title="지역별 총 매출")
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # 시계열 차트
    st.subheader("📈 시간별 매출 추이")
    
    daily_sales = filtered_df.groupby('date')['sales'].sum().reset_index()
    fig_line = px.line(daily_sales, x='date', y='sales', 
                      title="일별 매출 추이")
    st.plotly_chart(fig_line, use_container_width=True)
    
    # 상세 데이터 테이블
    with st.expander("📋 상세 데이터 보기"):
        st.dataframe(filtered_df.sort_values('date', ascending=False), 
                    use_container_width=True)
        
        # 데이터 다운로드
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="필터링된 데이터 다운로드",
            data=csv,
            file_name=f'sales_data_{datetime.now().strftime("%Y%m%d")}.csv',
            mime='text/csv'
        )
    
    # 분석 리포트
    st.subheader("📝 분석 리포트")
    
    # 최고 실적 카테고리
    best_category = category_sales.loc[category_sales['sales'].idxmax(), 'category']
    best_region = region_sales.loc[region_sales['sales'].idxmax(), 'region']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"**최고 실적 카테고리:** {best_category}")
        st.info(f"**최고 실적 지역:** {best_region}")
    
    with col2:
        peak_day = daily_sales.loc[daily_sales['sales'].idxmax(), 'date']
        st.info(f"**최고 매출일:** {peak_day.strftime('%Y-%m-%d')}")
        st.info(f"**분석 기간 평균 일일 매출:** ₩{daily_sales['sales'].mean():,.0f}")

if __name__ == "__main__":
    main()