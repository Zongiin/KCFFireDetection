# KCFFireDetection
한국코드페어2020빌더스챌린지 출품작

프로그램 구조
--------------
이 프로그램은 두 개의 프로젝트로 나뉘어진다.

하나는 monkey.py이다. 이 파이썬 프로그램은 영상을 입력받고 영상에서 화재를 감지하는 역할을 한다.

monkey.py는 yolov4 weight를 tensorflow용으로 변환하여 화재 감지에 사용한다.

[이 링크](https://colab.research.google.com/drive/16XM8A53CNXX7NQi4yP4tBw6Modzgnf3m?usp=sharing)의 구글 코랩 노트북을 통해 구글의 클라우드 서버를 이용하여 weight를 training했다.

수백장의 화재 사진에 불이 난 부분을 표시한 뒤, 위의 코랩 노트북을 통해 클라우드에 화재 사진을 업로드하고 그 데이터를 통해 학습시킨 weight를 [tensorflow-yolov4-tflite](https://github.com/hunglc007/tensorflow-yolov4-tflite)을 통해 tensorflow용 weight로 변환하여 사용했다.

