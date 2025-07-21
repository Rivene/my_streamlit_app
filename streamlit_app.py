# # main.py
# import streamlit as st

# st.text('hello Streamlit!')

# youtube_trend_conversation.py
import streamlit as st
import requests
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import re
from collections import Counter
# :열쇠와_잠긴_자물쇠: 유튜브 API 키 (← 본인의 키로 변경)
API_KEY = "AIzaSyCHDXTtIcfegyjBplVooLoeBud1dkchfGA"
# :앞쪽_화살표: 채널 ID 입력 받기
st.set_page_config(page_title="YouTube 트렌드 & 대화 주제 분석기", page_icon=":클래퍼:", layout="wide")
st.title("🎬: 유튜브 인기 트렌드 분석 & 대화 주제 추천")
st.write("유튜브 채널의 인기 영상을 분석해 키워드와 대화 주제를 알려드립니다.")
channel_id = st.text_input("📺: 유튜브 채널 ID", help="예: UC_x5XG1OV2P6uZZ5FSM9Ttw")
video_count = st.slider("🎞: 분석할 영상 개수", 5, 20, 10)
# :빗자루: 텍스트 정제

def clean_text(text):
    text = re.sub(r"[^\uAC00-\uD7A3a-zA-Z0-9\s]", "", text)
    return text.lower()

# :대문자_abcd: 키워드 추출 (한글 2글자 이상만)
def extract_keywords(texts, top_n=30):
    all_words = []
    for text in texts:
        # 한글 2글자 이상만 추출
        words = re.findall(r'[가-힣]{2,}', clean_text(text))
        all_words.extend(words)
    return Counter(all_words).most_common(top_n)

# :구름: 워드클라우드 생성 (한글 폰트 지정)
def create_wordcloud(freq_dict):
    wc = WordCloud(font_path="nanumgothic.ttf", background_color="white", width=800, height=400)
    wc.generate_from_frequencies(freq_dict)
    return wc
# :시계_반대_방향_화살표: 채널 → 업로드 리스트 ID
def get_upload_playlist_id(channel_id):
    url = f"https://www.googleapis.com/youtube/v3/channels?part=contentDetails&id={channel_id}&key={API_KEY}"
    res = requests.get(url).json()
    try:
        return res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    except:
        return None
# :받은_편지함_트레이: 업로드 리스트 → 영상 정보
def get_videos_from_playlist(playlist_id, max_results):
    url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={playlist_id}&maxResults={max_results}&key={API_KEY}"
    res = requests.get(url).json()
    videos = []
    for item in res.get("items", []):
        snippet = item["snippet"]
        videos.append({
            "video_id": snippet["resourceId"]["videoId"],
            "title": snippet["title"],
            "description": snippet["description"],
            "url": f"https://www.youtube.com/watch?v={snippet['resourceId']['videoId']}"
        })
    return videos
# :말풍선: 대화 주제 생성
def generate_conversation_topics(keywords):
    prompts = []
    for keyword, _ in keywords[:10]:
        if "게임" in keyword:
            prompts.append(f"🎮: 요즘 '{keyword}' 관련 콘텐츠 많이 보이던데, 즐겨 하세요?")
        elif "여행" in keyword or "휴가" in keyword:
            prompts.append(f"✈️: '{keyword}' 관련 영상이 인기인데, 최근에 어디 다녀오셨어요?")
        elif "음악" in keyword or "노래" in keyword:
            prompts.append(f"🎵: '{keyword}' 영상이 많은데, 어떤 음악 좋아하세요?")
        elif "다이어트" in keyword or "헬스" in keyword:
            prompts.append(f"💪: '{keyword}' 관련한 영상이 많네요. 건강관리 어떻게 하세요?")
        elif "드라마" in keyword or "영화" in keyword:
            prompts.append(f"🎬: '{keyword}' 영상이 핫한데, 혹시 최근 본 거 있으세요?")
        else:
            prompts.append(f"🗣️: '{keyword}' 요즘 핫한 주제 같아요. 어떻게 생각하세요?")
    return prompts[:5]
# :로켓: 분석 시작
if st.button(": 트렌드 분석 시작"):
    if not channel_id:
        st.error("채널 ID를 입력해주세요.")
    else:
        with st.spinner("YouTube 채널 정보 불러오는 중..."):
            playlist_id = get_upload_playlist_id(channel_id)
        if not playlist_id:
            st.error("채널 ID가 잘못되었거나 영상이 없습니다.")
        else:
            with st.spinner("인기 영상 분석 중..."):
                videos = get_videos_from_playlist(playlist_id, video_count)
            if not videos:
                st.warning("영상을 가져올 수 없습니다.")
            else:
                titles = [v["title"] for v in videos]
                descriptions = [v["description"] for v in videos]
                texts = titles + descriptions
                keywords = extract_keywords(texts)
                keyword_df = pd.DataFrame(keywords)
                keyword_df.columns = ["키워드", "빈도"]
                # :구름: 워드클라우드
                st.subheader("☁️: 워드클라우드")
                fig, ax = plt.subplots(figsize=(10, 5))
                wc = create_wordcloud(dict(keywords))
                ax.imshow(wc, interpolation="bilinear")
                ax.axis("off")
                st.pyplot(fig)
                # :막대_차트: 키워드 바 차트
                st.subheader("📊: 키워드 빈도수")
                st.bar_chart(keyword_df.set_index("키워드"))
                # :말풍선: 대화 주제 추천
                st.subheader("💬: 추천 대화 주제")
                topics = generate_conversation_topics(keywords)
                for i, t in enumerate(topics, 1):
                    st.write(f"**{i}.** {t}")
                # :필름_프레임: 영상 목록
                st.subheader("🎥: 인기 영상 목록")
                for v in videos:
                    st.markdown(f"- [{v['title']}]({v['url']})")
                # :받은_편지함_트레이: 다운로드
                st.subheader("📥: 결과 다운로드")
                csv = keyword_df.to_csv(index=False)
                st.download_button("📄:글씨가_쓰여진_페이지: 키워드 CSV 다운로드", csv, "youtube_trend_keywords.csv", mime="text/csv")
                txt = "\n".join(topics)
                st.download_button("💬: 대화 주제 TXT 다운로드", txt, "youtube_conversation_topics.txt", mime="text/plain")