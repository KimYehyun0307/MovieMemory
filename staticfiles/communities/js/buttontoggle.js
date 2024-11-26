// 대댓글 작성 폼 토글 함수
function toggleReplyForm(commentId) {
  // 댓글 ID를 사용하여 대댓글 폼을 찾음
  var replyForm = document.getElementById("reply-form-" + commentId);

  // 'hidden' 클래스를 토글하여 폼을 보이거나 숨김
  replyForm.classList.toggle('hidden');
}

