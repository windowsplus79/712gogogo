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
            st.success("✅ 학생 정보가 저장되었습니다!")
        
        st.markdown("---")
        show_progress()
    
    # 메인 콘텐츠
    if not (st.session_state.student_info.get('name') and st.session_state.student_info.get('id')):
        st.warning("👈 먼저 사이드바에서 이름과 학번을 입력해주세요!")
        return
    
    # 환영 메시지
    st.markdown(f"""
    ### 안녕하세요, {st.session_state.student_info['name']}님! 👋
    
    오늘은 인공지능의 두 가지 주요 학습 방법에 대해 알아보겠습니다:
    """)
    
    # 학습 모듈 소개
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
            <h4>🎯 1차시: 지도학습 (Supervised Learning)</h4>
            <p>정답이 있는 데이터로 학습하는 방법</p>
            <ul>
                <li>분류(Classification) 체험</li>
                <li>회귀(Regression) 체험</li>
                <li>실제 데이터셋으로 실습</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-box">
            <h4>🔍 2차시: 비지도학습 (Unsupervised Learning)</h4>
            <p>정답 없이 패턴을 찾는 학습 방법</p>
            <ul>
                <li>클러스터링(Clustering) 체험</li>
                <li>고객 세분화 실습</li>
                <li>데이터 패턴 발견</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # 학습 안내
    st.markdown("### 📚 학습 진행 방법")
    st.info("""
    1. **왼쪽 사이드바**에서 각 페이지로 이동하세요
    2. **지도학습** → **비지도학습** → **형성평가** 순서로 진행해주세요
    3. 각 페이지에서 이론 학습 후 **실습 체험**을 해보세요
    4. 마지막에 **형성평가**를 통해 학습 내용을 확인해보세요
    """)
    
    # 시작하기 버튼
    st.markdown("### 🚀 학습 시작하기")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎯 지도학습 시작", use_container_width=True):
            st.switch_page("pages/1_지도학습.py")
    
    with col2:
        if st.button("🔍 비지도학습 시작", use_container_width=True):
            st.switch_page("pages/2_비지도학습.py")
    
    with col3:
        if st.button("📝 형성평가 시작", use_container_width=True):
            st.switch_page("pages/3_형성평가.py")
    
    # 하단 정보
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6c757d;">
        <p>💡 <strong>Tip:</strong> 각 단계를 차근차근 따라가며 AI의 원리를 이해해보세요!</p>
        <p>🕐 예상 소요시간: 지도학습 25분 + 비지도학습 20분 + 형성평가 5분</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
