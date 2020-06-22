# Wedac 프로젝트 소개 _ BackEnd
암호 화폐 거래소 GDAC 웹사이트 클론 프로젝트입니다.
<br>
<br>

## 개발 인원 및  기간
- 기간 : 10일(5월 11일 ~ 5월 22일)
- Back-end members : [Yeeunlee](https://github.com/yenilee), [Soohyungkim](https://github.com/soohyung0121)
- [Front-end GitHub](https://github.com/wecode-bootcamp-korea/wedac-frontend)

## 데모 영상 
[![Video Label](http://bitly.kr/sJamEpDUGl)](https://youtu.be/LdF1LG_R4Uo)
<br>

## 진행 방식
- scrum 방식으로 agile한 팀 프로젝트 진행
- Daily standup meeting, trello 체크 및 공유 
- 프로젝트 기간 동안 weekly sprint 2회로 나누어 진행 

## 기술

- Python
- Django web framework
- Beautifulsoup 
- Selenium
- Bcrypt
- Json Web Token
- AWS EC2, RDS
- CORS headers
- Gunicorn
- Websocket (기술 조사)
<br>

## DB Modeling
![](http://bitly.kr/BRv5mjbimu)

## 구현 기능
### 회원가입/로그인
- 카카오 API 연동하여 로그인 및 사용자 정보 조회 기능 구현
- 정규 표현식을 통한 ID, Password Validation
- 회원가입 시 이메일, 문자 인증 기능 구현

### 거래
- 기준 화폐(KRW, BTC, 지닥토큰 등)에 따른 암호 화폐 일별 저가, 고가, 종가 등 가격 데이터 조회
- 매수/매도 기능 구현 (transaction으로 작업 단위 ) 
- 가상의 통장을 생성하여 입/출금 기능 구현(실 거래는 불가)

## 인프라
- Amazon AWS를 통한 배포
- EC2 인스턴스에 RDS서버에 설치된 mysql 연동

<br>

## API documents(POSTMAN)
추가 
