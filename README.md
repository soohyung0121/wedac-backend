# Wedac 프로젝트 소개 _ BackEnd

암호 화폐 거래소 GDAC 웹사이트 클론 프로젝트입니다.
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
![](https://images.velog.io/images/jeongin/post/42270f13-dc2a-4989-bea1-974b82cabb0b/image.png)

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
[회원가입, 로그인, 좋아요](https://interstellar-sunset-788761.postman.co/collections/7338957-fceb2bce-0c66-4d27-82fe-479806136a99?version=latest&workspace=9e529a22-5100-4f53-85c7-608a41491819)

[PRODUCT 상세페이지 및 설정하기](https://interstellar-sunset-788761.postman.co/collections/10871481-cdba486f-5c26-4d62-8e16-d4464932eda3?version=latest&workspace=9e529a22-5100-4f53-85c7-608a41491819)

[DAY-DATE LIST](https://interstellar-sunset-788761.postman.co/collections/10871815-34aa5019-5c1b-4596-9fcf-a17a7bbf6023?version=latest&workspace=9e529a22-5100-4f53-85c7-608a41491819#e1a2af48-fdf1-4e74-8c93-1c5bc30ffa93)
