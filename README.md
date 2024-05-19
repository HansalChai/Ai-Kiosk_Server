# Ai-Kiosk_Server

24.05.08 초기세팅 완료

1. Django 프로젝트 생성

Ai-Kiosk_Server 디렉토리에 들어온 후,

1-1. 가상환경 설정
python -m venv venv
or python3 -m venv venv

1-2. 가상환경 활성화
source venv/bin/activate

2. 라이브러리 설치

지금 설치한 건 'Django', 'djangorestframework' 이 두 개 밖에 없어서 requirements.txt에 넣어놨습니다.

pip install -r requirements.txt

위 명령어 사용하면 txt 파일에 들어있는 라이브러리들 한 번에 설치 가능합니다.

- 라이브러리 설치 이후 settings.py, urls.py에 맞는 거 수정해야 함

~/settings.py

INSTALLED_APPS = [
'django.contrib.admin',
'django.contrib.auth',
'django.contrib.contenttypes',
'django.contrib.sessions',
'django.contrib.messages',
'django.contrib.staticfiles',
'rest_framework' ####### 이거
]

~/.urls.py

from django.conf import settings ## 이거 1
from django.contrib import admin
from django.urls import path, include ## 이거 2

urlpatterns = [
path('admin/', admin.site.urls),
path('api-auth/', include('rest_framework.urls')) ## 이거
]

지금 앱도 안 만들고 home도 없어서 서버 실행한 후에
http://127.0.0.1:8000/admin/
http://127.0.0.1:8000/api-auth
여기로 들어가야 뭐 나옵니다

3. 언어, 시간대 변경

settings.py에서

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

두 설정 바꿨습니다.

-

requirements랑 settings.py는 common, dev, prod 나눠서 종속성 관리 해줘야 한다해서 우선 나눠만 놓았고 settings는 잘 몰라서 우선 폴더랑 파일만 만들어놓고 아무것도 안 건들였음. 공부하면서 해야 할듯 !

- .gitignore 에는 가상환경이랑 파이썬, vscode 관련된 거 넣어놨음

# pip install 중요!

|| pip install -r requirements.txt
|| -> git pull 받으면 꼭 한 번 실행해주기

# ADD LIBRARY

|| pip freeze > requirements.txt
|| -> 라이브러리 추가할 때마다 실행해주기
