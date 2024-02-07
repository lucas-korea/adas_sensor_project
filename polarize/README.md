## polarize camera 

- sony IMX250MZR 편광 센서 사용
- bayer 구조의 이미지 프로세싱  

- demosicing
- 편광파라미터를 활용한 이미지 분석 자동화 프로그램 개발  
- 편광카메라 이미지 추출
- 편광 센서가 적용된 이미지 데이터를 이용해 bayer 수준의 이미지 프로세싱 알고리즘을 적용, 성능을 평가하는 프로그램을 개발 

[stokes parameter](https://en.wikipedia.org/wiki/Stokes_parameters)  
𝑆_0=𝐼=𝑃_(0˚)+𝑃_(90˚)  
𝑆_1=𝑄=𝑃_(0˚)−𝑃_(90˚)  
𝑆_2=𝑈=𝑃_(45˚)−𝑃_(135˚)  
  
𝑃_(𝑥˚)  - 각도 𝑥로 편광된 성분  
𝑆_0 - 전체 광량  
𝑆_1,𝑆_2  - 편광의 정도  

𝐷𝑜𝐿𝑃=√(𝑆_1^2+𝑆_2^2 )/𝑆_0    = 편광 성분의 크기 (선편광도)   
𝐴𝑜𝐿𝑃=𝑎𝑟𝑐𝑡𝑎𝑛⁡〖𝑆_2/𝑆_1 〗  =편광된 각도(선편광각) 



### 소니 편광카메라 픽셀 구조
---
<center><img src="https://github.com/lucas-korea/adas_sensor_project/assets/57425658/f99b12be-6bd2-4977-a78b-a8f6bc52d3c0" width="500" height="170"></center>  



### **이미지 프로세싱**  
---
DOLP이미지는 편광의 정도, AOLP는 편광의 각도를 의미한다. 따라서 DOLP는 흑백이미지로 강도를 표현할 수 있고, AOLP의 경우 color map을 구성하여 360의 편광 방향을 반영한다. 

 

이 두가지 이미지를 합쳐서, hue는 AOLP의 값으로,  saturation은 DOLP의 값으로, brightness는 255로 고정하여 HSV 형태로 이미지를 표현할 수 있게 만들어 보았다


<center><img src="https://github.com/lucas-korea/FLIR_LUCID_acquire/assets/57425658/f84194a9-dc2d-4388-8de9-c2cfe949dda1" width="650" height="270"></center>  
<p align="center" style="color:gray">
   이미지 프로세싱 결과
   (각도별 분할, DOLP AOLP 결합)
</p>

 ***
```
def distribute_polarize_img(polar_image)
```
- 각 각도별로 이미지 분리

 ***
```
def polar_analysis(polar_image_gray, img_path_)
```  
- 각 각도별로 이미지 분리 및 뷰잉
 ***

```
def Glare_reduction
```
- 4가지 방향 데이터 중, 가장 값이 작은 데이터를 반사광이 없는 픽셀로 간주
- 만약 편광 성분이 하나도 없다면, 픽셀간 데이터 차이는 없을 것
 ***

```
def S_0_img(polar_image)
```
- S_0 = I = (P_0 + + P_45 + P_90 + P_135)/2

 ***

```
def S_1_img(polar_image)
```
- S_1 = Q = P_0 - P_90
***

```
def S_2_img(polar_image)
```
- S_2 = P_45 - P_135
 ***

```
def DOLP(polar_image)
```
- Degree of linear Polarize, 편광의 정도
 ***

```
def AOLP(polar_image)
```
- Angle of linear Polarize, 편광의 각도
 ***

```
def HSV_color_mapping(AOLP_img_)
```
 - AoLP 이미지를 분석하기 위한 HSV color mapping 
 ***

```
def DOLPplusAOLP(polar_img)
```
- DoLP + AoLP 이미지 통합 분석하여 이미지 생성