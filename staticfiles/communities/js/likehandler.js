document.addEventListener("DOMContentLoaded", function () {
    const likeButtons = document.querySelectorAll("#like-button, #like-button-bamboo");  // 여러 like-button 선택
  
    likeButtons.forEach(function (likeButton) {
        likeButton.addEventListener("click", function () {
            const url = likeButton.getAttribute("data-url");
            const post_id = likeButton.getAttribute("data-post-id");  // post_id 가져오기
  
            if (!post_id) {
                console.error("post_id가 없습니다.");
                alert("잘못된 요청입니다.");
                return;
            }
  
            const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  
            likeButton.disabled = true;  // 버튼 비활성화
  
            fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrftoken,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    post_id: post_id  // post_id를 서버로 전송
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                } else {
                    // 좋아요 수 업데이트
                    const likeCountElement = document.getElementById(`like-count-${data.post_id}`);
                    if (likeCountElement) {
                        likeCountElement.textContent = data.likes_count;
                    }
  
                    // 버튼 텍스트 및 상태 업데이트
                    likeButton.textContent = `좋아요 ❤️ ${data.likes_count}`;
                    if (data.liked) {
                        likeButton.classList.add("liked");
                    } else {
                        likeButton.classList.remove("liked");
                    }
                }
            })
            .catch(error => {
                console.error("Error liking post:", error);
                alert("좋아요 처리 중 오류가 발생했습니다. 다시 시도해주세요.");
            })
            .finally(() => {
                likeButton.disabled = false;  // 버튼 다시 활성화
            });
        });
    });
  });
  