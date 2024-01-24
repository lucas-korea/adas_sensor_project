
## 3d_iou_evalution
 - 3d point cloud cuboid의 GT와 인식기 결과값에 대한 3d iou를 계산하여 성능 평가
 - 성능 평가 결과에 대한 csv 파일 출력  

|<b>평가 시각화</b> |
| :--: |
| ![](https://github.com/lucas-korea/adas_sensor_project/assets/57425658/ab8a9ee2-beac-4974-82e0-0803a8f09e25)|

|<b>평가 프로세스</b> |
| :--: |
| ![](https://github.com/lucas-korea/adas_sensor_project/assets/57425658/2a4b6e2f-a082-4a60-9c38-7f35aad6a125)|

## Lidar basic function evaluation 2d viewer
 - 라이다 성능 평가를 위해 ROI를 지정하여 depth, intensity 값을 상세확인 가능한 툴
    * bbox의 크기 및 위치를 기입하여 ROI를 설정하고, 해당 ROI에 속한 데이터의 값을 보여준다
    * 대상 객체에 대한 라이다의 성능을 평가하기 위해 ROI를 설정하여 해당 부분만 평가 할 수 있게 설계 
 - 확대, 축소 기능
 - tkinter 패키지 기반

|<b>라이다 성능 평가 프로그램</b> |
| :--: |
| ![](https://github.com/lucas-korea/adas_sensor_project/assets/57425658/138c90cd-a4d9-4348-b0d8-1589d9e8abc4)|
