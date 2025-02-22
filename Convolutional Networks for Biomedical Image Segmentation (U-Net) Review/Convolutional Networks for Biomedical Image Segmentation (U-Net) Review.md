# U-Net : Convolutional Networks for Biomedical Image Segmentation Review 

- papers : https://arxiv.org/abs/1505.04597

## 0. Abstract 

- 딥러닝의 경우 충분히 많은 학습 데이터를 필요로 함 
- 논문에서는 적은 양의 학습 데이터를 가지고도 충분히 좋은 성능을 내는 Augmentation 방법을 사용하여 학습함 
- 네트워크의 경우 "Contracting path" 와 "Expanding path"으로 구성하여 적은 데이터로 End-to-End의 학습을 수행 
  - Contracting path : 이미지의 특징을 추출 
  - Expanding path : localization을 가능하게 함 
- 성능적으로도 높게 나와서 대부분의 대회에서 SOTA를 달성함 
  - ISBI 대회에서 이전의 가장 좋은 방법인 sliding-window의 성능을 뛰어넘음 
  - ISBI cell tracking chaalenge 2015에서도 우승 
- 네트워크의 속도 또한 빨라서 512x512의 이미지 기준으로 Segmentation이 몇 초밖에 걸리지 않음 

## 1. Introduction 

- Visual Recognition 분야에서 딥러닝 모델 성능의 향상을 보였고 이를 Biomedical 분야에 적용하려는 시도를 보임 
- Biomedical image processing 분야의 경우 각각의 픽셀이 클래스를 가지는 "localization"이 필요함 
- 특히, Biomedical의 특성상 학습 데이터의 수가 많이 부족할 수 밖에 없음
  - 전문가가 라벨링을 해야하고 환자의 데이터이기 때문에 라벨된 이미지의 수가 부족함 
- 위의 한계를 극복하기 위해서 Ciresan [1]의 경우 Sliding Window 방식을 도입 

![](https://drive.google.com/uc?export=view&id=1UeNMMcJyaFYgrtpFIkrTFRMYge4-2Kqd)

- Sliding Window 방식의 경우 아래의 장점이 존재 
  - Localize를 가능하게 함 
  - 패치 단위의 학습을 할 경우 데이터의 양이 많아지는 효과가 있음 
  - EM segmentation challenge에서 좋은 결과를 가져옴 
- 하지만 Sliding Window 방식의 Patch 단위 학습은 2가지의 문제점이 있음 
  - 각각에 Patch에 대해 학습을 하기에 속도가 느리고 패치마다 많은 영역이 겹치는 부분이 생김
  - Localization 정확도와 context의 사용간에 trade-off가 존재 
    - Patch가 크면 주변정보도 같이 학습이 가능하지만 이미지의 크기를 줄이기위해 많은 Pooling이 필요하고 이는  localization accuracy을 떨어트림 
    - Patch가 작으면 Sub sampling에 의한 정보 손실은 작아지지만 작은 context만 보는 문제점이 있음  
    - 이는 classifier의 output을 multiple layer의 features로 고려해서 Good Localization과 use of context가 가능해짐
- 추가적으로 Sliding Window 방식이 아닌 Overlap-tile 전략을 통해 이미지를 패치단위로 쪼개서 학습함  
  - fully connected layers를 사용하지 않고 오직 convolution만 사용하여 Overlap tile을 통해 임의의 이미지를 입력으로 받아도 문제가 없게함 
  - 큰 이미지를 한정된 GPU에서 학습하도록 함 

![](https://drive.google.com/uc?export=view&id=1qU-5ckfupH9E8qWmqljjND6DugAv1wQj)

- 이때 겹치지 않은 파란색 Input과 노란색 Output 사이의 차이를 보완해주기 위해서 Mirroring 방식을 사용

![](https://drive.google.com/uc?export=view&id=1U6QzqqgtPXzbmO6AA8iHWpREoGmq_r2s)

- 이미지의 테두리 영역에서 픽셀을 예측하기 위해 입력 이미지를 미러링하여 누락된 부분을 추정

![](https://drive.google.com/uc?export=view&id=1tAPr_CklemFE6a1jJNtQtObWlC7MDDPE)

- Unet의 경우 FCN을 확장한 U 모습의 네트워크를 제안 
  - 적은 학습 데이터를 가지고도 높은 성능을 가짐 
  - FCN의 주요 공헌이었던 Contracting network를 이용하여 출력의 Resolution을 증가시키는 방법 사용 
- Upsampling시에 채널의 수를 크게함으로서 context information을 높은 resolution layer에 전파 
- FC Layer을 제거하고 Convolution만을 이용하여 Overlap tile 전략에의해 임의의 크기의 이미지가 들어와도 Segmentation이 가능하게 함
- 결론적으로 contracting path는 expanding path와 대칭이고 U-shape의 모양을 가짐 
- 이를 이용하여 "the segmentation of neuronal structures in EM stacks"와 ISBI cell tracking challenge 2015에서 SOTA를 달성  

## 2. Network 

### 2.1 Contracting Path 

![](https://drive.google.com/uc?export=view&id=1IZVh5fKlPAEpTlInbWx4Ra_ZZg4FADfm)

### 2.2 Expanding Path 

![](https://drive.google.com/uc?export=view&id=1qyPYtDdYtxt-3_MVUST5cCaUVrFoUF1V)

## 3. Training 

### Optimizer 

- SGD with momentum 0.99
  - 배치를 키우는 것보다 타일의 크기를 키우는걸 선호 
  - 단, 배치가 작아서 학습이 잘 안되는 문제가 발생하기에 이를 해결하려고 모멘텀을 키워 이전의 샘플도 같이 사용하도록함 

### Energy function 

![](https://drive.google.com/uc?export=view&id=1uIbVMC7g_pkNeqfsmptMsVqF0Y4a9X9R)

- pixel-wise soft-max를 수행하고 cross-entropy loss 함수를 통해서 학습을 진행함 
  - pk(x) : approximated maximum-function (k개의 클래스에 대해서 분류한 확률)
  - a(x) : 픽셀 x의 활성화 함수
  - K : 클래스의 개수 

### Touching cells separation 

![](https://drive.google.com/uc?export=view&id=1as77mPEM9kRjnt06RM8ev9y3IG0apmcn)

- pixel-wise loss weight를 계산하기위한 weight map을 생성 

  - 같은 클래스를 가지는 인접한 셀을 분리하기위해서 해당 경계부분에 가중치를 제공 
  - 가중치의 계산은 아래의 식을 이용해서 계산 

  ![](https://drive.google.com/uc?export=view&id=1nKfZwYJnLLqR4sT--7UwyhyugCMTOOx_)

  - Wc(x) : 클래스별 빈도에 따른 가중치 
  - d1 : 가장 가까운 셀과의 거리 
  - d2 : 두번째로 가까운 셀과의 거리 
  - 인접 셀들간의 거리가 가까워서 d1 + d2가 작으면 지수함수 부분이 크게되어서 가중치를 크게 받음 
    - w0 : 10, 시그마 : 5으로 설정 

![](https://drive.google.com/uc?export=view&id=1F7jJlNDjOFQ60HFxL5IzyZRowxlexIsh)

- Energy function과 weight map을 결합해서 최종적인 로스함수 생성 

### Weight initialize 

- Gaussian distribution 학습 파라미터 초기화
  - standard deviation : (2/N) ** 0.5 (N : number of incoming nodes of one neuron)
    - 예) 3x3x64 Convolution의 경우 9x64=576의 N을 가짐 

### 3.1 Data Augmentation 

![](https://drive.google.com/uc?export=view&id=1N-aGjgO3F491_Y3gZfcVd7ogYDKK1tkm)

- Random Elastic deformations를 통해서 Augmentation을 수행 
  - 모델이 invariance와 robustness를 학습할 수 있도록 하는 방법 
  - shift and rotation invariance와 deformations에 대한 robustness, gray value variations을 충족시킴 

## 4. Experiments 

### 4.1 EM segmentation challenge 

![](https://drive.google.com/uc?export=view&id=1Yri-6FQKPdQkF243yx2Pf2txNxlhWuL9)

- 30 images (512x512 pixels) from serial section transmission electron microscopy of the Drosophila first instar larva ventral nerve cord (VNC) - 초파리 유충 1단계의 무척추 중추 신경계
- cells (white) and membranes (black) - 세포와 세포막을 각각 Segmentation 하는 테스크 
- 평가 지표는 Warping Error, Rand Error, Pixel Error 

![](https://drive.google.com/uc?export=view&id=1_auTTl3CppCOBOI1Vx2GpNP-ek1CzgIL)

- 7개 버전으로 회전시킨 입력데이터를 학습한 u-net에 전처리와 후처리를 통해 1등 달성 

### 4.2 ISBI cell tracking challenge 

![](https://drive.google.com/uc?export=view&id=1k6QycllY2ARBMlh5dm50vQ1pj0v9R7pE)

- PhC-U373 : Giloblastoma-astrocytoma U373 Cells on a polyacrylimide substrate recorded by phas contrast  microscopy (Fig.4.a, b) 
  - 35개의 annotated training images 
- DIC-HeLa : HeLa cells on a flat glass recorded by differential interference contrast (DIC) microscopy (Fig.4.c, d)
  - 20개의 annotated training images 

![](https://drive.google.com/uc?export=view&id=173dgzidr2JZgWsmFz3NPO8ovmVOIErrB)

- IoU 평가지표로 둘 모두 압도적으로 1등을 달성 

## 5. Conclusion 

- 3개의 데이터셋에서 압도적인 성능을 달성한 네트워크 
- 학습 데이터셋의 부족을 극복하기위해서 elastic deformations을 사용
- Titan GPU (6 GB)로 10시간의 학습시간과 수초의 추론시간을 가짐 

### 5.1  Advantages 

- 바이오 메디컬 이미지가 가지는 여러가지 한계를 극복하기 위해서 다양한 기법들을 도입 
  - 데이터 셋의 부족 
    - Overlap-tite strategy 
    - Mirroring Extrapolation
    - Elastic Deformations
  - 겹치는 세포들의 분리 
    - Weight Loss 
- Concatenation과 High Channel을 통해서 High Resolution의 세그멘테이션 출력을 생성 
- 3개의 데이터셋에서 모두 SOTA를 달성했을 정도로 압도적인 성능을 보임 

### 5.2 Disadvantages 

- 압도적인 성능에 대한 근거가 많이 부족함. 비록 딥러닝이 블랙박스 모형이기는 하지만 이전의 DeconvNet의 논문처럼 시각적으로 해석하려는 시도가 들어갔으면 더 좋았을 것 같음 
- Biomedical으로 데이터셋을 한정해서 실험했는데 VOC2012 등의 대회에도 제출해서 결과를 확인해봤으면 더 좋았을 듯 
- Zero-padding을 안해서 발생하는 문제를 Mirroring을 통해서 해결하려는 이유를 모르겠음. 
  - 실제 세포의 이미지를 보면 대칭형태가 아닌데 차라리 타일을 더 크게해서 학습하고 Crop하는 형식이 더 맞지 않을까 생각이듬
  - 아니면 DeconvNet에서 결과들을 앙상블한 것처럼 제로페딩을 수행하고 앙상블하는 방법도 있었을 듯 

## 6. Apendix 

- http://brainiac2.mit.edu/isbi_challenge/home
- https://towardsdatascience.com/review-u-net-biomedical-image-segmentation-d02bf06ca760
- https://joungheekim.github.io/2020/09/28/paper-review/