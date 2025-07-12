import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from utils import *
from config import *

# 페이지 설정
st.set_page_config(
    page_title="SEP ME ver.6 - 학생 글 채점 연습",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .student-text {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 2rem;
        border-radius: 15px;
        border-left: 5px solid #007bff;
        margin: 1.5rem 0;
        font-size: 1.1rem;
        line-height: 1.8;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .grade-card {
        background: white;
        border: 2px solid #e9ecef;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        margin: 0.5rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .grade-card:hover {
        background: #007bff;
        color: white;
        transform: translateY(-3px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        text-align: center;
        border: 1px solid #e9ecef;
    }
    
    .progress-container {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .feedback-success {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border: 1px solid #c3e6cb;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .feedback-error {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border: 1px solid #f5c6cb;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def show_sidebar():
    """사이드바 표시"""
    st.sidebar.title("📊 진행 현황")
    
    # 관리자 모드 버튼 추가
    if st.sidebar.button("🔧 관리자 모드"):
        st.session_state.stage = 'admin'
        st.rerun()
    
    # 기존 코드...


def initialize_session_state():
    """세션 상태 초기화"""
    if 'stage' not in st.session_state:
        st.session_state.stage = 'intro'
        st.session_state.user_name = ''
        st.session_state.user_level = ''
        st.session_state.current_question = 1
        st.session_state.practice1_results = []
        st.session_state.practice2_results = []
        st.session_state.start_time = datetime.now()
        st.session_state.samples_p1 = []
        st.session_state.samples_p2 = []
        st.session_state.question_start_time = datetime.now()

def show_sidebar():
    """사이드바 표시"""
    st.sidebar.title("📊 진행 현황")
     # 관리자 모드 버튼 추가
    if st.sidebar.button("🔧 관리자 모드"):
        st.session_state.stage = 'admin'
        st.rerun()
        
    if st.session_state.user_name:
        st.sidebar.success(f"👋 {st.session_state.user_name}님")
        st.sidebar.info(f"📚 레벨: {st.session_state.user_level}")
        
        # 경과 시간
        elapsed = datetime.now() - st.session_state.start_time
        st.sidebar.metric("⏱️ 경과 시간", f"{elapsed.seconds // 60}분 {elapsed.seconds % 60}초")
    
    # 진행률 표시
    if st.session_state.stage == 'practice1':
        progress = (st.session_state.current_question - 1) / 15
        st.sidebar.progress(progress)
        st.sidebar.write(f"**연습1 진행률**: {st.session_state.current_question}/15")
        
        if st.session_state.practice1_results:
            correct_count = sum(1 for r in st.session_state.practice1_results if r['is_correct'])
            st.sidebar.metric("현재 정답률", f"{(correct_count/len(st.session_state.practice1_results)*100):.1f}%")
        
    elif st.session_state.stage == 'practice2':
        progress = (st.session_state.current_question - 1) / 15
        st.sidebar.progress(progress)
        st.sidebar.write(f"**연습2 진행률**: {st.session_state.current_question}/15")
        
        # 연습1 결과 요약
        if st.session_state.practice1_results:
            correct_count = sum(1 for r in st.session_state.practice1_results if r['is_correct'])
            accuracy = (correct_count / len(st.session_state.practice1_results)) * 100
            st.sidebar.metric("연습1 최종 정답률", f"{accuracy:.1f}%")
        
        if st.session_state.practice2_results:
            avg_accuracy = calculate_practice2_accuracy(st.session_state.practice2_results)
            st.sidebar.metric("연습2 현재 정확도", f"{avg_accuracy['overall']:.1f}%")
    
    # 도움말 및 가이드
    with st.sidebar.expander("❓ 사용 가이드"):
        st.markdown("""
        **📚 연습1 - 등급 추정**
        - 학생 글을 읽고 1~5등급 중 선택
        - 즉시 정답 여부와 피드백 제공
        
        **📊 연습2 - 점수 추정**
        - 내용/조직/표현 영역별 점수 입력
        - 각 영역별 상세 분석 제공
        
        **💡 팁**
        - 평가 기준을 숙지하고 시작하세요
        - 천천히 읽고 신중하게 판단하세요
        - 피드백을 통해 학습하세요
        """)
    
    # 리셋 버튼
    if st.sidebar.button("🔄 처음부터 다시 시작"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

def show_intro_page():
    """소개 페이지"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 👋 SEP ME에 오신 것을 환영합니다!")
        
        # 프로그램 소개
        st.markdown("""
        **SEP ME**는 학생 글 채점 능력 향상을 위한 AI 기반 학습 도구입니다.
        실제 학생들이 작성한 글을 바탕으로 채점 연습을 할 수 있습니다.
        """)
        
        # 사용자 정보 입력
        with st.form("user_info"):
            st.markdown("#### 📝 사용자 정보")
            name = st.text_input("이름을 입력해주세요:", placeholder="홍길동")
            level = st.selectbox(
                "현재 채점 경험 수준을 선택해주세요:",
                ["초급 (채점 경험 없음)", "중급 (1년 미만)", "고급 (1-3년)", "전문가 (3년 이상)"]
            )
            
            st.markdown("---")
            agreement = st.checkbox("개인정보 수집 및 이용에 동의합니다 (학습 목적)")
            
            submitted = st.form_submit_button("🚀 학습 시작하기", type="primary", use_container_width=True)
            
            if submitted:
                if not name:
                    st.error("이름을 입력해주세요.")
                elif not agreement:
                    st.error("개인정보 수집 및 이용에 동의해주세요.")
                else:
                    st.session_state.user_name = name
                    st.session_state.user_level = level
                    st.session_state.stage = 'practice1'
                    st.session_state.samples_p1 = load_samples('practice1')
                    st.session_state.samples_p2 = load_samples('practice2')
                    st.success("등록이 완료되었습니다! 잠시 후 연습이 시작됩니다.")
                    st.rerun()
    
    # 프로그램 구성 설명
    st.markdown("---")
    st.markdown("### 📚 학습 프로그램 구성")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
        <div class="metric-card">
            <h4>📖 연습1: 등급 추정</h4>
            <ul style="text-align: left;">
                <li>15개의 학생 글 제시</li>
                <li>1~5등급 중 선택</li>
                <li>즉시 피드백 제공</li>
                <li>등급별 특성 학습</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col_b:
        st.markdown("""
        <div class="metric-card">
            <h4>📊 연습2: 점수 추정</h4>
            <ul style="text-align: left;">
                <li>15개의 학생 글 제시</li>
                <li>내용/조직/표현 영역별 점수</li>
                <li>상세 분석 제공</li>
                <li>정확한 채점 기준 학습</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # 평가 기준 표시
    st.markdown("---")
    st.markdown("### 📋 평가 기준 및 과제")
    
    # 등급 기준표
    st.markdown("#### 🎯 등급 기준")
    grade_df = pd.DataFrame({
        '등급': ['1등급', '2등급', '3등급', '4등급', '5등급'],
        '점수 범위': ['29-33점', '27-28점', '24-26점', '20-23점', '13-19점'],
        '수준': ['매우 우수', '우수', '보통', '미흡', '매우 미흡']
    })
    st.table(grade_df)
    
    # 영역별 점수 기준
    st.markdown("#### 📝 영역별 점수 기준")
    score_df = pd.DataFrame({
        '영역': ['내용', '조직', '표현'],
        '점수 범위': ['3-18점', '2-12점', '2-12점'],
        '평가 요소': [
            '주제 적합성, 내용의 충실성, 독창성',
            '글의 구성, 단락 구성, 논리적 연결',
            '어휘 사용, 문장 표현, 맞춤법'
        ]
    })
    st.table(score_df)

def show_practice1_page():
    """연습1 페이지 - 등급 추정"""
    st.markdown("## 📚 연습1: 글의 등급 추정하기")
    
    # 진행률 표시
    progress = (st.session_state.current_question - 1) / 15
    st.markdown(f"""
    <div class="progress-container">
        <h4>진행 상황: {st.session_state.current_question}/15 문제</h4>
    </div>
    """, unsafe_allow_html=True)
    st.progress(progress)
    
    # 현재 문제 데이터 가져오기
    if st.session_state.samples_p1:
        current_sample = st.session_state.samples_p1[st.session_state.current_question - 1]
        
        # 학생 글 표시
        st.markdown("### 📖 학생 글")
        st.markdown(f"""
        <div class="student-text">
        <strong>문제 {st.session_state.current_question}번</strong><br><br>
        {current_sample['text']}
        </div>
        """, unsafe_allow_html=True)
        
        # 등급 선택
        st.markdown("### 🎯 이 글의 등급을 선택해주세요")
        
        # 등급 선택 버튼들
        cols = st.columns(5)
        grade_options = {
            1: "1등급\n(29-33점)",
            2: "2등급\n(27-28점)", 
            3: "3등급\n(24-26점)",
            4: "4등급\n(20-23점)",
            5: "5등급\n(13-19점)"
        }
        
        selected_grade = None
        for i, (grade, description) in enumerate(grade_options.items()):
            with cols[i]:
                if st.button(description, key=f"grade_{grade}_{st.session_state.current_question}", use_container_width=True):
                    selected_grade = grade
        
        # 등급이 선택되면 결과 처리
        if selected_grade:
            # 결과 저장
            is_correct = selected_grade == current_sample['correct_grade']
            result = {
                'question': st.session_state.current_question,
                'selected': selected_grade,
                'correct': current_sample['correct_grade'],
                'is_correct': is_correct,
                'timestamp': datetime.now(),
                'time_taken': (datetime.now() - st.session_state.question_start_time).seconds
            }
            
            # 중복 저장 방지
            if not any(r['question'] == st.session_state.current_question for r in st.session_state.practice1_results):
                st.session_state.practice1_results.append(result)
            
            # 피드백 표시
            st.markdown("---")
            if is_correct:
                st.markdown("""
                <div class="feedback-success">
                    <h4>🎉 정답입니다!</h4>
                    <p>훌륭한 판단력을 보여주셨습니다.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="feedback-error">
                    <h4>😔 아쉽지만 오답입니다</h4>
                    <p><strong>정답:</strong> {current_sample['correct_grade']}등급</p>
                    <p><strong>선택:</strong> {selected_grade}등급</p>
                </div>
                """, unsafe_allow_html=True)
                
                # 상세 피드백
                with st.expander("💡 상세 피드백 보기"):
                    st.write(get_detailed_feedback(current_sample, selected_grade))
            
            # 다음 문제로 이동
            st.markdown("---")
            col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
            
            with col_btn2:
                if st.session_state.current_question < 15:
                    if st.button("다음 문제 →", type="primary", use_container_width=True):
                        st.session_state.current_question += 1
                        st.session_state.question_start_time = datetime.now()
                        st.rerun()
                else:
                    if st.button("연습2로 이동 →", type="primary", use_container_width=True):
                        st.session_state.stage = 'practice2'
                        st.session_state.current_question = 1
                        st.session_state.question_start_time = datetime.now()
                        st.rerun()

def show_practice2_page():
    """연습2 페이지 - 점수 추정"""
    st.markdown("## 📊 연습2: 글의 점수 추정하기")
    
    # 진행률 표시
    progress = (st.session_state.current_question - 1) / 15
    st.markdown(f"""
    <div class="progress-container">
        <h4>진행 상황: {st.session_state.current_question}/15 문제</h4>
    </div>
    """, unsafe_allow_html=True)
    st.progress(progress)
    
    # 현재 문제 데이터 가져오기
    if st.session_state.samples_p2:
        current_sample = st.session_state.samples_p2[st.session_state.current_question - 1]
        
        # 학생 글 표시
        st.markdown("### 📖 학생 글")
        st.markdown(f"""
        <div class="student-text">
        <strong>문제 {st.session_state.current_question}번</strong><br><br>
        {current_sample['text']}
        </div>
        """, unsafe_allow_html=True)
        
        # 점수 입력
        st.markdown("### 🎯 영역별 점수를 입력해주세요")
        
        with st.form(f"score_form_{st.session_state.current_question}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**내용 영역 (3-18점)**")
                st.caption("주제 적합성, 내용의 충실성, 독창성")
                content_score = st.number_input(
                    "내용 점수",
                    min_value=3,
                    max_value=18,
                    value=10,
                    key=f"content_{st.session_state.current_question}",
                    label_visibility="collapsed"
                )
            
            with col2:
                st.markdown("**조직 영역 (2-12점)**")
                st.caption("글의 구성, 단락 구성, 논리적 연결")
                organization_score = st.number_input(
                    "조직 점수",
                    min_value=2,
                    max_value=12,
                    value=7,
                    key=f"organization_{st.session_state.current_question}",
                    label_visibility="collapsed"
                )
            
            with col3:
                st.markdown("**표현 영역 (2-12점)**")
                st.caption("어휘 사용, 문장 표현, 맞춤법")
                expression_score = st.number_input(
                    "표현 점수",
                    min_value=2,
                    max_value=12,
                    value=7,
                    key=f"expression_{st.session_state.current_question}",
                    label_visibility="collapsed"
                )
            
            total_score = content_score + organization_score + expression_score
            
            # 총점 및 등급 표시
            st.markdown("---")
            col_total1, col_total2, col_total3 = st.columns(3)
            with col_total2:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>총점: {total_score}점</h3>
                    <h4>예상 등급: {score_to_grade(total_score)}등급</h4>
                </div>
                """, unsafe_allow_html=True)
            
            # 제출 버튼
            submitted = st.form_submit_button("점수 제출하기", type="primary", use_container_width=True)
            
            if submitted:
                # 결과 저장
                correct_scores = current_sample['correct_scores']
                result = {
                    'question': st.session_state.current_question,
                    'content': content_score,
                    'organization': organization_score,
                    'expression': expression_score,
                    'total': total_score,
                    'correct_content': correct_scores['content'],
                    'correct_organization': correct_scores['organization'],
                    'correct_expression': correct_scores['expression'],
                    'correct_total': sum(correct_scores.values()),
                    'timestamp': datetime.now(),
                    'time_taken': (datetime.now() - st.session_state.question_start_time).seconds
                }
                
                # 중복 저장 방지
                if not any(r['question'] == st.session_state.current_question for r in st.session_state.practice2_results):
                    st.session_state.practice2_results.append(result)
                
                # 피드백 표시
                show_score_feedback(result)
                
                # 다음 문제로 이동
                st.markdown("---")
                col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
                
                with col_btn2:
                    if st.session_state.current_question < 15:
                        if st.button("다음 문제 →", type="primary", use_container_width=True):
                            st.session_state.current_question += 1
                            st.session_state.question_start_time = datetime.now()
                            st.rerun()
                    else:
                        if st.button("결과 보기 →", type="primary", use_container_width=True):
                            st.session_state.stage = 'results'
                            st.rerun()

def show_results_page():
    """결과 페이지"""
    st.markdown("## 🎉 학습 완료!")
    st.balloons()
    
    # 완료 메시지
    total_time = datetime.now() - st.session_state.start_time
    st.success(f"🎊 {st.session_state.user_name}님, 모든 연습을 완료하셨습니다! (소요시간: {total_time.seconds // 60}분)")
    
    # 전체 결과 요약
    st.markdown("### 📊 종합 결과")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # 연습1 결과
    if st.session_state.practice1_results:
        p1_correct = sum(1 for r in st.session_state.practice1_results if r['is_correct'])
        p1_accuracy = (p1_correct / len(st.session_state.practice1_results)) * 100
        
        with col1:
            st.metric("연습1 정답률", f"{p1_accuracy:.1f}%", f"{p1_correct}/15")
    
    # 연습2 결과
    if st.session_state.practice2_results:
        p2_scores = calculate_practice2_accuracy(st.session_state.practice2_results)
        
        with col2:
            st.metric("연습2 정확도", f"{p2_scores['overall']:.1f}%")
        with col3:
            st.metric("평균 오차", f"{p2_scores['avg_error']:.1f}점")
    
    # 전체 성과
    with col4:
        if st.session_state.practice1_results and st.session_state.practice2_results:
            overall_score = (p1_accuracy + p2_scores['overall']) / 2
            st.metric("종합 점수", f"{overall_score:.1f}점")
    
    # 상세 분석 탭
    st.markdown("---")
    tab1, tab2, tab3, tab4 = st.tabs(["📈 연습1 분석", "📊 연습2 분석", "🎯 종합 분석", "📋 상세 결과"])
    
    with tab1:
        show_practice1_analysis()
    
    with tab2:
        show_practice2_analysis()
    
    with tab3:
        show_comprehensive_analysis()
    
    with tab4:
        show_detailed_results()
    
    # 액션 버튼들
    st.markdown("---")
    col_action1, col_action2, col_action3 = st.columns(3)
    
    with col_action1:
        if st.button("📊 결과 다운로드", use_container_width=True):
            csv_data = create_results_csv()
            st.download_button(
                label="CSV 파일 다운로드",
                data=csv_data,
                file_name=f"sep_results_{st.session_state.user_name}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    with col_action2:
        if st.button("🔄 다시 도전하기", use_container_width=True):
            # 결과는 유지하고 연습만 다시 시작
            st.session_state.stage = 'practice1'
            st.session_state.current_question = 1
            st.session_state.practice1_results = []
            st.session_state.practice2_results = []
            st.session_state.start_time = datetime.now()
            st.session_state.samples_p1 = load_samples('practice1')
            st.session_state.samples_p2 = load_samples('practice2')
            st.rerun()
    
    with col_action3:
        if st.button("🏠 처음으로", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
            
def show_admin_page():
    """관리자 데이터 관리 페이지"""
    st.title("📊 관리자 - 학생 글 데이터 관리")
    
    # 뒤로가기 버튼
    if st.button("← 메인으로 돌아가기"):
        st.session_state.stage = 'intro'
        st.rerun()
    
    st.markdown("---")
    
    # 비밀번호 확인
    password = st.text_input("관리자 비밀번호", type="password")
    
    if password == "admin123":  # 간단한 비밀번호
        st.success("관리자 로그인 성공!")
        
        # 파일 업로드 섹션
        st.markdown("### 📁 학생 글 데이터 업로드")
        
        uploaded_file = st.file_uploader(
            "CSV 파일을 업로드하세요",
            type=['csv'],
            help="학생 글 데이터가 포함된 CSV 파일을 선택하세요"
        )
        
        if uploaded_file is not None:
            # 업로드된 파일 미리보기
            df = pd.read_csv(uploaded_file)
            st.write("**업로드된 데이터 미리보기:**")
            st.dataframe(df.head())
            
            # 데이터 검증
            required_columns = ['id', 'text', 'correct_grade', 'content_score', 'organization_score', 'expression_score']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                st.error(f"필수 컬럼이 누락되었습니다: {missing_columns}")
                st.info("필요한 컬럼: id, text, correct_grade, content_score, organization_score, expression_score")
            else:
                st.success("✅ 데이터 형식이 올바릅니다!")
                
                if st.button("데이터 저장", type="primary"):
                    # 세션 상태에 데이터 저장
                    st.session_state.uploaded_data = df.to_dict('records')
                    st.success(f"✅ {len(df)}개의 학생 글 데이터가 저장되었습니다!")
                    
        # 현재 저장된 데이터 확인
        if 'uploaded_data' in st.session_state:
            st.markdown("### 📋 현재 저장된 데이터")
            st.write(f"총 {len(st.session_state.uploaded_data)}개의 학생 글이 저장되어 있습니다.")
            
            if st.button("저장된 데이터 초기화"):
                del st.session_state.uploaded_data
                st.success("데이터가 초기화되었습니다.")
                st.rerun()
    
    elif password:
        st.error("비밀번호가 틀렸습니다.")


if __name__ == "__main__":
    main()
        main()
