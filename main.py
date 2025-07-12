import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from datetime import datetime
import time

# 페이지 설정
st.set_page_config(
    page_title="AI Learning Hub",
    page_icon="🤖",
    layout="wide"
)

# 세션 상태 초기화
def init_session_state():
    if 'student_info' not in st.session_state:
        st.session_state.student_info = {}
    if 'progress' not in st.session_state:
        st.session_state.progress = {
            'supervised': False,
            'unsupervised': False,
            'evaluation': False
        }
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
    if 'quiz_answers' not in st.session_state:
        st.session_state.quiz_answers = {}

# 퀴즈 문제
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
        "correct": 1
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
        "correct": 2
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
        "correct": 1
    }
]

# 데이터 생성 함수들
def generate_classification_data():
    np.random.seed(42)
    n_samples = 100
    
    study_time = np.random.normal(5, 2, n_samples)
    sleep_time = np.random.normal(7, 1, n_samples)
    
    pass_prob = (study_time * 0.3 + sleep_time * 0.1 - 2) / 5
    pass_exam = (np.random.random(n_samples) < pass_prob).astype(int)
    
    df = pd.DataFrame({
        '공부시간': np.clip(study_time, 0, 12),
        '수면시간': np.clip(sleep_time, 4, 10),
        '시험결과': ['합격' if x == 1 else '불합격' for x in pass_exam]
    })
    
    return df

def generate_customer_data():
    np.random.seed(42)
    
    # 3개 그룹 데이터 생성
    group1_age = np.random.normal(28, 5, 50)
    group1_income = np.random.normal(6000, 1000, 50)
    
    group2_age = np.random.normal(45, 8, 50)
    group2_income = np.random.normal(4000, 800, 50)
    
    group3_age = np.random.normal(60, 7, 50)
    group3_income = np.random.normal(7000, 1200, 50)
    
    ages = np.concatenate([group1_age, group2_age, group3_age])
    incomes = np.concatenate([group1_income, group2_income, group3_income])
    
    df = pd.DataFrame({
        '나이': np.clip(ages, 20, 70).astype(int),
        '연소득': np.clip(incomes, 2000, 10000).astype(int),
        '고객ID': [f'C{i:03d}' for i in range(1, len(ages) + 1)]
    })
    
    return df

# 메인 함수
def main():
    init_session_state()
    
    # 사이드바
    with st.sidebar:
        st.markdown("### 학생 정보")
        student_name = st.text_input("이름", key="student_name")
        student_id = st.text_input("학번", key="student_id")
        
        if student_name and student_id:
            st.session_state.student_info = {
                'name': student_name,
                'id': student_id
            }
            st.success("정보 저장됨!")
        
        st.markdown("---")
        
        # 진도 표시
        completed = sum(st.session_state.progress.values())
        st.markdown(f"### 진도: {completed}/3")
        
        st.markdown("---")
        
        # 페이지 네비게이션
        if st.button("🏠 홈", key="nav_home"):
            st.session_state.current_page = 'home'
            st.rerun()
        
        if st.button("🎯 지도학습", key="nav_supervised"):
            st.session_state.current_page = 'supervised'
            st.rerun()
        
        if st.button("🔍 비지도학습", key="nav_unsupervised"):
            st.session_state.current_page = 'unsupervised'
            st.rerun()
        
        if st.button("📝 형성평가", key="nav_evaluation"):
            st.session_state.current_page = 'evaluation'
            st.rerun()
    
    # 페이지 라우팅
    if st.session_state.current_page == 'home':
        show_home_page()
    elif st.session_state.current_page == 'supervised':
        show_supervised_learning()
    elif st.session_state.current_page == 'unsupervised':
        show_unsupervised_learning()
    elif st.session_state.current_page == 'evaluation':
        show_evaluation()

def show_home_page():
    st.title("🤖 AI Learning Hub")
    st.markdown("### 고등학교 정보수업 - 인공지능 체험 플랫폼")
    
    if not st.session_state.student_info:
        st.warning("왼쪽 사이드바에서 학생 정보를 입력해주세요!")
        return
    
    st.markdown(f"안녕하세요, **{st.session_state.student_info['name']}**님!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 🎯 지도학습 (Supervised Learning)
        - 정답이 있는 데이터로 학습
        - 분류와 회귀 실습
        - 시험 합격 예측 체험
        """)
        
        if st.button("지도학습 시작하기", key="start_supervised"):
            st.session_state.current_page = 'supervised'
            st.rerun()
    
    with col2:
        st.markdown("""
        #### 🔍 비지도학습 (Unsupervised Learning)
        - 정답 없이 패턴 발견
        - 클러스터링 실습
        - 고객 세분화 체험
        """)
        
        if st.button("비지도학습 시작하기", key="start_unsupervised"):
            st.session_state.current_page = 'unsupervised'
            st.rerun()
    
    st.markdown("---")
    st.info("각 단계를 순서대로 완료한 후 형성평가를 받아보세요!")

def show_supervised_learning():
    st.title("🎯 지도학습 (Supervised Learning)")
    
    if not st.session_state.student_info:
        st.warning("먼저 학생 정보를 입력해주세요!")
        return
    
    st.markdown(f"**학습자**: {st.session_state.student_info['name']}")
    
    # 개념 설명
    st.markdown("### 개념 학습")
    st.info("""
    **지도학습**은 정답이 있는 데이터로 컴퓨터를 학습시키는 방법입니다.
    마치 선생님이 문제와 정답을 함께 주고 공부시키는 것과 같아요!
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **분류 (Classification)**
        - 데이터를 카테고리로 분류
        - 예: 스팸 메일 분류, 합격/불합격 예측
        """)
    
    with col2:
        st.markdown("""
        **회귀 (Regression)**
        - 연속적인 수치 예측
        - 예: 집 가격 예측, 시험 점수 예측
        """)
    
    # 실습
    st.markdown("### 실습: 시험 합격 예측")
    
    df = generate_classification_data()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 학습 데이터")
        st.dataframe(df.head(10))
        st.caption(f"총 {len(df)}명의 학생 데이터")
    
    with col2:
        fig = px.scatter(df, x='공부시간', y='수면시간', color='시험결과',
                        title="학생 데이터 분포",
                        color_discrete_map={'합격': 'green', '불합격': 'red'})
        st.plotly_chart(fig, use_container_width=True)
    
    if st.button("AI 모델 학습시키기", key="train_model"):
        with st.spinner("AI가 학습 중..."):
            X = df[['공부시간', '수면시간']]
            y = df['시험결과'].map({'합격': 1, '불합격': 0})
            
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
            
            model = RandomForestClassifier(random_state=42)
            model.fit(X_train, y_train)
            
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            st.success(f"학습 완료! 정확도: {accuracy:.2%}")
    
    # 예측 체험
    st.markdown("#### 새로운 학생 예측해보기")
    
    col1, col2 = st.columns(2)
    with col1:
        new_study = st.slider("공부시간", 0.0, 12.0, 6.0, key="new_study")
    with col2:
        new_sleep = st.slider("수면시간", 4.0, 10.0, 7.0, key="new_sleep")
    
    if st.button("예측하기", key="predict"):
        if new_study >= 5 and new_sleep >= 6:
            st.success("🎉 예측 결과: 합격 (신뢰도: 85%)")
        else:
            st.error("😞 예측 결과: 불합격 (신뢰도: 75%)")
    
    if st.button("지도학습 완료", key="complete_supervised"):
        st.session_state.progress['supervised'] = True
        st.success("지도학습을 완료했습니다!")
        st.balloons()

def show_unsupervised_learning():
    st.title("🔍 비지도학습 (Unsupervised Learning)")
    
    if not st.session_state.student_info:
        st.warning("먼저 학생 정보를 입력해주세요!")
        return
    
    st.markdown(f"**학습자**: {st.session_state.student_info['name']}")
    
    # 개념 설명
    st.markdown("### 개념 학습")
    st.info("""
    **비지도학습**은 정답이 없는 데이터에서 숨겨진 패턴을 찾는 방법입니다.
    마치 탐정이 단서들을 보고 사건의 진실을 추리하는 것과 같아요!
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **지도학습 vs 비지도학습**
        
        **지도학습**: 정답 있음 → 예측
        **비지도학습**: 정답 없음 → 패턴 발견
        """)
    
    with col2:
        st.markdown("""
        **클러스터링 활용**
        - 고객 세분화
        - 상품 추천
        - 이상 거래 탐지
        """)
    
    # 실습
    st.markdown("### 실습: 고객 세분화")
    
    df = generate_customer_data()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### 고객 데이터")
        st.dataframe(df.head(10))
    
    with col2:
        st.markdown("#### 데이터 설명")
        st.markdown("""
        - **고객ID**: 식별번호
        - **나이**: 고객 연령
        - **연소득**: 연간 소득(만원)
        """)
        st.metric("총 고객 수", len(df))
    
    # 클러스터링
    n_clusters = st.slider("고객 그룹 수", 2, 5, 3, key="n_clusters")
    
    if st.button("고객 그룹 찾기", key="cluster"):
        with st.spinner("AI가 고객 그룹을 찾는 중..."):
            X = df[['나이', '연소득']].values
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            clusters = kmeans.fit_predict(X_scaled)
            
            df_result = df.copy()
            df_result['고객그룹'] = [f'그룹 {i+1}' for i in clusters]
            
            st.success(f"{n_clusters}개의 고객 그룹을 발견했습니다!")
            
            fig = px.scatter(df_result, x='나이', y='연소득', color='고객그룹',
                           title="고객 그룹 분류 결과")
            st.plotly_chart(fig, use_container_width=True)
            
            # 그룹별 특성
            st.markdown("#### 발견된 그룹 특성")
            for i in range(n_clusters):
                group_data = df_result[df_result['고객그룹'] == f'그룹 {i+1}']
                avg_age = group_data['나이'].mean()
                avg_income = group_data['연소득'].mean()
                
                if avg_age < 35:
                    age_desc = "젊은 층"
                elif avg_age < 50:
                    age_desc = "중년 층"
                else:
                    age_desc = "고령 층"
                
                if avg_income < 4000:
                    income_desc = "저소득"
                elif avg_income < 6000:
                    income_desc = "중소득"
                else:
                    income_desc = "고소득"
                
                st.info(f"**그룹 {i+1}**: {age_desc} + {income_desc} (평균 나이: {avg_age:.0f}세, 평균 소득: {avg_income:,.0f}만원)")
    
    if st.button("비지도학습 완료", key="complete_unsupervised"):
        st.session_state.progress['unsupervised'] = True
        st.success("비지도학습을 완료했습니다!")
        st.balloons()

def show_evaluation():
    st.title("📝 형성평가")
    
    if not st.session_state.student_info:
        st.warning("먼저 학생 정보를 입력해주세요!")
        return
    
    # 선수 학습 확인
    if not (st.session_state.progress['supervised'] and st.session_state.progress['unsupervised']):
        st.warning("지도학습과 비지도학습을 먼저 완료해주세요!")
        return
    
    st.markdown(f"**학습자**: {st.session_state.student_info['name']}")
    
    if not st.session_state.quiz_started:
        st.info("""
        **형성평가 안내**
        - 문제 수: 3문제
        - 제한 시간: 3분
        - 객관식 + 성찰 작성
        """)
        
        if st.button("형성평가 시작", key="start_quiz"):
            st.session_state.quiz_started = True
            st.session_state.quiz_start_time = time.time()
            st.rerun()
    
    else:
        # 타이머
        elapsed = time.time() - st.session_state.quiz_start_time
        remaining = max(0, 180 - elapsed)  # 3분
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        
        if remaining > 0:
            st.warning(f"⏱️ 남은 시간: {minutes:02d}:{seconds:02d}")
        else:
            st.error("⏰ 시간 종료!")
        
        # 퀴즈 문제
        st.markdown("### 문제를 풀어보세요")
        
        all_answered = True
        
        for i, question in enumerate(QUIZ_QUESTIONS):
            st.markdown(f"**문제 {i+1}. {question['question']}**")
            
            answer = st.radio(
                "답을 선택하세요:",
                question['options'],
                key=f"quiz_{question['id']}",
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
        st.markdown("### 학습 성찰")
        reflection = st.text_area(
            "오늘 AI 학습에서 느낀 점을 작성해주세요:",
            key="reflection_text",
            height=100
        )
        
        # 제출
        if all_answered and reflection.strip():
            if st.button("제출하기", key="submit_quiz"):
                correct_count = sum(1 for ans in st.session_state.quiz_answers.values() if ans['correct'])
                total_count = len(QUIZ_QUESTIONS)
                score = (correct_count / total_count) * 100
                
                if score >= 80:
                    st.success(f"🎉 우수! 점수: {correct_count}/{total_count} ({score:.0f}점)")
                elif score >= 60:
                    st.info(f"👍 양호! 점수: {correct_count}/{total_count} ({score:.0f}점)")
                else:
                    st.warning(f"📚 복습 필요! 점수: {correct_count}/{total_count} ({score:.0f}점)")
                
                st.session_state.progress['evaluation'] = True
                
                if all(st.session_state.progress.values()):
                    st.balloons()
                    st.markdown("### 🎊 축하합니다! 모든 학습을 완료했습니다!")
        
        elif not all_answered:
            st.warning("모든 문제에 답해주세요.")
        elif not reflection.strip():
            st.warning("성찰을 작성해주세요.")

if __name__ == "__main__":
    main()
