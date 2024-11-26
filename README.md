MovieMemory README
---

![001](https://github.com/user-attachments/assets/caebfe7f-ad9c-4be3-b339-b440cbeb3230)
![002](https://github.com/user-attachments/assets/e02eb3a4-2624-47ce-bd03-3ca6965fe943)
![003](https://github.com/user-attachments/assets/fcd237d8-4d1c-4c76-a40c-89b0f054d235)
![004](https://github.com/user-attachments/assets/342a9916-1f1f-46cd-a1f9-80f1dddc55c2)
![005](https://github.com/user-attachments/assets/84b91265-2d1d-4e36-ac92-95989108d25c)
![006](https://github.com/user-attachments/assets/bb5200df-1c35-4e6d-8e45-3ee453c2e6c6)
![007](https://github.com/user-attachments/assets/ebc12ff8-2df5-417f-aebd-7c9b62c9befe)
![008](https://github.com/user-attachments/assets/78e3a48c-cd9f-4a98-96b0-5084285620b8)
![009](https://github.com/user-attachments/assets/f9ac5f92-d899-4873-b597-d358d74239d0)
![010](https://github.com/user-attachments/assets/85ceb89f-ef8a-496f-bc0f-4efd351f15c7)
[시연영상](https://drive.google.com/file/d/1Zhg-8byNA31KEbq9-rBT3jUDQzNEPr-R/view?usp=sharing)
![011](https://github.com/user-attachments/assets/e812e683-8413-4778-9d52-45625ad3316c)
![012](https://github.com/user-attachments/assets/39d7056e-83b7-4f80-937e-9106dcd06ee3)
![013](https://github.com/user-attachments/assets/c55ad965-d9bf-436d-85e2-1377de5ca7f7)

---

# README with Text

### 3조
팀원 정보 및 업무 분담 내역

**팀장: 김동철**
- 담당한 작업: movies, reviews모델 구현, 추천 알고리즘 구현

**팀원: 김예현**
- 담당한 작업: accounts, communities 앱, movies의 프로필 관리

목표 서비스 구현 및 실제 구현 정도
- 영화 사이트 + 추천 알고리즘, 커뮤니티(대나무 숲)
- 소셜 로그인
- 유저간 소통할 수 있는 커뮤니티 구현

김동철
| No. | 기능                                   | 구현여부 |
| --- | -------------------------------------- | -------- |
| 1   | 영화상세(detail)                       | O        |
| 2   | 영화스크랩(좋아요)                     | O        |
| 3   | 영화검색(search)                       | O        |
| 4   | 영화 추천 알고리즘(memory)             | O        |
| 5   | 리뷰 CRUD                              | O        |
| 6   | 영화 스크랩                            | O        |
| 7   | 리뷰코멘트생성, 삭제(비동기)           | O        |

김예현
| No. | 기능                                   | 구현여부 |
| --- | -------------------------------------- | -------- |
| 1   | 로그인, 로그아웃, 회원가입, 회원탈퇴   | O        |
| 2   | 프로필, 개인정보수정, 비밀번호변경     | O        |
| 3   | 선호 장르 설정, 작성글/댓글 목록 관리, 공개여부 결정 | O        |
| 4   | 소셜로그인(카카오톡)                   | O        |
| 5   | 커뮤니티(영화 게시판)                  | O        |
| 6   | 커뮤니티(대나무숲)                     | O        |
| 7   | 커뮤니티(이벤트 게시판)                | X        |

  
데이터베이스 모델링 (ERD)
![generated (1)](https://github.com/user-attachments/assets/b4bca1cc-9e75-419b-9858-e2c9ec6578ef)# project1

영화 추천 알고리즘에 대한 기술적 설명
- 사용자 나이 및 선호 장르 기반으로 추천 알고리즘 구현
   - 사용자의 0~20살 까지 나왔던 영화
   - 선호장르
   - 투표수 200이상
   - 평점 7이상 

사용한 프레임워크
   - Django + VanillaJs


생성형 AI를 활용한 부분
- 배경 이미지, fixtures생성, fixtures user프로필 사진 생성, 로고
- detail부분 댓글 비동기 처리, css
- 카카오 로그인 구현 부문 오류 수정
- 자동으로 fixtures 로딩하는 기능
- css 충돌 해결

느낀점, 후기

김동철: 
- Django와 JavaScript 부분을 복습할 수 있는 좋은 시간이었다고 생각합니다.
- ChatGPT가 유용하지만 사용자의 역량에 따라 더 좋은 방향을 제시할 수 있다는 것을 깨달았습니다.
- 초기 모델 작성의 중요성을 깨달았습니다.

김예현:
- 카카오 로그인 구현 과정에서 여러 어려움을 겪었지만, 그만큼 값진 경험을 얻을 수 있었습니다. 처음에는 단순히 로그인 기능만 구현하려다 실패하기도 했고, 사용자 모델에 테이블을 추가해야했기 때문에 아예 처음부터 카카오 로그인을 다시 구현해야했던 일도 있었습니다. 이런 과정을 거치는 도중에 많이 힘들었지만, 모든 기능을 완성했을 때 느꼈던 뿌듯함은 이루 말할 수 없었습니다.
- 스타일링 도중에 ChatGPT를 많이 사용했는데 디자인 면에서 일관성을 유지하려면 사람이 직접 손을 보는게 더 낫다는 생각이 많이 들었습니다. 
- 프로젝트를 진행하면서 몰랐던 기능들을 찾아보고, 이전에 알았지만 까먹었던 부분들을 다시 떠올릴 수 있었던 것도 큰 도움이 되었습니다. 작업을 하다 보니 REST API를 제대로 활용하지 않았던 점이 아쉽다는 생각이 들었습니다. 처음에는 REST API를 굳이 사용할 필요가 없을거라고 생각했지만, 시간이 갈수록 기능 확장성과 작업 효율성 면에서 REST API를 사용했더라면 훨씬 더 수월했을 것 같아 후회가 남았습니다.
- Vue와 Django를 함께 사용하며 어려움을 많이 겪었기 때문에 이번에는 Django와 Vanilla JS를 조합해 진행했는데 예상 이상으로 작업량이 많고 번거로운 부분이 많았습니다. 그래도 이러한 시행착오를 통해 많은 것들을 배울 수 있었고, 다음에 Django를 사용할 기회가 생긴다면 이번 경험을 바탕으로 REST API와 Vue를 적극 활용해보고 싶습니다.
- 힘들었던 순간들도 돌아보니 모두 성장의 밑거름이 되었고, 이번 경험은 앞으로 개발을 이어가는 데 큰 자산이 될 것 같습니다.

---
