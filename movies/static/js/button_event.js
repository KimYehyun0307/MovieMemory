let selectedGenres = [];

function selectGenre(button) {
    const genreId = button.getAttribute('data-genre-id');

    // 이미 선택한 장르가 3개 이상일 경우 경고 메시지
    if (selectedGenres.length >= 3 && !selectedGenres.includes(genreId)) {
        alert("최대 3개의 장르만 선택할 수 있습니다.");
        return;
    }

    // 장르가 이미 선택되어 있으면 취소
    if (selectedGenres.includes(genreId)) {
        // 선택한 장르 삭제
        selectedGenres = selectedGenres.filter(id => id !== genreId);

        // 버튼에서 'btn-selected' 클래스 제거
        button.classList.remove('btn-selected', 'btn-gold', 'btn-silver', 'btn-bronze');
        
        // 숨겨진 입력 필드에서 값 삭제
        const index = selectedGenres.indexOf(genreId) + 1;
        const genreInputField = document.getElementById(`genre_${index}`);
        if (genreInputField) {
            genreInputField.value = ''; // 입력 필드가 존재하면 값 삭제
        }

        // 선택된 장르가 다시 3개 미만이 되면, 모든 버튼을 재정렬
        reorderButtons();
        
        return;
    }

    // 장르가 아직 선택되지 않았다면 선택
    selectedGenres.push(genreId);

    // 'btn-selected' 클래스 추가
    button.classList.add('btn-selected');

    // 색상 변경
    if (selectedGenres.length === 1) {
        button.classList.add('btn-gold');  // 금색
    } else if (selectedGenres.length === 2) {
        button.classList.add('btn-silver');  // 은색
    } else if (selectedGenres.length === 3) {
        button.classList.add('btn-bronze');  // 동색
    }

    // 숨겨진 입력 필드에 값 설정
    const genreInputField = document.getElementById(`genre_${selectedGenres.length}`);
    if (genreInputField) {
        genreInputField.value = genreId;
    }

    // 3개를 다 선택했다면 나머지 버튼을 비활성화
    if (selectedGenres.length === 3) {
        const allButtons = document.querySelectorAll('#genre-buttons button');
        allButtons.forEach(btn => {
            if (!btn.classList.contains('btn-selected')) {
                btn.classList.add('btn-disabled');  // 선택되지 않은 버튼을 비활성화 스타일로 변경
            }
        });
    }
}

// 장르 버튼 순서를 재정렬하는 함수
function reorderButtons() {
    // 선택된 장르 버튼들의 순서를 재정렬
    const allButtons = document.querySelectorAll('#genre-buttons button');
    let reorderedGenres = selectedGenres.slice(); // 선택된 장르 목록
    
    // 모든 버튼의 상태를 초기화
    allButtons.forEach(btn => {
        btn.classList.remove('btn-gold', 'btn-silver', 'btn-bronze', 'btn-selected', 'btn-disabled');
    });

    // 선택된 장르 순서대로 색상 변경
    reorderedGenres.forEach((genreId, index) => {
        const button = [...allButtons].find(btn => btn.getAttribute('data-genre-id') === genreId);
        if (index === 0) button.classList.add('btn-gold');
        else if (index === 1) button.classList.add('btn-silver');
        else if (index === 2) button.classList.add('btn-bronze');
        button.classList.add('btn-selected');  // 선택된 버튼에 'btn-selected' 클래스 추가
    });

    // 숨겨진 입력 필드에 선택된 장르 순서 반영
    reorderedGenres.forEach((genreId, index) => {
        const genreInputField = document.getElementById(`genre_${index + 1}`);
        if (genreInputField) {
            genreInputField.value = genreId;
        }
    });
}
