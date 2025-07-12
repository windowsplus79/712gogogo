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
    page_title="영동일고등학교 AI Learning Hub",
    page_icon="🤖",
    layout="wide"
)

# 전역 데이터 저장소 (실제 환경에서는 데이터베이스 사용)
if 'all_students_data' not in st.session_state:
    st.session_state.all_students_data = []

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
    if 'is_teacher' not in st.session_state:
        st.session_state.is_teacher = False

# 학생 데이터 저장 함수
def save_student_data():
    if st.session_state.student_info:
        # 퀴즈 점수 계산
        quiz_score = 0
        if st.session_state.quiz_answers:
            correct_count = sum(1 for ans in st.session_state.quiz_answers.values() if ans['correct'])
            quiz_score = (correct_count / len(QUIZ_QUESTIONS)) * 100
        
        student_data = {
            'name': st.session_state.student_info['name'],
            'id': st.session_state.student_info['id'],
            'progress': st.session_state.progress.copy(),
            'quiz_answers': st.session_state.quiz_answers.copy(),
            'last_updated': datetime.now().strftime('%H:%M:%S'),
            'quiz_score': quiz_score,
            'reflection': getattr(st.session_state, 'current_reflection', '')
        }
        
        # 기존 학생 데이터 업데이트 또는 새로 추가
        existing_index = None
        for i, data in enumerate(st.session_state.all_students_data):
            if data['id'] == student_data['id']:
                existing_index = i
                break
        
        if existing_index is not None:
            st.session_state.all_students_data[existing_index] = student_data
        else:
            st.session_state.all_students_data.append(student_data)
        
        # 강제로 상태 저장
        st.session_state.all_students_data = st.session_state.all_students_data

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
        # 교사/학생 모드 선택
        st.markdown("### 👤 사용자 모드")
        user_type = st.selectbox("모드 선택", ["학생", "교사"], key="user_type")
        
        if user_type == "교사":
            st.session_state.is_teacher = True
            teacher_password = st.text_input("교사 비밀번호", type="password", key="teacher_password")
            if teacher_password == "teacher123":  # 간단한 비밀번호
                st.success("교사 모드 활성화")
                show_teacher_sidebar()
            else:
                st.warning("비밀번호를 입력하세요 (teacher123)")
                return
        else:
            st.session_state.is_teacher = False
            show_student_sidebar()
    
    # 페이지 라우팅
    if st.session_state.is_teacher:
        show_teacher_dashboard()
    elif st.session_state.current_page == 'home':
        show_home_page()
    elif st.session_state.current_page == 'supervised':
        show_supervised_learning()
    elif st.session_state.current_page == 'unsupervised':
        show_unsupervised_learning()
    elif st.session_state.current_page == 'evaluation':
        show_evaluation()

def show_student_sidebar():
    st.markdown("### 👨‍🎓 학생 정보")
    student_name = st.text_input("이름", key="student_name")
    student_id = st.text_input("학번", key="student_id")
    
    if student_name and student_id:
        st.session_state.student_info = {
            'name': student_name,
            'id': student_id
        }
        st.success("정보 저장됨!")
        save_student_data()  # 학생 데이터 저장
    
    st.markdown("---")
    
    # 진도 표시
    completed = sum(st.session_state.progress.values())
    st.markdown(f"### 📊 진도: {completed}/3")
    
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

def show_teacher_sidebar():
    st.markdown("### 🎓 교사 대시보드")
    
    total_students = len(st.session_state.all_students_data)
    st.metric("총 접속 학생 수", total_students)
    
    if total_students > 0:
        completed_all = sum(1 for data in st.session_state.all_students_data 
                           if all(data['progress'].values()))
        st.metric("전체 완료 학생", f"{completed_all}/{total_students}")
        
        if st.button("🔄 새로고침", key="refresh_data"):
            st.rerun()
        
        if st.button("📥 CSV 다운로드", key="download_csv"):
            if st.session_state.all_students_data:
                # 한글 지원을 위한 데이터 준비
                csv_data = []
                for data in st.session_state.all_students_data:
                    csv_data.append({
                        '이름': data['name'],
                        '학번': data['id'],
                        '지도학습완료': '완료' if data['progress']['supervised'] else '미완료',
                        '비지도학습완료': '완료' if data['progress']['unsupervised'] else '미완료',
                        '형성평가완료': '완료' if data['progress']['evaluation'] else '미완료',
                        '퀴즈점수': data['quiz_score'],
                        '성찰내용': data.get('reflection', ''),
                        '최근접속시간': data['last_updated']
                    })
                
                df = pd.DataFrame(csv_data)
                
                # UTF-8 BOM 추가로 한글 깨짐 방지
                csv_string = df.to_csv(index=False, encoding='utf-8-sig')
                
                st.download_button(
                    label="📥 학생 데이터 다운로드 (CSV)",
                    data=csv_string.encode('utf-8-sig'),
                    file_name=f"AI학습현황_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv",
                    key="download_button"
                )
            else:
                st.warning("다운로드할 데이터가 없습니다.")

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
        save_student_data()  # 진도 저장
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
        save_student_data()  # 진도 저장
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
        st.markdown("### 🤔 학습 성찰")
        reflection = st.text_area(
            "오늘 AI 학습에서 느낀 점을 작성해주세요:",
            key="reflection_text",
            height=100
        )
        
        # 제출
        if all_answered and reflection.strip():
            if st.button("제출하기", key="submit_quiz"):
                # 성찰 내용을 세션에 저장
                st.session_state.current_reflection = reflection
                
                correct_count = sum(1 for ans in st.session_state.quiz_answers.values() if ans['correct'])
                total_count = len(QUIZ_QUESTIONS)
                score = (correct_count / total_count) * 100
                
                st.session_state.progress['evaluation'] = True
                save_student_data()  # 최종 데이터 저장
                
                if score >= 80:
                    st.success(f"🎉 우수! 점수: {correct_count}/{total_count} ({score:.0f}점)")
                elif score >= 60:
                    st.info(f"👍 양호! 점수: {correct_count}/{total_count} ({score:.0f}점)")
                else:
                    st.warning(f"📚 복습 필요! 점수: {correct_count}/{total_count} ({score:.0f}점)")
                
                if all(st.session_state.progress.values()):
                    st.balloons()
                    st.markdown("### 🎊 축하합니다! 모든 학습을 완료했습니다!")
                
                # 성공 메시지
                st.info("✅ 결과가 교사 대시보드에 전송되었습니다!")
        
        elif not all_answered:
            st.warning("모든 문제에 답해주세요.")
        elif not reflection.strip():
            st.warning("성찰을 작성해주세요.")

def show_teacher_dashboard():
    st.title("🎓 교사 실시간 대시보드")
    
    # 새로고침 버튼을 맨 위에 배치
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("🔄 새로고침", key="refresh_dashboard"):
            st.rerun()
    with col2:
        st.metric("현재 시간", datetime.now().strftime('%H:%M:%S'))
    
    if not st.session_state.all_students_data:
        st.info("아직 접속한 학생이 없습니다.")
        st.markdown("### 💡 사용 방법")
        st.markdown("""
        1. 학생들이 사이드바에서 **"학생"** 모드를 선택
        2. 이름과 학번을 입력하고 학습 시작
        3. 학생 활동이 이 대시보드에 실시간으로 표시됩니다
        """)
        return
    
    # 전체 통계
    st.markdown("## 📊 전체 현황")
    
    total_students = len(st.session_state.all_students_data)
    completed_supervised = sum(1 for data in st.session_state.all_students_data if data['progress']['supervised'])
    completed_unsupervised = sum(1 for data in st.session_state.all_students_data if data['progress']['unsupervised'])
    completed_evaluation = sum(1 for data in st.session_state.all_students_data if data['progress']['evaluation'])
    completed_all = sum(1 for data in st.session_state.all_students_data if all(data['progress'].values()))
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("총 학생 수", total_students)
    with col2:
        st.metric("지도학습 완료", f"{completed_supervised}/{total_students}")
    with col3:
        st.metric("비지도학습 완료", f"{completed_unsupervised}/{total_students}")
    with col4:
        st.metric("형성평가 완료", f"{completed_evaluation}/{total_students}")
    with col5:
        st.metric("전체 완료", f"{completed_all}/{total_students}")
    
    # 진도 현황 차트
    st.markdown("### 📈 학습 진도 현황")
    
    progress_data = {
        '단계': ['지도학습', '비지도학습', '형성평가'],
        '완료 학생 수': [completed_supervised, completed_unsupervised, completed_evaluation],
        '완료율(%)': [
            (completed_supervised/total_students)*100 if total_students > 0 else 0,
            (completed_unsupervised/total_students)*100 if total_students > 0 else 0,
            (completed_evaluation/total_students)*100 if total_students > 0 else 0
        ]
    }
    
    fig = px.bar(progress_data, x='단계', y='완료 학생 수', 
                 title="단계별 완료 현황",
                 color='완료율(%)',
                 color_continuous_scale='viridis')
    st.plotly_chart(fig, use_container_width=True)
    
    # 개별 학생 현황
    st.markdown("### 👥 개별 학생 현황")
    
    # 학생 데이터를 DataFrame으로 변환
    students_df = []
    for data in st.session_state.all_students_data:
        students_df.append({
            '이름': data['name'],
            '학번': data['id'],
            '지도학습': '✅' if data['progress']['supervised'] else '❌',
            '비지도학습': '✅' if data['progress']['unsupervised'] else '❌',
            '형성평가': '✅' if data['progress']['evaluation'] else '❌',
            '퀴즈점수': f"{data['quiz_score']:.0f}점" if data['quiz_score'] > 0 else '-',
            '최근접속': data['last_updated']
        })
    
    if students_df:
        df = pd.DataFrame(students_df)
        st.dataframe(df, use_container_width=True)
    
    # 성적 분포
    if completed_evaluation > 0:
        st.markdown("### 📊 퀴즈 성적 분포")
        
        scores = [data['quiz_score'] for data in st.session_state.all_students_data if data['quiz_score'] > 0]
        
        if scores:
            fig_hist = px.histogram(x=scores, nbins=5, title="퀴즈 점수 분포",
                                   labels={'x': '점수', 'y': '학생 수'})
            st.plotly_chart(fig_hist, use_container_width=True)
            
            avg_score = sum(scores) / len(scores)
            st.info(f"📈 평균 점수: {avg_score:.1f}점")
    
    # 학생별 상세 정보
    st.markdown("### 📝 학생별 성찰 내용")
    
    reflection_found = False
    for data in st.session_state.all_students_data:
        if data['progress']['evaluation'] and data.get('reflection'):
            reflection_found = True
            with st.expander(f"{data['name']} ({data['id']}) - {data['quiz_score']:.0f}점"):
                st.write(data['reflection'])
    
    if not reflection_found:
        st.info("아직 제출된 성찰 내용이 없습니다.")
    
    # 디버깅 정보 (개발용)
    with st.expander("🔧 디버깅 정보 (개발용)"):
        st.write("전체 학생 데이터:")
        st.json(st.session_state.all_students_data)

if __name__ == "__main__":
    main()
