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
from sklearn.metrics import accuracy_score, mean_squared_error
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="지도학습", page_icon="🎯", layout="wide")

# CSS 스타일
st.markdown("""
<style>
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
</style>
""", unsafe_allow_html=True)

def init_session_state():
    if 'student_info' not in st.session_state:
        st.session_state.student_info = {}
    if 'progress' not in st.session_state:
        st.session_state.progress = {
            'supervised': False,
            'unsupervised': False,
            'evaluation': False
        }

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

def main():
    init_session_state()
    
    # 학생 정보 확인
    if not (st.session_state.student_info.get('name') and st.session_state.student_info.get('id')):
        st.warning("먼저 메인 페이지에서 학생 정보를 입력해주세요!")
        if st.button("메인 페이지로 이동"):
            st.switch_page("main.py")
        return
    
    # 페이지 헤더
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
            
            # 분류 예시 시각화
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=[1, 2, 3, 7, 8, 9],
                y=[1, 2, 1.5, 7, 8, 7.5],
                mode='markers',
                marker=dict(color=['red', 'red', 'red', 'blue', 'blue', 'blue'], size=15),
                name='데이터',
                text=['불합격', '불합격', '불합격', '합격', '합격', '합격'],
                textposition="middle right"
            ))
            fig.update_layout(
                title="분류 예시: 공부시간 vs 성적",
                xaxis_title="공부 시간",
                yaxis_title="평균 점수"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("""
            ### 📈 회귀 (Regression)
            - **목적**: 연속적인 수치 예측
            - **예시**:
              - 집 크기 → 집 가격
              - 공부시간 → 시험점수
              - 광고비 → 매출액
            """)
            
            # 회귀 예시 시각화
            x = np.linspace(0, 10, 50)
            y = 2 * x + 1 + np.random.normal(0, 1, 50)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x, y=y, mode='markers', name='실제 데이터'))
            fig.add_trace(go.Scatter(x=x, y=2*x+1, mode='lines', name='예측 선'))
            fig.update_layout(
                title="회귀 예시: 공부시간 vs 시험점수",
                xaxis_title="공부 시간",
                yaxis_title="시험 점수"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        ### 🔄 지도학습 과정
        1. **데이터 준비**: 입력(X)과 정답(y)이 있는 데이터 수집
        2. **모델 학습**: 컴퓨터가 입력과 정답의 관계를 학습
        3. **예측**: 새로운 데이터에 대해 정답 예측
        4. **평가**: 예측 결과가 얼마나 정확한지 확인
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
        if st.button("🤖 AI 모델 학습시키기", type="primary"):
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
                
                st.success(f"✅ 학습 완료! 정확도: {accuracy:.2%}")
                
                # 결과 분석
                st.markdown("""
                <div class="result-box">
                    <h4>📊 학습 결과 분석</h4>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("모델 정확도", f"{accuracy:.1%}")
                    st.metric("학습 데이터 수", len(X_train))
                    st.metric("테스트 데이터 수", len(X_test))
                
                with col2:
                    # 특성 중요도
                    importance = model.feature_importances_
                    importance_df = pd.DataFrame({
                        '특성': ['공부시간', '수면시간'],
                        '중요도': importance
                    })
                    fig = px.bar(importance_df, x='특성', y='중요도', 
                               title="어떤 요소가 더 중요할까요?")
                    st.plotly_chart(fig, use_container_width=True)
        
        # 새로운 데이터 예측
        st.markdown("#### 🔮 새로운 학생 데이터로 예측해보기")
        
        col1, col2 = st.columns(2)
        with col1:
            new_study_time = st.slider("공부시간 (시간)", 0.0, 12.0, 6.0, 0.5)
        with col2:
            new_sleep_time = st.slider("수면시간 (시간)", 4.0, 10.0, 7.0, 0.5)
        
        if st.button("예측하기"):
            # 간단한 규칙 기반 예측 (실제로는 학습된 모델 사용)
            if new_study_time >= 6 and new_sleep_time >= 6:
                prediction = "합격"
                confidence = 85
                color = "green"
            elif new_study_time >= 4 and new_sleep_time >= 5:
                prediction = "합격"
                confidence = 65
                color = "orange"
            else:
                prediction = "불합격"
                confidence = 75
                color = "red"
            
            st.markdown(f"""
            <div style="background: {color}; color: white; padding: 1rem; border-radius: 10px; text-align: center;">
                <h3>예측 결과: {prediction}</h3>
                <p>신뢰도: {confidence}%</p>
            </div>
            """, unsafe_allow_html=True)
    
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
        
        # 모델 학습
        if st.button("🏠 부동산 가격 예측 모델 학습", type="primary"):
            with st.spinner("부동산 전문가 AI를 학습시키고 있습니다..."):
                # 데이터 준비
                X = df_reg[['평수', '건물연수']]
                y = df_reg['가격(만원)']
                
                # 학습/테스트 분할
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
                
                # 모델 학습
                model = LinearRegression()
                model.fit(X_train, y_train)
                
                # 예측 및 평가
                y_pred = model.predict(X_test)
                mse = mean_squared_error(y_test, y_pred)
                rmse = np.sqrt(mse)
                
                st.success(f"✅ 학습 완료! 평균 오차: ±{rmse:.0f}만원")
                
                # 결과 분석
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("평균 오차", f"±{rmse:.0f}만원")
                    st.metric("학습 데이터 수", len(X_train))
                    
                    # 계수 표시
                    st.markdown("**학습된 규칙:**")
                    st.write(f"• 평수 1평 증가 → +{model.coef_[0]:.0f}만원")
                    st.write(f"• 건물연수 1년 증가 → {model.coef_[1]:.0f}만원")
                
                with col2:
                    # 실제 vs 예측 비교
                    comparison_df = pd.DataFrame({
                        '실제가격': y_test,
                        '예측가격': y_pred
                    })
                    fig = px.scatter(comparison_df, x='실제가격', y='예측가격',
                                   title="실제 가격 vs 예측 가격")
                    fig.add_trace(go.Scatter(x=[y_test.min(), y_test.max()], 
                                           y=[y_test.min(), y_test.max()],
                                           mode='lines', name='완벽 예측선'))
                    st.plotly_chart(fig, use_container_width=True)
        
        # 새로운 집 가격 예측
        st.markdown("#### 🏠 새로운 집 가격 예측해보기")
        
        col1, col2 = st.columns(2)
        with col1:
            new_size = st.slider("평수", 30, 200, 100, 5)
        with col2:
            new_age = st.slider("건물 연수 (년)", 1, 30, 10, 1)
        
        if st.button("가격 예측하기"):
            # 간단한 규칙 기반 예측
            predicted_price = new_size * 50 - new_age * 10 + 2000
            predicted_price = max(1000, predicted_price)  # 최소 가격
            
            st.markdown(f"""
            <div style="background: #007bff; color: white; padding: 1rem; border-radius: 10px; text-align: center;">
                <h3>예측 가격: {predicted_price:,.0f}만원</h3>
                <p>{new_size}평, {new_age}년된 집</p>
            </div>
            """, unsafe_allow_html=True)
    
    # 학습 완료 처리
    if st.button("🎯 지도학습 완료", type="primary"):
        st.session_state.progress['supervised'] = True
        st.success("🎉 지도학습을 완료했습니다! 이제 비지도학습으로 넘어가세요.")
        st.balloons()

if __name__ == "__main__":
    main()
