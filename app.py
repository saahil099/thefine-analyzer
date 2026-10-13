import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from google import genai

# Page Config
st.set_page_config(page_title="TheFindTv Trend Analyzer", page_icon="📈", layout="wide")

st.title("🎬 TheFindTv - Video Trend & Topic Analyzer AI")
st.markdown("Yahan kisi bhi YouTube video ka link dalein. AI aapko batayega ke ye topic is waqt internet aur social media par trend kar raha hai ya nahi, aur **TheFindTv** ke liye is par video kaise banani chahiye.")

# Gemini API Key Input (Sidebar)
st.sidebar.header("🔑 Settings")
api_key = st.sidebar.text_input("Enter Google Gemini API Key", type="password")

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip:** Agar aapke paas API key nahi hai, toh Google AI Studio par jaakar bilkul free mein hasil kar sakte hain.")

# Function to extract video ID from YouTube URL
def extract_youtube_id(url):
    if "youtu.be" in url:
        return url.split("/")[-1].split("?")[0]
    elif "watch?v=" in url:
        return url.split("watch?v=")[1].split("&")[0]
    return None

# Main Input Form
video_url = st.text_input("🔗 Paste YouTube Video Link Here:", placeholder="https://www.youtube.com/watch?v=...")

if st.button("🚀 Analyze Trend & Generate Strategy"):
    if not api_key:
        st.error("Barah-e-karam pehle sidebar mein apni Gemini API Key enter karein!")
    elif not video_url:
        st.error("Barah-e-karam koi valid YouTube link enter karein.")
    else:
        video_id = extract_youtube_id(video_url)
        
        if not video_id:
            st.error("Invalid YouTube URL! Sahi link enter karein.")
        else:
            with st.spinner("🔄 Video data fetch ho raha hai aur AI market research kar raha hai..."):
                try:
                    # Fetch Transcript
                    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
                    transcript_text = " ".join([item['text'] for item in transcript_list])
                except Exception as e:
                    transcript_text = "Transcript directly fetch nahi ho saka, lekin AI video ke topic aur metadata ke mutabiq analysis karega."

                # Initialize Gemini Client
                client = genai.Client(api_key=api_key)
                
                prompt = f"""
                You are an expert YouTube Content Strategist and SEO Market Analyst for the popular channel 'TheFindTv'.
                Analyze the following video content/transcript:
                ---
                {transcript_text[:5000]}
                ---
                
                Provide a detailed research report in Roman Urdu/English format covering:
                1. **Trend & Market Demand (Google & Social Media):** Is this topic currently trending or searched widely? What is the current public interest level?
                2. **Search Intent & Target Keywords:** What exact search terms, long-tail keywords, and queries are people using regarding this topic?
                3. **TheFindTv Unique Angle:** How can 'TheFindTv' cover this topic in a unique, highly engaging documentary/investigative style to hook viewers?
                4. **High-CTR Video Title Options:** Give 3 viral title ideas optimized for maximum clicks.
                5. **Video Outline / Structure:** A scene-by-scene structural breakdown for the script.
                """

                try:
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt
                    )
                    
                    st.success("✅ Analysis Complete!")
                    st.markdown("### 📊 Market & Strategy Report for TheFindTv")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"Error generating AI analysis: {e}")
