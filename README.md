---

# Flask-Template

Flask(2.0.3) 과 Flask-Restful 프레임워크를 활용해 빠르게 서버를 띄울 수 있도록 만들어 둔 Flask-Template 입니다.

범용적인 서비스에 대응하기 위해 큰 탬플릿을 작성하였으나, 
간단한 API 서버가 필요한 경우 프로젝트 최상위 경로에 위치한 `single_file_server.py` 를 참고하면 
빠르게 Micro-Service 를 호스팅 할 수 있습니다.

---

## 개요

### 기본적인 구성

- 주요 파라미터는 `environments.yaml` 을 참조 하도록 구성 (at `settings.py` & `RunServer(with docker)`)
  
  docker 는 프로젝트 경로와 컨테이너 내부를 Bind-Mount 하여 코드 동기화
  
- server_timezone 및 logger 세팅

- HealthCheck API 를 포함하여, 기본적인 URL-parameter, JSON, Form-Data(File) 포멧의 Request parameter 입력에 대응하는 SampleAPI 구성
  
- Response 포맷 통일
    
  `{'code': status_code, 'message': message, 'payload': payload}`

---

## 초기 실행

### Dependency

```
flask==2.0.3
flask-cors==3.0.10
flask-restful==0.3.9
werkzeug==2.0.3
pyyaml
Pillow==8.3.2  # 이미지 처리 예시를 위한 라이브러리 (/api/upload_form_data)
pandas==1.4.0  # CSV 처리 예시를 위한 라이브러리 (/api/upload_form_data)
numpy==1.22.2
```

conda 환경에서 uwsgi 를 설치할 땐, `conda install -c conda-forge uwsgi` 명령어를 사용해 설치

### Skeleton

```
└── flask-template
    ├── /api
    │   ├── /sample
    │   │   ├── get_query_string.py
    │   │   ├── json_api.py
    │   │   └── upload_form_data.py
    │   │
!   │   └── response.py
    │
    ├── /bin
    │   ├── build_docker_image.sh
    │   ├── docker_run_container.sh
    │   ├── docker_stop_container.sh
    │   ├── pip.conf
    │   ├── run_dev_server.sh
    │   └── yaml_reader.sh
    │
    ├── /common
    │   ├── /logs
    │   ├── /media
    │   └── /static
    │
!   ├── /nameless_server
    │   ├── logger_config.py
    │   ├── settings.py
    │   └── system_api.py
    │
    ├── /system
!   │   ├── environments.yaml
    │   ├── keys-sample.yaml
*   │   └── keys.yaml
    │
    ├── .gitignore
    ├── Dockerfile
    ├── README.md
    ├── requirements.txt
    ├── server.py
    └── single_file_server.py  
        # 단일 파일 동작 서버 >>> python single_file_server.py
```

Repository 에는 다음과 같이 `*` 표시된 경로 & 파일들이 빠져있습니다.
( 미 세팅시 서버가 동작하지 않습니다 )
- /system 이하 경로에 `keys.yaml` 세팅 (DB 및 기타 중요 key 값을 기록)

프로젝트 서버 구성을 위해 `!` 표시된 파일들의 내용 수정이 필요합니다.
- 대부분 시스템 환경 세팅은 environments.yaml 수정으로 변경됩니다.

- 프로젝트의 이름에 따라 settings.py 가 있는 폴더의 이름 (탬플릿에선 `/nameless_server`) 을 변경하길 권장하지만, 필수 사항은 아닙니다.

- 프로젝트의 이름에 따라 `/api/response.py` 파일에 작성된 Response Class (탬플릿에선 `NamelessServer_Response`) 의 이름을 변경하는 것을 권장합니다.

---

## Run

서버 실행을 위한 명령어

### Python 가상환경에서 개발서버 구동
```
# environments.yaml 의 server 파라미터를 참조하여 서버 구동
./bin/run_dev_server.sh
```

### Docker Container 로 구동
```
# Docker Image 빌드
./bin/build_docker_image.sh
# Container 실행
./bin/docker_run_container.sh
# Container 중지
./bin/docker_stop_container.sh
```

---
