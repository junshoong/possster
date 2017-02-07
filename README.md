# possster
[![Build Status](https://travis-ci.com/vaporize93/possster.svg?token=n9ZwF2LE4Sw2aM9mujNf&branch=master)](https://travis-ci.com/vaporize93/possster)
2017년 SSS 겨울 프로젝트 웹 대자보/포스터 possster

## 개발 환경
- windows 10 , Arch Linux, OS X
- python 3.5 or 3.6
- django 1.10
- postgresql 9.61

## Work Flow

> 개인 별로 커밋을 할 때 `git add -p`와 `git commit -v`로 자신의 코드를 다시 한 번 확인하는 습관을 들이자.

1. 코드를 `push` 하기 전에 `pull`한 뒤에 올바른 작동을 하는지 확인하고 진행한다.
2. 로컬에서 개발을 진행하고 확실히 문제가 없으면 `develop`에 `pull`한다.
3. 일정 간격으로 완성된 프로그램을 `master`에 `pull` 하고 서비스를 유지한다.
4. 같은 부분은 개발하지 않도록 조율하고, 수정이 필요한 부분은 일단 `issue`로 등록한다.
5. 코드를 확인받고 싶으면 `pull request`를 올리고 슬랙에 코드리뷰해달라고 부탁한다.
6. 코드에 문제가 있는경우에는 되돌린 후에 작성자가 다시 작업한다.

## Docker deploy
```
$ docker run --name db -d postgres
$ docker run --name possster --publish 80:80 --link db:db --env="DJANGO_SETTINGS_MODULE=possster.production" --env="PYTHONIOENCODING=UTF-8" -d harvey/possster
```

## Collaborators

김준수, 추건우, 공원배, 고다경
