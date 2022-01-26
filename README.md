# 반자율주행자동차

## 개요

고등학교 2학년 동아리 활동 중 제작한 작품.

개발기간 4~5개월 걸렸다.

학업이랑 겹쳐서 그런지 생각보다 오래 걸린 것 같다.

## 사용 부품

고딩 1학년때 쓰고 남은 차체 부품을 재활용하고,

아두이노에 기반하고 ESP32 칩셋이 탑재된 와이파이 보드와 카메라 보드를 사용.

카메라 보드에는 와이파이도 탑재돼있어 촬영과 동시에 송출이 가능하다.

## 로직

카메라 보드가 촬영한 데이터를 송출하면, 컴퓨터가 받아서 데이터를 분석하고

와이파이 보드에 조향할 방향과, 속도를 지시한다.

와이파이 보드는 지시를 수신해 차체를 제어한다.

## 개발언어

아두이노 -- C++

데이터 처리 -- python

## 한계 & 느낀점

1. ESP32 카메라 보드의 한계로
