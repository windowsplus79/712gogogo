import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="비지도학습", page_icon="🔍", layout="wide")

# CSS 스타일
st.markdown("""
<style>
    .concept-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
    }
    .practice-box {
        background: #f8f9fa;
        border: 2px solid #dc3545;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .cluster-box {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
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

def explain_clustering():
    """클러스터링 개념 설명"""
    st.markdown("""
    <div class="concept-box">
        <h2>🔍 비지도학습이란?</h2>
        <p><strong>정답이 없는 데이터</strong>에서 숨겨진 패턴을 찾는 방법입니다.</p>
        <p>마치 탐정이 단서들을 보고 사건의 진실을 추리하는 것과 같아요!</p>
    </div>
    """, unsafe_allow_html=True)

def main():
    init_session_state()
    
    # 학생 정보 확인
    if not (st.session_state.student_info.get('name') and st.session_state.student_info.get('id')):
        st.warning("먼저 메인 페이지에서 학생 정보를 입력해주세요!")
        if st.button("메인 페이지로 이동"):
            st.switch_page("main.py")
        return
    
    # 페이지 헤더
    st.markdown("# 🔍 비지도학습 (Unsupervised Learning)")
    st.markdown(f"**학습자**: {st.session_state.student_info['name']} ({st.session_state.student_info['id']})")
    
    # 탭 구성
    tab1, tab2, tab3 = st.tabs(["📚 개념 학습", "👥 고객 세분화 실습", "🎨 데이터 시각화"])
    
    with tab1:
        explain_clustering()
        
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
        
        # 클러스터링 시각적 설명
        st.markdown("### 📊 클러스터링 과정")
        
        # 예시 데이터 생성
        np.random.seed(42)
        cluster1 = np.random.multivariate_normal([2, 2], [[0.5, 0], [0, 0.5]], 50)
        cluster2 = np.random.multivariate_normal([6, 6], [[0.5, 0], [0, 0.5]], 50)
        cluster3 = np.random.multivariate_normal([2, 6], [[0.5, 0], [0, 0.5]], 50)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 클러스터링 전
            fig1 = go.Figure()
            all_points = np.vstack([cluster1, cluster2, cluster3])
            fig1.add_trace(go.Scatter(
                x=all_points[:, 0], y=all_points[:, 1],
                mode='markers',
                marker=dict(color='gray', size=8),
                name='원본 데이터'
            ))
            fig1.update_layout(title="🔍 클러스터링 전: 어떤 그룹이 있을까?")
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # 클러스터링 후
            fig2 = go.Figure()
            colors = ['red', 'blue', 'green']
            clusters = [cluster1, cluster2, cluster3]
            for i, (cluster, color) in enumerate(zip(clusters, colors)):
                fig2.add_trace(go.Scatter(
                    x=cluster[:, 0], y=cluster[:, 1],
                    mode='markers',
                    marker=dict(color=color, size=8),
                    name=f'그룹 {i+1}'
                ))
            fig2.update_layout(title="✨ 클러스터링 후: 3개 그룹 발견!")
            st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown("""
        ### 🎯 비지도학습의 장점
        - **새로운 발견**: 예상하지 못한 패턴 발견 가능
        - **비용 효율적**: 정답 라벨링 작업 불필요
        - **탐색적 분석**: 데이터의 전체적인 구조 파악
        
        ### ⚠️ 주의할 점
        - **해석의 어려움**: 발견된 패턴의 의미 파악 필요
        - **결과 검증**: 도메인 전문가의 검토 필요
        - **파라미터 설정**: 적절한 클러스터 수 결정 중요
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
        
        # 데이터 탐색
        st.markdown("#### 🔍 데이터 탐색")
        
        selected_features = st.multiselect(
            "분석할 특성을 선택하세요:",
            ['나이', '연소득(만원)', '온라인구매점수'],
            default=['나이', '연소득(만원)']
        )
        
        if len(selected_features) >= 2:
            # 산점도로 데이터 분포 확인
            fig = px.scatter(df_customers, 
                           x=selected_features[0], 
                           y=selected_features[1],
                           title=f"{selected_features[0]} vs {selected_features[1]}",
                           hover_data=['고객ID'])
            st.plotly_chart(fig, use_container_width=True)
            
            # 클러스터 수 선택
            st.markdown("#### 🎯 클러스터링 실행")
            n_clusters = st.slider("몇 개의 고객 그룹으로 나누고 싶나요?", 2, 6, 3)
            
            if st.button("🔍 고객 그룹 찾기", type="primary"):
                with st.spinner("AI가 고객 그룹을 찾고 있습니다..."):
                    # 데이터 전처리
                    X = df_customers[selected_features].values
                    scaler = StandardScaler()
                    X_scaled = scaler.fit_transform(X)
                    
                    # K-means 클러스터링
                    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
                    clusters = kmeans.fit_predict(X_scaled)
                    
                    # 결과를 데이터프레임에 추가
                    df_result = df_customers.copy()
                    df_result['고객그룹'] = [f'그룹 {i+1}' for i in clusters]
                    
                    st.success(f"✅ {n_clusters}개의 고객 그룹을 발견했습니다!")
                    
                    # 클러스터링 결과 시각화
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # 클러스터별 산점도
                        fig = px.scatter(df_result, 
                                       x=selected_features[0], 
                                       y=selected_features[1],
                                       color='고객그룹',
                                       title="고객 그룹 분류 결과",
                                       hover_data=['고객ID'])
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        # 그룹별 고객 수
                        group_counts = df_result['고객그룹'].value_counts()
                        fig = px.pie(values=group_counts.values, 
                                   names=group_counts.index,
                                   title="그룹별 고객 수")
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # 그룹별 특성 분석
                    st.markdown("#### 📈 발견된 고객 그룹 특성")
                    
                    group_analysis = df_result.groupby('고객그룹')[['나이', '연소득(만원)', '온라인구매점수']].mean().round(1)
                    
                    for group in group_analysis.index:
                        group_data = group_analysis.loc[group]
                        group_count = (df_result['고객그룹'] == group).sum()
                        
                        # 그룹 특성 해석
                        if group_data['나이'] < 35:
                            age_desc = "젊은 층"
                        elif group_data['나이'] < 50:
                            age_desc = "중년 층"
                        else:
                            age_desc = "고령 층"
                        
                        if group_data['연소득(만원)'] < 4000:
                            income_desc = "저소득"
                        elif group_data['연소득(만원)'] < 7000:
                            income_desc = "중소득"
                        else:
                            income_desc = "고소득"
                        
                        if group_data['온라인구매점수'] > 70:
                            online_desc = "온라인 쇼핑 선호"
                        elif group_data['온라인구매점수'] > 40:
                            online_desc = "온오프라인 균형"
                        else:
                            online_desc = "오프라인 쇼핑 선호"
                        
                        st.markdown(f"""
                        <div class="cluster-box">
                            <h4>👥 {group} ({group_count}명)</h4>
                            <p><strong>특징:</strong> {age_desc} · {income_desc} · {online_desc}</p>
                            <p><strong>평균 나이:</strong> {group_data['나이']:.0f}세 | 
                               <strong>평균 소득:</strong> {group_data['연소득(만원)']:,.0f}만원 | 
                               <strong>온라인 점수:</strong> {group_data['온라인구매점수']:.0f}점</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # 마케팅 전략 제안
                    st.markdown("#### 💡 마케팅 전략 제안")
                    st.info("""
                    **발견된 고객 그룹별 맞춤 전략:**
                    
                    🎯 **젊은 고소득층**: 프리미엄 온라인 상품, SNS 마케팅, 최신 트렌드 상품
                    
                    🏪 **중년 중소득층**: 실용적 상품, 오프라인 매장 이벤트, 가족 대상 상품
                    
                    💎 **고령 고소득층**: 프리미엄 서비스, 개인 맞춤 상담, 품질 중심 마케팅
                    """)
                    
                    # 상세 결과 다운로드
                    if st.button("📊 상세 결과 보기"):
                        st.dataframe(df_result, use_container_width=True)
    
    with tab3:
        st.markdown("""
        <div class="practice-box">
            <h3>🎨 다양한 데이터 시각화</h3>
            <p>비지도학습 결과를 다양한 방법으로 시각화해보세요!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 시각화할 데이터 생성
        df_viz = generate_customer_data()
        
        # 간단한 클러스터링 수행
        X = df_viz[['나이', '연소득(만원)', '온라인구매점수']].values
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        kmeans = KMeans(n_clusters=3, random_state=42)
        df_viz['그룹'] = kmeans.fit_predict(X_scaled)
        df_viz['그룹명'] = [f'그룹 {i+1}' for i in df_viz['그룹']]
        
        viz_type = st.selectbox(
            "시각화 방법을 선택하세요:",
            ["3D 산점도", "박스 플롯", "히트맵", "바이올린 플롯"]
        )
        
        if viz_type == "3D 산점도":
            fig = px.scatter_3d(df_viz, 
                              x='나이', y='연소득(만원)', z='온라인구매점수',
                              color='그룹명',
                              title="고객 데이터 3D 시각화")
            st.plotly_chart(fig, use_container_width=True)
            
        elif viz_type == "박스 플롯":
            feature = st.selectbox("분석할 특성:", ['나이', '연소득(만원)', '온라인구매점수'])
            fig = px.box(df_viz, x='그룹명', y=feature, 
                        title=f"그룹별 {feature} 분포")
            st.plotly_chart(fig, use_container_width=True)
            
        elif viz_type == "히트맵":
            # 그룹별 평균값 계산
            heatmap_data = df_viz.groupby('그룹명')[['나이', '연소득(만원)', '온라인구매점수']].mean()
            
            fig = px.imshow(heatmap_data.T, 
                          text_auto=True,
                          title="그룹별 특성 히트맵",
                          color_continuous_scale="RdYlBu")
            st.plotly_chart(fig, use_container_width=True)
            
        elif viz_type == "바이올린 플롯":
            feature = st.selectbox("분석할 특성:", ['나이', '연소득(만원)', '온라인구매점수'])
            fig = px.violin(df_viz, x='그룹명', y=feature,
                          title=f"그룹별 {feature} 분포 (바이올린 플롯)")
            st.plotly_chart(fig, use_container_width=True)
        
        # 인사이트 설명
        st.markdown("#### 💡 시각화에서 발견할 수 있는 것들")
        st.info("""
        - **3D 산점도**: 데이터의 전체적인 분포와 클러스터 경계
        - **박스 플롯**: 각 그룹의 중간값, 사분위수, 이상치
        - **히트맵**: 그룹 간 특성 차이를 색상으로 직관적 파악
        - **바이올린 플롯**: 데이터 분포의 모양과 밀도
        """)
    
    # 학습 완료 처리
    if st.button("🔍 비지도학습 완료", type="primary"):
        st.session_state.progress['unsupervised'] = True
        st.success("🎉 비지도학습을 완료했습니다! 이제 형성평가를 받아보세요.")
        st.balloons()

if __name__ == "__main__":
    main()
