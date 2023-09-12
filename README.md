# `branch전략, PR, commit 컨벤션`

Smart-Parking 프로젝트 브랜치 전략과 풀 리퀘스트

<br>

## `1. 브랜치 전략`

먼저 코드의 충돌나는 상황을 최대한 적게 하고 프로젝트를 배포할 때 수월하게 하기 위해서는 브랜치 관리를 잘하는 것이 중요합니다. 

따라서 아래와 같이 브랜치를 관리하려고 합니다. 

<br>

### `main 브랜치`

- develop 브랜치에서 배포할 수 있을 정도로 구현된 것을 Merge를 하는 브랜치입니다. 

<br>

### `develop 브랜치`

- 기능 개발과 버그 수정의 브랜치 Merge가 자주 일어나는 브랜치입니다. 한마디로 개발이 활발하게 일어나는 브랜치입니다. 

<br>

### `docs 브랜치`

- readme와 같은 markdown파일을 수정 및 추가하는 브랜치입니다. 

<br>


### `feature/#이슈번호`

- 본인이 이슈를 만들었던(기능) 것에 대한 기능을 개발하는 브랜치입니다. 기능이 완벽하게 구현이 되었다면 develop 브랜치에 Pull Request를 보낸 후에 Merge를 하면 됩니다. ex) feature/#1

<br>

## `CLI로 브랜치를 만드는 방법`

```
git checkout -b 브랜치이름 (해당 브랜치가 존재하지 않는다면 브랜치를 새로 만들면서 바로 그 브랜치로 이동합니다.)
ex) git checkout -b feature/#1

git checkout 브랜치이름 (존재하는 브랜치가 있다면 그 브랜치로 이동합니다.)
ex) git checkout feature/#1
```

<br>

## `Pull Request 보내는 방법`

Pull Request를 보내는 이유는 Merge 하기 전에 `코드 리뷰`를 하기 위해서 입니다. 
만약 `feature/#1`과 같은 기능 브랜치가 완성이 되었다면 `develop` 브랜치에 Pull Request를 보내야 합니다. 그 방법에 대해서 알아보겠습니다. 

```
git add "파일 명"
git status
gitmoji -c  
git push origin 브랜치이름
```
이후 GitHub 접속 후 compare & pull request 버튼 클릭

PR메시지 작성 후 PR보내기

# `Commit Message Convension(깃모지 사용)`

### `GITMOZI`

- `✨`: 새로운 기능
- `🐛`: 버그 수정
- `📝`: README, wiki 문서 수정
- `💄`: 코드 변경 없이 스타일 변경
- `♻️`: 리팩토링
- `💡`: 동작에 영향이 없는 코드 변경 없는 변경사항(주석 추가 등등)
- 이외의 것들은 https://gitmoji-js.netlify.app/  참고
### `title`
- 첫 글자는 대문자로 입력
- 마지막에 .을 찍지 않음
- 명령문의 형태 (동사 원형 사용)
- 끝에는 작업중인 이슈번호를 붙임 '#이슈번호'
### `message`
- 각 줄은 최대 72자를 넘지 않도록 함.
- 어떻게 무엇을 왜 변경했는지 설명