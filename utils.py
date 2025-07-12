import pandas as pd
import numpy as np
import random
from datetime import datetime
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def load_samples(practice_type):
    """샘플 데이터 로드 - 실제 구현에서는 CSV 파일에서 로드"""
    if practice_type == 'practice1':
        # 연습1용 샘플 데이터 (실제로는 CSV에서 로드)
        sample_texts = [
            "환경 보호는 우리 모두의 책임입니다. 지구 온난화로 인해 빙하가 녹고 있고, 해수면이 상승하고 있습니다. 우리는 일회용품 사용을 줄이고, 재활용을 실천해야 합니다. 또한 대중교통을 이용하고, 에너지를 절약해야 합니다. 작은 실천이 모여 큰 변화를 만들 수 있습니다.",
            "독서는 인생을 풍요롭게 만드는 활동입니다. 책을 통해 다양한 지식을 얻을 수 있고, 상상력을 기를 수 있습니다. 또한 독서는 스트레스를 해소하고 집중력을 향상시킵니다. 하루에 조금씩이라도 책을 읽는 습관을 기르는 것이 중요합니다.",
            "스마트폰의 과도한 사용은 여러 문제를 야기합니다. 목과 어깨 통증, 시력 저하, 수면 장애 등이 대표적입니다. 또한 대면 소통 능력이 떨어지고 집중력이 저하됩니다. 스마트폰 사용 시간을 제한하고 규칙적인 휴식을 취해야 합니다.",
        ]
        
        samples = []
        for i in range(15):
            text_idx = i % len(sample_texts)
            sample = {
                'id': i + 1,
                'text': sample_texts[text_idx] + f" (문제 {i+1}번 변형)",
                'correct_grade': random.randint(1, 5)
            }
            samples.append(sample)
        return samples
    
    elif practice_type == 'practice2':
        # 연습2용 샘플 데이터
        sample_texts = [
            "교육의 중요성에 대해 논하시오. 교육은 개인의 성장과 사회 발전의 기초가 됩니다. 올바른 교육을 통해 인격을 형성하고 지식을 습득할 수 있습니다. 또한 교육은 사회적 불평등을 해소하고 민주주의를 발전시키는 역할을 합니다.",
            "현대 사회에서 기술의 역할은 매우 중요합니다. 인공지능, 빅데이터, 사물인터넷 등의 기술이 우리 생활을 편리하게 만들고 있습니다. 하지만 기술 발전에 따른 부작용도 고려해야 합니다. 일자리 감소, 개인정보 보호 문제 등이 대표적입니다.",
            "건강한 생활습관의 중요성을 강조하고 싶습니다. 규칙적인 운동과 균형 잡힌 식사는 건강의 기본입니다. 또한 충분한 수면과 스트레스 관리도 중요합니다. 건강한 몸과 마음을 유지하기 위해 꾸준한 노력이 필요합니다.",
        ]
        
        samples = []
        for i in range(15):
            text_idx = i % len(sample_texts)
            sample = {
                'id': i + 1,
                'text': sample_texts[text_idx] + f" (문제 {i+1}번 변형)",
                'correct_scores': {
                    'content': random.randint(8, 16),
                    'organization': random.randint(4, 10),
                    'expression': random.randint(4, 10)
                }
            }
            samples.append(sample)
        return samples

def score_to_grade(total_score):
    """총점을 등급으로 변환"""
    if total_score >= 29:
        return 1
    elif total_score >= 27:
        return 2
    elif total_score >= 24:
        return 3
    elif total_score >= 20:
        return 4
    else:
        return 5

def get_detailed_feedback(sample, selected_grade):
    """상세 피드백 생성"""
    correct_grade = sample['correct_grade']
    
    feedback = f"""
    **정답 등급**: {correct_grade}등급
    **선택 등급**: {selected_grade}등급
    
    **분석**:
    """
    
    if selected_grade > correct_grade:
        feedback += "선택하신 등급이 실제보다 낮습니다. 글의 장점을 더 주의깊게 살펴보세요."
    elif selected_grade < correct_grade:
        feedback += "선택하신 등급이 실제보다 높습니다. 글의 부족한 부분을 더 면밀히 검토해보세요."
    
    feedback += f"""
    
    **{correct_grade}등급 특징**:
    - 내용: {'매우 충실' if correct_grade <= 2 else '보통' if correct_grade <= 3 else '부족'}
    - 조직: {'매우 체계적' if correct_grade <= 2 else '체계적' if correct_grade <= 3 else '미흡'}
    - 표현: {'매우 정확' if correct_grade <= 2 else '적절' if correct_grade <= 3 else '부정확'}
    """
    
    return feedback

def show_score_feedback(result):
    """점수 피드백 표시"""
    content_diff = result['content'] - result['correct_content']
    org_diff = result['organization'] - result['correct_organization']
    exp_diff = result['expression'] - result['correct_expression']
    total_diff = result['total'] - result['correct_total']
    
    st.markdown("### 📊 채점 결과 분석")
    
    # 점수 비교 표시
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "내용 영역",
            f"{result['content']}점",
            f"{content_diff:+d}점",
            delta_color="normal"
        )
        st.caption(f"정답: {result['correct_content']}점")
    
    with col2:
        st.metric(
            "조직 영역", 
            f"{result['organization']}점",
            f"{org_diff:+d}점",
            delta_color="normal"
        )
        st.caption(f"정답: {result['correct_organization']}점")
    
    with col3:
        st.metric(
            "표현 영역",
            f"{result['expression']}점", 
            f"{exp_diff:+d}점",
            delta_color="normal"
        )
        st.caption(f"정답: {result['correct_expression']}점")
    
    with col4:
        st.metric(
            "총점",
            f"{result['total']}점",
            f"{total_diff:+d}점",
            delta_color="normal"
        )
        st.caption(f"정답: {result['correct_total']}점")
    
    # 정확도 평가
    abs_total_diff = abs(total_diff)
    if abs_total_diff <= 2:
        st.success("🎉 매우 정확한 채점입니다! 훌륭한 평가 능력을 보여주셨습니다.")
    elif abs_total_diff <= 5:
        st.info("👍 양호한 채점입니다. 조금 더 세밀한 관찰이 필요합니다.")
    else:
        st.warning("💡 채점 기준을 다시 검토해보세요. 각 영역별 특성을 더 자세히 살펴보시기 바랍니다.")
    
    # 영역별 상세 분석
    with st.expander("📋 영역별 상세 분석"):
        if abs(content_diff) > 2:
            st.write(f"**내용 영역**: {abs(content_diff)}점 차이가 있습니다. 주제 적합성과 내용의 충실성을 더 면밀히 검토해보세요.")
        
        if abs(org_diff) > 2:
            st.write(f"**조직 영역**: {abs(org_diff)}점 차이가 있습니다. 글의 구성과 단락 간 연결성을 더 자세히 살펴보세요.")
        
        if abs(exp_diff) > 2:
            st.write(f"**표현 영역**: {abs(exp_diff)}점 차이가 있습니다. 어휘 사용과 문장 표현의 적절성을 다시 확인해보세요.")

def calculate_practice2_accuracy(results):
    """연습2 정확도 계산"""
    if not results:
        return {'overall': 0, 'avg_error': 0, 'content_accuracy': 0, 'organization_accuracy': 0, 'expression_accuracy': 0}
    
    total_errors = []
    content_errors = []
    org_errors = []
    exp_errors = []
    
    for result in results:
        total_error = abs(result['total'] - result['correct_total'])
        content_error = abs(result['content'] - result['correct_content'])
        org_error = abs(result['organization'] - result['correct_organization'])
        exp_error = abs(result['expression'] - result['correct_expression'])
        
        total_errors.append(total_error)
        content_errors.append(content_error)
        org_errors.append(org_error)
        exp_errors.append(exp_error)
    
    return {
        'overall': max(0, 100 - np.mean(total_errors) * 8),
        'avg_error': np.mean(total_errors),
        'content_accuracy': max(0, 100 - np.mean(content_errors) * 12),
        'organization_accuracy': max(0, 100 - np.mean(org_errors) * 15),
        'expression_accuracy': max(0, 100 - np.mean(exp_errors) * 15)
    }

def show_practice1_analysis():
    """연습1 분석 표시"""
    if not st.session_state.practice1_results:
        st.info("연습1 결과가 없습니다.")
        return
    
    results_df = pd.DataFrame(st.session_state.practice1_results)
    
    # 전체 정답률
    total_correct = results_df['is_correct'].sum()
    total_questions = len(results_df)
    accuracy = (total_correct / total_questions) * 100
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("전체 정답률", f"{accuracy:.1f}%", f"{total_correct}/{total_questions}")
    
    with col2:
        avg_time = results_df['time_taken'].mean()
        st.metric("평균 소요시간", f"{avg_time:.1f}초")
    
    # 등급별 정답률 차트
    st.markdown("#### 등급별 정답률")
    grade_stats = []
    for grade in range(1, 6):
        grade_results = results_df[results_df['correct'] == grade]
        if len(grade_results) > 0:
            grade_accuracy = (grade_results['is_correct'].sum() / len(grade_results)) * 100
            grade_stats.append({
                '등급': f"{grade}등급",
                '정답률': grade_accuracy,
                '문제수': len(grade_results)
            })
    
    if grade_stats:
        grade_df = pd.DataFrame(grade_stats)
        fig = px.bar(grade_df, x='등급', y='정답률', 
                     title="등급별 정답률", 
                     color='정답률',
                     color_continuous_scale='RdYlGn')
        st.plotly_chart(fig, use_container_width=True)
    
    # 상세 결과 테이블
    st.markdown("#### 상세 결과")
    display_df = results_df[['question', 'selected', 'correct', 'is_correct', 'time_taken']].copy()
    display_df.columns = ['문제번호', '선택등급', '정답등급', '정답여부', '소요시간(초)']
    display_df['정답여부'] = display_df['정답여부'].map({True: '✅', False: '❌'})
    st.dataframe(display_df, use_container_width=True)

def show_practice2_analysis():
    """연습2 분석 표시"""
    if not st.session_state.practice2_results:
        st.info("연습2 결과가 없습니다.")
        return
    
    results_df = pd.DataFrame(st.session_state.practice2_results)
    accuracy_data = calculate_practice2_accuracy(st.session_state.practice2_results)
    
    # 전체 정확도
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("전체 정확도", f"{accuracy_data['overall']:.1f}%")
    with col2:
        st.metric("평균 오차", f"{accuracy_data['avg_error']:.1f}점")
    with col3:
        avg_time = results_df['time_taken'].mean()
        st.metric("평균 소요시간", f"{avg_time:.1f}초")
    
    # 영역별 정확도
    st.markdown("#### 영역별 정확도")
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        st.metric("내용 영역", f"{accuracy_data['content_accuracy']:.1f}%")
    with col_b:
        st.metric("조직 영역", f"{accuracy_data['organization_accuracy']:.1f}%")
    with col_c:
        st.metric("표현 영역", f"{accuracy_data['expression_accuracy']:.1f}%")
    
    # 점수 분포 차트
    st.markdown("#### 점수 분포 분석")
    
    # 실제 점수 vs 예측 점수 비교
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=list(range(1, len(results_df) + 1)),
        y=[r['correct_total'] for r in st.session_state.practice2_results],
        mode='lines+markers',
        name='정답 점수',
        line=dict(color='blue')
    ))
    
    fig.add_trace(go.Scatter(
        x=list(range(1, len(results_df) + 1)),
        y=[r['total'] for r in st.session_state.practice2_results],
        mode='lines+markers',
        name='예측 점수',
        line=dict(color='red')
    ))
    
    fig.update_layout(
        title="문제별 점수 비교",
        xaxis_title="문제 번호",
        yaxis_title="점수",
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 상세 결과 테이블
    st.markdown("#### 상세 결과")
    display_df = results_df[['question', 'content', 'organization', 'expression', 'total', 'correct_total', 'time_taken']].copy()
    display_df.columns = ['문제번호', '내용점수', '조직점수', '표현점수', '총점', '정답총점', '소요시간(초)']
    display_df['점수차이'] = display_df['총점'] - display_df['정답총점']
    st.dataframe(display_df, use_container_width=True)

def show_comprehensive_analysis():
    """종합 분석 표시"""
    st.markdown("### 🎯 종합 학습 성과 분석")
    
    if not st.session_state.practice1_results or not st.session_state.practice2_results:
        st.warning("모든 연습을 완료해야 종합 분석을 볼 수 있습니다.")
        return
    
    # 전체 성과 계산
    p1_accuracy = (sum(1 for r in st.session_state.practice1_results if r['is_correct']) / 15) * 100
    p2_accuracy = calculate_practice2_accuracy(st.session_state.practice2_results)['overall']
    overall_score = (p1_accuracy + p2_accuracy) / 2
    
    # 성과 등급 결정
    if overall_score >= 85:
        grade = "A+"
        comment = "🏆 탁월한 채점 능력을 보여주셨습니다!"
        color = "success"
    elif overall_score >= 75:
        grade = "A"
        comment = "🎉 우수한 채점 능력을 보여주셨습니다!"
        color = "success"
    elif overall_score >= 65:
        grade = "B+"
        comment = "👍 양호한 채점 능력을 보여주셨습니다."
        color = "info"
    elif overall_score >= 55:
        grade = "B"
        comment = "📚 더 많은 연습이 필요합니다."
        color = "warning"
    else:
        grade = "C"
        comment = "💪 기초부터 차근차근 학습해보세요."
        color = "warning"
    
    # 성과 표시
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if color == "success":
            st.success(f"**종합 등급: {grade}** ({overall_score:.1f}점)\n\n{comment}")
        elif color == "info":
            st.info(f"**종합 등급: {grade}** ({overall_score:.1f}점)\n\n{comment}")
        else:
            st.warning(f"**종합 등급: {grade}** ({overall_score:.1f}점)\n\n{comment}")
    
    # 상세 분석
    st.markdown("#### 📊 상세 성과 분석")
    
    # 레이더 차트 데이터 준비
    categories = ['등급 판단', '내용 평가', '조직 평가', '표현 평가', '일관성']
    
    p2_scores = calculate_practice2_accuracy(st.session_state.practice2_results)
    
    values = [
        p1_accuracy,
        p2_scores['content_accuracy'],
        p2_scores['organization_accuracy'],
        p2_scores['expression_accuracy'],
        (p1_accuracy + p2_accuracy) / 2  # 일관성 점수
    ]
    
    # 레이더 차트 생성
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='현재 성과',
        line_color='rgb(1,90,200)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="채점 능력 분석"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 개선 제안
    st.markdown("#### 💡 개선 제안")
    
    suggestions = []
    
    if p1_accuracy < 70:
        suggestions.append("**등급 판단 능력 향상**: 등급별 특성을 더 명확히 구분하는 연습이 필요합니다.")
    
    if p2_scores['content_accuracy'] < 70:
        suggestions.append("**내용 평가 능력 향상**: 주제 적합성과 내용의 충실성 평가 기준을 재검토하세요.")
    
    if p2_scores['organization_accuracy'] < 70:
        suggestions.append("**조직 평가 능력 향상**: 글의 구성과 논리적 연결성 평가에 더 주의를 기울이세요.")
    
    if p2_scores['expression_accuracy'] < 70:
        suggestions.append("**표현 평가 능력 향상**: 어휘 사용과 문장 표현의 적절성 판단 연습이 필요합니다.")
    
    if abs(p1_accuracy - p2_accuracy) > 15:
        suggestions.append("**일관성 향상**: 등급 판단과 점수 평가 간의 일관성을 높이는 연습이 필요합니다.")
    
    if suggestions:
        for i, suggestion in enumerate(suggestions, 1):
            st.write(f"{i}. {suggestion}")
    else:
        st.success("🎉 모든 영역에서 균형 잡힌 우수한 성과를 보이고 있습니다!")
    
    # 학습 권장사항
    st.markdown("#### 📚 추천 학습 방향")
    
    if overall_score >= 80:
        st.info("""
        **고급 학습자를 위한 권장사항:**
        - 다양한 장르의 글 채점 연습
        - 채점 기준의 세부 항목 숙지
        - 동료 채점자와의 비교 분석
        """)
    elif overall_score >= 60:
        st.info("""
        **중급 학습자를 위한 권장사항:**
        - 채점 기준표 반복 학습
        - 우수 답안과 미흡 답안 비교 분석
        - 영역별 집중 연습
        """)
    else:
        st.info("""
        **초급 학습자를 위한 권장사항:**
        - 기본 채점 기준 숙지
        - 단계별 체계적 학습
        - 충분한 연습 시간 확보
        """)

def show_detailed_results():
    """상세 결과 표시"""
    st.markdown("### 📋 전체 상세 결과")
    
    # 연습1 상세 결과
    if st.session_state.practice1_results:
        st.markdown("#### 📚 연습1 상세 결과")
        p1_df = pd.DataFrame(st.session_state.practice1_results)
        p1_display = p1_df[['question', 'selected', 'correct', 'is_correct', 'time_taken']].copy()
        p1_display.columns = ['문제번호', '선택등급', '정답등급', '정답여부', '소요시간(초)']
        p1_display['정답여부'] = p1_display['정답여부'].map({True: '✅ 정답', False: '❌ 오답'})
        st.dataframe(p1_display, use_container_width=True)
    
    # 연습2 상세 결과
    if st.session_state.practice2_results:
        st.markdown("#### 📊 연습2 상세 결과")
        p2_df = pd.DataFrame(st.session_state.practice2_results)
        p2_display = p2_df[['question', 'content', 'organization', 'expression', 'total', 
                           'correct_content', 'correct_organization', 'correct_expression', 'correct_total', 'time_taken']].copy()
        p2_display.columns = ['문제번호', '내용점수', '조직점수', '표현점수', '총점', 
                             '정답내용', '정답조직', '정답표현', '정답총점', '소요시간(초)']
        
        # 차이 계산
        p2_display['내용차이'] = p2_display['내용점수'] - p2_display['정답내용']
        p2_display['조직차이'] = p2_display['조직점수'] - p2_display['정답조직']
        p2_display['표현차이'] = p2_display['표현점수'] - p2_display['정답표현']
        p2_display['총점차이'] = p2_display['총점'] - p2_display['정답총점']
        
        st.dataframe(p2_display, use_container_width=True)

def create_results_csv():
    """결과를 CSV 형태로 생성"""
    # 기본 정보
    basic_info = {
        'user_name': st.session_state.user_name,
        'user_level': st.session_state.user_level,
        'completion_time': datetime.now().isoformat(),
        'total_time_minutes': (datetime.now() - st.session_state.start_time).seconds // 60
    }
    
    # 연습1 결과 요약
    if st.session_state.practice1_results:
        p1_correct = sum(1 for r in st.session_state.practice1_results if r['is_correct'])
        basic_info['practice1_accuracy'] = (p1_correct / 15) * 100
        basic_info['practice1_correct_count'] = p1_correct
    
    # 연습2 결과 요약
    if st.session_state.practice2_results:
        p2_scores = calculate_practice2_accuracy(st.session_state.practice2_results)
        basic_info['practice2_accuracy'] = p2_scores['overall']
        basic_info['practice2_avg_error'] = p2_scores['avg_error']
    
    # 종합 점수
    if st.session_state.practice1_results and st.session_state.practice2_results:
        basic_info['overall_score'] = (basic_info['practice1_accuracy'] + basic_info['practice2_accuracy']) / 2
    
    # DataFrame 생성
    df = pd.DataFrame([basic_info])
    return df.to_csv(index=False, encoding='utf-8-sig')
