# 애플리케이션 설정
APP_CONFIG = {
    'title': 'SEP ME ver.6 - 학생 글 채점 연습',
    'version': '6.0.0',
    'author': 'SEP Team',
    'description': 'AI 기반 학생 글 채점 연습 프로그램'
}

# 등급 기준
GRADE_CRITERIA = {
    1: {'min': 29, 'max': 33, 'description': '매우 우수'},
    2: {'min': 27, 'max': 28, 'description': '우수'},
    3: {'min': 24, 'max': 26, 'description': '보통'},
    4: {'min': 20, 'max': 23, 'description': '미흡'},
    5: {'min': 13, 'max': 19, 'description': '매우 미흡'}
}

# 점수 범위
SCORE_RANGES = {
    'content': {'min': 3, 'max': 18, 'description': '주제 적합성, 내용의 충실성, 독창성'},
    'organization': {'min': 2, 'max': 12, 'description': '글의 구성, 단락 구성, 논리적 연결'},
    'expression': {'min': 2, 'max': 12, 'description': '어휘 사용, 문장 표현, 맞춤법'}
}

# 파일 경로
PATHS = {
    'data': './data/',
    'assets': './assets/',
    'results': './data/results/',
    'samples': './data/samples.csv'
}

# UI 설정
UI_CONFIG = {
    'primary_color': '#007bff',
    'success_color': '#28a745',
    'warning_color': '#ffc107',
    'error_color': '#dc3545',
    'info_color': '#17a2b8'
}

# 성과 평가 기준
PERFORMANCE_CRITERIA = {
    'excellent': {'min': 85, 'grade': 'A+', 'description': '탁월함'},
    'very_good': {'min': 75, 'grade': 'A', 'description': '우수함'},
    'good':
