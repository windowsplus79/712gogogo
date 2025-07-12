import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, mean_squared_error
from datetime import datetime
import time
import warnings
warnings.filterwarnings('ignore')

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
    .concept-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
    }
    .practice-box {
        background: #f8f9fa;
        border: 2px solid #28a745;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .result-box {
        background: #e7f3ff;
        border-left: 4px solid #007bff;
        padding: 1rem;
        margin: 1rem 0;
    }
    .quiz-container {
        background: #f8f9fa;
        border: 2px solid #007bff;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
    }
    .question-box {
        background: white;
        border-left: 4px solid #007bff;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 8px;
    }
    .timer-box {
        background: linear-gradient(45deg, #ff6b6b, #feca57);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-size: 1.2em;
        font-weight: bold;
    }
    .result-excellent {
        background: linear-gradient(45deg, #56ab2f, #a8e6cf);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
    }
    .result-good {
        background: linear-gradient(45deg, #f093fb, #f5576c);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
    }
    .result-need-review {
        background: linear-gradient(45deg, #ffeaa7, #fab1a0);
        color: #2d3436;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
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
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
    if 'quiz_start_time' not in st.session_state:
        st.session_state.quiz_start_time = None
    if 'quiz_answers' not in st.session_state:
        st.session_state.quiz_answers = {}

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

def show_sidebar():
    """사이드바 표시"""
    with st.sidebar:
        st.markdown("### 👨‍🎓 학생 정보")
        student_name = st.text_input("이름", value=st.session_state.student_info.get('name', ''))
        student_id = st.text_input("학번", value=st.session_state.student_info.get('id', ''))
        
        if student_name and student_id:
            st.session_state.student_info = {
                'name': student_name,
                'id': student_id
            }
            st.success("학생 정보가 저장되었습니다!")
        
        st.markdown("---")
        show_progress()
        
        st.markdown("---")
        st.markdown("### 🧭 페이지 이동")
        
        if st.button("🏠 홈", use_container_width=True):
            st.session_state.current_page = 'home'
            st.rerun()
        
        if st.button("🎯 지도학습", use_container_width=True):
            st.session_state.current_page = 'supervised'
            st.rerun()
        
        if st.button("🔍 비지도학습", use_container_width=True):
            st.session_state.current_page = 'unsupervised'
            st.rerun()
        
        if st.button("📝 형성평가", use_container_width=True):
            st.session_state.current_page = 'evaluation'
            st.rerun()

def show_home_page():
    """홈 페이지 표시"""
    # 메인 헤더
    st.markdown("""
    <div class="main-header">
        <h1>🤖 AI Learning Hub</h1>
        <h3>고등학교 정보수업 - 인공지능 체험 플랫폼</h3>
        <p>지도학습과 비지도학습을 직접 체험하며 배워보세요!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 메인 콘텐츠
    if not (st.session_state.student_info.get('name') and st.session_state.student_info.get('id')):
        st.warning("먼저 사이드바에서 이름과 학번을 입력해주세요!")
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
    1. 왼쪽 사이드바에서 각 페이지로 이동하세요
    2. 지도학습 → 비지도학습 → 형성평가 순서로 진행해주세요
    3. 각 페이지에서 이론 학습 후 실습 체험을 해보세요
    4. 마지막에 형성평가를 통해 학습 내용을 확인해보세요
    """)
    
    # 시작하기 버튼
    st.markdown("### 🚀 학습 시작하기")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎯 지도학습 시작", use_container_width=True):
            st.session_state.current_page = "supervised"
            st.rerun()
    
    with col2:
        if st.button("🔍 비지도학습 시작", use_container_width=True):
            st.session_state.current_page = "unsupervised"
            st.rerun()
    
    with col3:
        if st.button("📝 형성평가 시작", use_container_width=True):
            st.session_state.current_page = "evaluation"
            st.rerun()
    
    # 하단 정보
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6c757d;">
        <p>💡 <strong>Tip:</strong> 각 단계를 차근차근 따라가며 AI의 원리를 이해해보세요!</p>
        <p>🕐 예상 소요시간: 지도학습 25분 + 비지도학습 20분 + 형성평가 5분</p>
    </div>
    """, unsafe_allow_html=True)

# 여기에 지도학습, 비지도학습, 형성평가 함수들을 추가
def generate_classification_data():
    """분류용 샘플 데이터 생성"""
    np.random.seed(42)
    n_samples = 200
    
    # 학생 성적 데이터 생성
    study_time = np.random.normal(5, 2, n_samples)  # 공부 시간
    sleep_time = np.random.normal(7, 1, n_samples)  # 수면 시간
    
    # 합격/불합격 결정 (논리적 규칙 적용)
    pass_prob = (study_time * 0.3 + sleep_time * 0.1 - 2) / 5
    pass_exam = (np.random.random(n_samples) < pass_prob).astype(int)
    
    df = pd.DataFrame({
        '공부시간': np.clip(study_time, 0, 12),
        '수면시간': np.clip(sleep_time, 4, 10),
        '시험결과': ['합격' if x == 1 else '불합격' for x in pass_exam]
    })
    
    return df

def generate_regression_data():
    """회귀용 샘플 데이터 생성"""
    np.random.seed(42)
    n_samples = 100
    
    # 집 크기에 따른 가격 데이터
    size = np.random.normal(100, 30, n_samples)  # 평수
    age = np.random.randint(1, 30, n_samples)    # 건물 연수
    
    # 가격 계산 (논리적 규칙)
    price = size * 50 - age * 10 + np.random.normal(0, 500, n_samples)
    
    df = pd.DataFrame({
        '평수': np.clip(size, 30, 200),
        '건물연수': age,
        '가격(만원)': np.clip(price, 1000, 15000)
    })
    
    return df

def generate_customer_data():
    """고객 세분화용 샘플 데이터 생성"""
    np.random.seed(42)
    n_customers = 300
    
    # 3개 고객 그룹 생성
    # 그룹 1: 젊은 고소득층 (온라인 쇼핑 선호)
    group1_age = np.random.normal(28, 5, 100)
    group1_income = np.random.normal(7000, 1000, 100)
    group1_online = np.random.normal(80, 10, 100)
    
    # 그룹 2: 중년 중소득층 (오프라인 쇼핑 선호)
    group2_age = np.random.normal(45, 8, 100)
    group2_income = np.random.normal(5000, 800, 100)
    group2_online = np.random.normal(30, 15, 100)
    
    # 그룹 3: 고령 고소득층 (프리미엄 상품 선호)
    group3_age = np.random.normal(60, 7, 100)
    group3_income = np.random.normal(8000, 1200, 100)
    group3_online = np.random.normal(50, 20, 100)
    
    # 데이터 결합
    ages = np.concatenate([group1_age, group2_age, group3_age])
    incomes = np.concatenate([group1_income, group2_income, group3_income])
    online_scores = np.concatenate([group1_online, group2_online, group3_online])
    
    # 데이터 정리
    df = pd.DataFrame({
        '나이': np.clip(ages, 20, 70).astype(int),
        '연소득(만원)': np.clip(incomes, 2000, 12000).astype(int),
        '온라인구매점수': np.clip(online_scores, 0, 100).astype(int)
    })
    
    # 고객 ID 추가
    df['고객ID'] = [f'C{i:03d}' for i in range(1, len(df) + 1)]
    
    return df

def show_supervised_learning():
    """지도학습 페이지"""
    st.markdown("# 🎯 지도학습 (Supervised Learning)")
    st.markdown(f"**학습자**: {st.session_state.student_info['name']} ({st.session_state.student_info['id']})")
    
    # 탭 구성
    tab1, tab2, tab3 = st.tabs(["📚 개념 학습", "🎯 분류 실습", "📈 회귀 실습"])
    
    with tab1:
        st.markdown("""
        <div class="concept-box">
            <h2>🎯 지도학습이란?</h2>
            <p><strong>정답이 있는 데이터</strong>로 컴퓨터를 학습시키는 방법입니다.</p>
            <p>마치 선생님이 문제와 정답을 함께 주고 공부시키는 것과 같아요!</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 🔍 분류 (Classification)
            - **목적**: 데이터를 카테고리로 분류
            - **예시**: 
              - 이메일 → 스팸 or 정상
              - 사진 → 고양이 or 강아지
              - 학생 성적 → 합격 or 불합격
            """)
        
        with col2:
            st.markdown("""
            ### 📈 회귀 (Regression)
            - **목적**: 연속적인 수치 예측
            - **예시**:
              - 집 크기 → 집 가격
              - 공부시간 → 시험점수
              - 광고비 → 매출액
            """)
    
    with tab2:
        st.markdown("""
        <div class="practice-box">
            <h3>🎯 분류 실습: 시험 합격/불합격 예측</h3>
            <p>학생들의 공부시간과 수면시간 데이터를 보고 시험 합격 여부를 예측해보세요!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 데이터 생성 및 표시
        df_class = generate_classification_data()
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### 📊 학습 데이터")
            st.dataframe(df_class.head(10), use_container_width=True)
            st.caption(f"총 {len(df_class)}명의 학생 데이터")
        
        with col2:
            # 데이터 분포 시각화
            fig = px.scatter(df_class, x='공부시간', y='수면시간', color='시험결과',
                           title="학생 데이터 분포", 
                           color_discrete_map={'합격': 'green', '불합격': 'red'})
            st.plotly_chart(fig, use_container_width=True)
        
        # 모델 학습 버튼
        if st.button("🤖 AI 모델 학습시키기", type="primary", key="supervised_train"):
            with st.spinner("AI가 데이터를 학습하고 있습니다..."):
                # 데이터 준비
                X = df_class[['공부시간', '수면시간']]
                y = df_class['시험결과'].map({'합격': 1, '불합격': 0})
                
                # 학습/테스트 데이터 분할
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
                
                # 모델 학습
                model = RandomForestClassifier(random_state=42)
                model.fit(X_train, y_train)
                
                # 예측 및 평가
                y_pred = model.predict(X_test)
                accuracy = accuracy_score(y_test, y_pred)
                
                st.success(f"학습 완료! 정확도: {accuracy:.2%}")
    
    with tab3:
        st.markdown("""
        <div class="practice-box">
            <h3>📈 회귀 실습: 부동산 가격 예측</h3>
            <p>집의 평수와 건물 연수를 보고 가격을 예측해보세요!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 데이터 생성 및 표시
        df_reg = generate_regression_data()
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### 📊 부동산 데이터")
            st.dataframe(df_reg.head(10), use_container_width=True)
            st.caption(f"총 {len(df_reg)}개의 부동산 데이터")
        
        with col2:
            # 3D 산점도
            fig = px.scatter_3d(df_reg, x='평수', y='건물연수', z='가격(만원)',
                              title="부동산 데이터 3D 시각화")
            st.plotly_chart(fig, use_container_width=True)
    
    # 학습 완료 처리
    if st.button("🎯 지도학습 완료", type="primary", key="supervised_complete"):
        st.session_state.progress['supervised'] = True
        st.success("지도학습을 완료했습니다! 이제 비지도학습으로 넘어가세요.")
        st.balloons()

def show_unsupervised_learning():
    """비지도학습 페이지"""
    st.markdown("# 🔍 비지도학습 (Unsupervised Learning)")
    st.markdown(f"**학습자**: {st.session_state.student_info['name']} ({st.session_state.student_info['id']})")
    
    # 탭 구성
    tab1, tab2 = st.tabs(["📚 개념 학습", "👥 고객 세분화 실습"])
    
    with tab1:
        st.markdown("""
        <div class="concept-box">
            <h2>🔍 비지도학습이란?</h2>
            <p><strong>정답이 없는 데이터</strong>에서 숨겨진 패턴을 찾는 방법입니다.</p>
            <p>마치 탐정이 단서들을 보고 사건의 진실을 추리하는 것과 같아요!</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### ❓ 지도학습 vs 비지도학습
            
            **지도학습** 🎯
            - 정답이 있는 데이터로 학습
            - 예: 사진 → 고양이/강아지
            - 목표: 정확한 예측
            
            **비지도학습** 🔍
            - 정답이 없는 데이터에서 패턴 발견
            - 예: 고객 구매 패턴 분석
            - 목표: 숨겨진 구조 발견
            """)
        
        with col2:
            st.markdown("""
            ### 🔍 클러스터링 (Clustering)
            
            - **목적**: 비슷한 특성의 데이터끼리 그룹화
            - **활용 예시**:
              - 고객 세분화 (마케팅)
              - 상품 추천 시스템
              - 이상 거래 탐지
              - 유전자 분석
            """)
    
    with tab2:
        st.markdown("""
        <div class="practice-box">
            <h3>👥 고객 세분화 실습</h3>
            <p>쇼핑몰 고객 데이터를 분석해서 비슷한 특성의 고객 그룹을 찾아보세요!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 고객 데이터 생성
        df_customers = generate_customer_data()
        
        # 데이터 미리보기
        st.markdown("#### 📊 고객 데이터")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.dataframe(df_customers.head(15), use_container_width=True)
        
        with col2:
            st.markdown("**데이터 설명**")
            st.markdown("""
            - **고객ID**: 고객 식별번호
            - **나이**: 고객 연령
            - **연소득**: 연간 소득 (만원)
            - **온라인구매점수**: 온라인 쇼핑 선호도 (0-100)
            """)
            st.metric("총 고객 수", len(df_customers))
        
        # 클러스터 수 선택
        st.markdown("#### 🎯 클러스터링 실행")
        n_clusters = st.slider("몇 개의 고객 그룹으로 나누고 싶나요?", 2, 6, 3)
        
        if st.button("🔍 고객 그룹 찾기", type="primary", key="unsupervised_cluster"):
            with st.spinner("AI가 고객 그룹을 찾고 있습니다..."):
                # 데이터 전처리
                X = df_customers[['나이', '연소득(만원)', '온라인구매점수']].values
                scaler = StandardScaler()
                X_scaled = scaler.fit_transform(X)
                
                # K-means 클러스터링
                kmeans = KMeans(n_clusters=n_clusters, random_state=42)
                clusters = kmeans.fit_predict(X_scaled)
                
                # 결과를 데이터프레임에 추가
                df_result = df_customers.copy()
                df_result['고객그룹'] = [f'그룹 {i+1}' for i in clusters]
                
                st.success(f"{n_clusters}개의 고객 그룹을 발견했습니다!")
                
                # 클러스터링 결과 시각화
                fig = px.scatter(df_result, 
                               x='나이', 
                               y='연소득(만원)',
                               color='고객그룹',
                               title="고객 그룹 분류 결과",
                               hover_data=['고객ID'])
                st.plotly_chart(fig, use_container_width=True)
    
    # 학습 완료 처리
    if st.button("🔍 비지도학습 완료", type="primary", key="unsupervised_complete"):
        st.session_state.progress['unsupervised'] = True
        st.success("비지도학습을 완료했습니다! 이제 형성평가를 받아보세요.")
        st.balloons()

# 퀴즈 문제 정의
QUIZ_QUESTIONS = [
    {
        "id": "q1",
        "question": "지도학습에 대한 설명으로 가장 올바른 것은?",
        "options": [
            "정답이 없는 데이터로 학습하는 방법",
            "정답이 있는 데이터로 학습하는 방법", 
            "데이터 없이 학습하는 방법",
            "사람이 직접 모든 규칙을 입력하는 방법"
        ],
        "correct": 1,
        "explanation": "지도학습은 입력(X)과 정답(y)이 모두 있는 데이터로 AI를 학습시키는 방법입니다."
    },
    {
        "id": "q2", 
        "question": "다음 중 지도학습의 예시가 아닌 것은?",
        "options": [
            "이메일 스팸 분류",
            "집 가격 예측",
            "고객 그룹 세분화",
            "시험 점수 예측"
        ],
        "correct": 2,
        "explanation": "고객 그룹 세분화는 정답 없이 고객들의 유사한 특성을 찾는 비지도학습의 예시입니다."
    },
    {
        "id": "q3",
        "question": "비지도학습의 주요 목적은 무엇인가요?",
        "options": [
            "정확한 예측값 계산",
            "데이터에서 숨겨진 패턴 발견",
            "정답과 입력의 관계 학습",
            "오류율 최소화"
        ],
        "correct": 1,
        "explanation": "비지도학습은 정답이 없는 데이터에서 숨겨진 패턴이나 구조를 발견하는 것이 목적입니다."
    },
    {
        "id": "q4",
        "question": "클러스터링(Clustering)에 대한 설명으로 올바른 것은?",
        "options": [
            "데이터를 미리 정해진 정답에 따라 분류",
            "비슷한 특성을 가진 데이터끼리 그룹으로 묶기",
            "연속적인 수치값을 예측하기",
            "모든 데이터를 하나의 그룹으로 통합"
        ],
        "correct": 1,
        "explanation": "클러스터링은 유사한 특성을 가진 데이터들을 자동으로 그룹화하는 비지도학습 기법입니다."
    },
    {
        "id": "q5",
        "question": "실습에서 고객 세분화 결과, 젊은 고소득층 그룹에게 가장 적합한 마케팅 전략은?",
        "options": [
            "저가 상품 위주의 할인 이벤트",
            "프리미엄 온라인 상품과 SNS 마케팅",
            "오프라인 매장 방문 유도",
            "기본 기능 중심의 실용적 상품"
        ],
        "correct": 1,
        "explanation": "젊은 고소득층은 온라인 쇼핑을 선호하고 구매력이 높아 프리미엄 상품과 SNS 마케팅이 효과적입니다."
    }
]

def show_evaluation():
    """형성평가 페이지"""
    st.markdown("# 📝 형성평가")
    st.markdown(f"**학습자**: {st.session_state.student_info['name']} ({st.session_state.student_info['id']})")
    
    # 선수 학습 확인
    if not st.session_state.progress.get('supervised') or not st.session_state.progress.get('unsupervised'):
        st.warning("지도학습과 비지도학습을 먼저 완료해주세요!")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎯 지도학습으로 이동", key="go_supervised"):
                st.session_state.current_page = "supervised"
                st.rerun()
        with col2:
            if st.button("🔍 비지도학습으로 이동", key="go_unsupervised"):
                st.session_state.current_page = "unsupervised"
                st.rerun()
        return
    
    if not st.session_state.quiz_started:
        # 퀴즈 시작 전 안내
        st.markdown("""
        <div class="quiz-container">
            <h3>📋 형성평가 안내</h3>
            <p><strong>제한시간:</strong> 5분</p>
            <p><strong>문제 수:</strong> 5문제 (지도학습 2문제 + 비지도학습 2문제 + 실습 관련 1문제)</p>
            <p><strong>평가 방법:</strong> 객관식 선택 후 성찰 작성</p>
            <br>
            <p>💡 <strong>Tip:</strong> 차근차근 문제를 읽고 앞서 학습한 내용을 떠올려보세요!</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📝 형성평가 시작하기", type="primary", use_container_width=True):
            st.session_state.quiz_started = True
            st.session_state.quiz_start_time = time.time()
            st.rerun()
    
    else:
        # 타이머 표시
        if st.session_state.quiz_start_time:
            elapsed_time = time.time() - st.session_state.quiz_start_time
            remaining_time = max(0, 300 - elapsed_time)  # 5분 = 300초
            minutes = int(remaining_time // 60)
            seconds = int(remaining_time % 60)
            
            if remaining_time > 0:
                st.markdown(f"""
                <div class="timer-box">
                    ⏱️ 남은 시간: {minutes:02d}:{seconds:02d}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("⏰ 시간이 종료되었습니다!")
        
        # 퀴즈 문제들
        st.markdown("### 📚 문제를 풀어보세요")
        
        all_answered = True
        
        for i, question in enumerate(QUIZ_QUESTIONS):
            st.markdown(f"""
            <div class="question-box">
                <h4>문제 {i+1}. {question['question']}</h4>
            </div>
            """, unsafe_allow_html=True)
            
            answer = st.radio(
                f"답을 선택하세요:",
                question['options'],
                key=f"q_{question['id']}",
                index=None
            )
            
            if answer is not None:
                st.session_state.quiz_answers[question['id']] = {
                    'answer': answer,
                    'correct': question['options'].index(answer) == question['correct']
                }
            else:
                all_answered = False
            
            st.markdown("---")
        
        # 성찰 작성
        st.markdown("### 🤔 학습 성찰")
        reflection = st.text_area(
            "오늘 AI 학습을 통해 느낀 점을 자유롭게 작성해주세요:",
            placeholder="예: 지도학습과 비지도학습의 차이를 실습으로 직접 체험해보니...",
            height=100,
            key="reflection"
        )
        
        # 제출 버튼
        if all_answered and reflection.strip():
            if st.button("📤 제출하기", type="primary", use_container_width=True):
                # 점수 계산
                correct_answers = sum(1 for ans in st.session_state.quiz_answers.values() if ans['correct'])
                total_questions = len(QUIZ_QUESTIONS)
                score_percentage = (correct_answers / total_questions) * 100
                
                # 결과 표시
                if score_percentage >= 80:
                    result_class = "result-excellent"
                    message = "🎉 우수! 인공지능 개념을 잘 이해했습니다!"
                elif score_percentage >= 60:
                    result_class = "result-good"
                    message = "👍 양호! 기본 개념을 이해했습니다!"
                else:
                    result_class = "result-need-review"
                    message = "📚 복습 필요! 다시 한 번 학습해보세요!"
                
                st.markdown(f"""
                <div class="{result_class}">
                    <h2>{message}</h2>
                    <h3>점수: {correct_answers}/{total_questions} ({score_percentage:.0f}점)</h3>
                </div>
                """, unsafe_allow_html=True)
                
                st.session_state.progress['evaluation'] = True
                
                # 학습 완료 축하
                if all(st.session_state.progress.values()):
                    st.balloons()
                    st.markdown("""
                    ### 🎊 축하합니다!
                    모든 학습을 완료했습니다! 인공지능의 기초 개념을 잘 이해하셨네요.
                    앞으로도 AI에 대한 관심을 가지고 더 깊이 학습해보세요!
                    """)
        
        elif not all_answered:
            st.warning("모든 문제에 답을 선택해주세요.")
        elif not reflection.strip():
            st.warning("학습 성찰을 작성해주세요.")

def main():
    init_session_state()
    
    # 학생 정보 확인
    if not (st.session_state.student_info.get('name') and st.session_state.student_info.get('id')):
        show_sidebar()
        if st.session_state.current_page != 'home':
            st.session_state.current_page = 'home'
            st.rerun()
    
    show_sidebar()
    
    # 페이지 라우팅
    if st.session_state.current_page == 'home':
        show_home_page()
    elif st.session_state.current_page == 'supervised':
        show_supervised_learning()
    elif st.session_state.current_page == 'unsupervised':
        show_unsupervised_learning()
    elif st.session_state.current_page == 'evaluation':
        show_evaluation()

if __name__ == "__main__":
    main()
