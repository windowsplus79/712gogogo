import streamlit as st
import pandas as pd
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="AI Learning Hub",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-box {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .progress-bar {
        background: #e9ecef;
        border-radius: 10px;
        height: 20px;
        overflow: hidden;
    }
    .progress-fill {
        background: linear-gradient(90deg, #28a745, #20c997);
        height: 100%;
        transition: width 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

def init_session_state():
    """세션 상태 초기화"""
    if 'student_info' not in st.session_state:
        st.session_state.student_info = {}
    if 'progress' not in st.session_state:
        st.session_state.progress = {
            'supervised': False,
            'unsupervised': False,
            'evaluation': False
        }
    if 'start_time' not in st.session_state:
        st.session_state.start_time = datetime.now()

def show_progress():
    """학습 진도 표시"""
    completed = sum(st.session_state.progress.values())
    total = len(st.session_state.progress)
    progress_percent = (completed / total) * 100
    
    st.markdown("### 📊 학습 진도")
    st.markdown(f"""
    <div class="progress-bar">
        <div class="progress-fill" style="width: {progress_percent}%"></div>
    </div>
    <p style="text-align: center; margin-top: 10px;">
        {completed}/{total} 완료 ({progress_percent:.0f}%)
    </p>
    """, unsafe_allow_html=True)

def main():
    init_session_state()
    
    # 메인 헤더
    st.markdown("""
    <div class="main-header">
        <h1>🤖 AI Learning Hub</h1>
        <h3>고등학교 정보수업 - 인공지능 체험 플랫폼</h3>
        <p>지도학습과 비지도학습을 직접 체험하며 배워보세요!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 사이드바에 학생 정보 입력
    with st.sidebar:
        st.markdown("### 👨‍🎓 학생 정보")
        student_name = st.text_input("이름", value=st.session_state.student_info.get('name', ''))
        student_id = st.text_input("학번", value=st.session_state.student_info.get('id', ''))
        
        if student_name and student_id:
            st.session_state.student_info = {
                'name': student_name,
                'id': student_id
            }
            st.success("✅ 학
