# NIA_dataprocessing
 * 자율주행 데이터 취득 후 센서별 데이터 취득, timestamp기반 센서 데이터 매칭 및 데이터 핸들링 관련 프로그램 모음

## pcd 추출
- windows,LABview 환경에서 logging 된 라이다 데이터 .bin 파일을 pcd파일로 변환하여 추출하는 코드
- 라이다 패킷에 대한 데이터 구조는 각 제조사 제공 메뉴얼에 다 정리되어 있음. 이에 기반하여 패킷을 point cloud 데이터로 변환
- 각 버전에 대한 설명은 '정제버전설명.txt'을 참고

<center><img src="https://github.com/lucas-korea/adas_sensor_project/assets/57425658/f3321f6d-7d9b-4e5c-a46d-77c36a9f0dd9" width="300" height="150"></center>  

## 열화상 카메라 추출
 - 국내 H사 열화상 카메라 로깅 데이터에 대하여 binary데이터를 이미지 픽셀 데이터로 변환

    <center><img src="https://github.com/lucas-korea/adas_sensor_project/assets/57425658/fdc68c15-e415-49fc-9844-f6fcab129841" width="320" height="240"></center>  



## RGB 카메라 추출
 - RGB 카메라 로깅 데이터에 대하여 binary데이터를 이미지 픽셀 데이터로 변환
## GPS 데이터 추출
 - Oxts社의 RT3000 GPS 데이터 로깅 데이터 핸들링
 - NMEA 형식을 이용하여 위경도, 고도, 각도 등의 데이터를 추출
 - 연속 GPS 데이터에 대하여 google map API를 이용해 주행경로를 지도에 ploting 기능
   
   <center><img src="https://github.com/lucas-korea/adas_sensor_project/assets/57425658/11499015-e5d8-4a53-819b-78a72bc66177" width="320" height="240"></center>  
   gps 데이터와 google API를 이용한 주행경로 확인 및 정밀성 평가

   <center><img src="https://github.com/lucas-korea/adas_sensor_project/assets/57425658/fa499ca4-7b0b-491e-989f-b48df6429c34" width="420" height="80"></center>  
   Oxts GPS에서 추출한 프레임별 데이터 예시. 시간, 위/경도, 롤피치요 각도, 속도 등

## data matching(중요)
 - 라이다s, 카메라s, GPS 데이터를 취득시 저장된 timestamp 기반하여 센서 데이터 매칭 자동화 프로그램  

   <center><img src="https://github.com/lucas-korea/adas_sensor_project/assets/57425658/45479d2e-b01a-439d-b2c2-8d6f1562bb3f" width="420" height="480"></center>  

### utils
 - 라이다 데이터 축 변환
 - 딥러닝 기반 image interpolation
 - 기타 프로그램에 필요한 코드
