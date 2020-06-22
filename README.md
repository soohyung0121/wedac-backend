# Wedac 프로젝트 소개 _ BackEnd
암호 화폐 거래소 GDAC 웹사이트 클론 프로젝트입니다.
<br>
<br>

## 개발 인원 및  기간
- 기간 : 10일(5월 11일 ~ 5월 22일)
- Back-end members : [Yeeunlee](https://github.com/yenilee), [Soohyungkim](https://github.com/soohyung0121)
- [Front-end GitHub](https://github.com/wecode-bootcamp-korea/wedac-frontend)
<br>

## 데모 영상 
[![Video Label](http://bitly.kr/sJamEpDUGl)](https://youtu.be/LdF1LG_R4Uo)

<br>

## 목적
- 웹페이지의 구조를 파악하여 모델링
- 모델링을 기반으로 API 생성(model, view, url 작성)
- 팀프로젝트를 통한 프론트엔드와 백엔드간의 의사소통

<br>

## 적용 기술 및 구현 기능


### 적용 기술

- Python
- Django web framework
- Beautifulsoup
- Selenium
- Bcrypt
- Json Web Token
- AWS EC2, RDS
- CORS headers
- Gunicorn

<br>

### DB Modeling
[](http://bitly.kr/XqkxcGrtK8)

### 구현 기능
- 회원가입 및 로그인 (Bcrypt 암호화 및 JWT Access Token 전송) 기능 구현
- 정규 표현식을 통한 ID, Password Validation
- 이메일, 문자 인증 기능 구현 
- 매수/매도 기능 
- 가상의 통장을 생성하여 입/출금 기능 구현(실 거래는 불가)

#### 인프라
- Amazon AWS를 통한 배포
- EC2 인스턴스에 RDS서버에 설치된 mysql 연동

<br>

## API documents(POSTMAN)

