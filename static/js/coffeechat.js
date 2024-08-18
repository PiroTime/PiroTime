window.onload = function() {
    var modal = document.getElementById("myModal");
    var btn = document.getElementById("openModalBtn");
    var span = document.getElementById("coffeechat-modal-close");

    btn.onclick = function() {
        modal.style.display = "flex";
    }

    // 모달 닫기 (X 버튼 클릭 시)
    span.onclick = function() {
        modal.style.display = "none";
    }

    // 모달 닫기 (모달 외부 클릭 시)
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
};

document.addEventListener("DOMContentLoaded", function() {
    // 모달 관련 변수 정의
    const modal = document.getElementById("coffeechatModal");
    const modalContent = document.getElementById("coffeechatModalContent");
    const closeModalBtn = document.getElementById("coffeechatModalClose");

    // "커피챗 문구보기" 버튼 클릭 시 모달 열기
    document.addEventListener('click', function(event) {
        if (event.target.classList.contains('btn-view-letter')) {
            const letterContent = event.target.getAttribute('data-letter');
            const urlRej = event.target.getAttribute('data-url-rej');
            const urlAcc = event.target.getAttribute('data-url-acc');
            console.log("+++++++++++++++++++++++++");
            console.log(urlRej);
            console.log(urlAcc);
            console.log(letterContent);

            modalContent.innerHTML = `
                <p>${letterContent.replace(/\r?\n/g, '<br>')}</p>
                <button type="button" class="btn-accept modal-accept" data-url="${urlAcc}">Accept</button>
                <button type="button" class="btn-reject modal-reject" data-url="${urlRej}">Reject</button>
            `;
            modal.style.display = "flex";
        }
    });

    // 모달 닫기 (X 버튼 클릭 시)
    closeModalBtn.onclick = function() {
        modal.style.display = "none";
    }

    // 모달 닫기 (모달 외부 클릭 시)
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
});