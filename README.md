# project1
관통 영화 프로젝트

---

git 관리법
1. 원본 레포지토리 접속
   - https://github.com/KimYehyun0307/project1.git
2. fork 눌러서 퍼가기
3. 자기 레포지토리에서 fork한 레포지토리를 git clone
4. 원본 레포지토리 upstream으로 추가
   - git remote add upstream https://github.com/(자기 github 닉네임)/project1.git
5. 별도 브랜치 자기 영문이름으로 생성
   - 사유: 번거로움 방지
   - git checkout -b 영문이름
     - 이미 브랜치 있는 경우 브랜치 이동만 하시면 됩니다
6. add, commit
   - 커밋 양식: yy.MM.DD hh.mm 자기 이름 - 내용(ex: css 추가)
7. push 할때 작업한 브랜치명으로
   - git push origin (본인 브랜치명)
8. push 완료 후 레포지토리 새로고침 한 뒤 pull request
9. 버튼 누르고 풀 리퀘스트 작성
10. 머지 완료하면 자기 origin branch와 생성한 branch sync 버튼 눌러서 동기화 진행

---

# 작업 log

### 3조

**팀장: 김동철**
담당한 작업:

**팀원: 김예현**
담당한 작업: 카카오, 사이트 고유 로그인/아웃, 프로필, navbar, 바탕화면

목표 서비스
- 사용자의 나이를 기반으로 추억의 인기영화를 추천해주는 추천 기능
  - 사용자가 선호하는 장르를 기반으로 n년 전의 영화를 추천해준다.
  - 평점 7점 이상의 영화를 받아온다.
  
데이터베이스 모델링 (ERD)
-

영화 추천 알고리즘에 대한 기술적 설명
-

핵심 기능에 대한 설명


생성형 AI를 활용한 부분
- 배경 이미지

느낀점, 후기
김동철:

김예현:

배포 서버 URL
-

---

