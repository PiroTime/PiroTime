window.onload = function() {
    // myModal 관련 변수 정의
    var myModal = document.getElementById("myModal");
    var btn = document.getElementById("openModalBtn");
    var myModalClose = document.getElementById("coffeechat-modal-close");

    btn.onclick = function() {
        myModal.style.display = "flex";
    }

    myModalClose.onclick = function() {
        myModal.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target == myModal) {
            myModal.style.display = "none";
        }
    }
};

document.addEventListener("DOMContentLoaded", function() {
    // coffeechatModal 관련 변수 정의
    const coffeechatModal = document.getElementById("coffeechatModal");
    const coffeechatModalContent = document.getElementById("coffeechatModalContent");
    const coffeechatCloseBtn = document.getElementById("coffeechatModalClose");

    document.addEventListener('click', function(event) {
        if (event.target.classList.contains('btn-view-letter')) {
            const letterContent = event.target.getAttribute('data-letter');
            const urlRej = event.target.getAttribute('data-url-rej');
            const urlAcc = event.target.getAttribute('data-url-acc');

            coffeechatModalContent.innerHTML = `
                <p>${letterContent.replace(/\r?\n/g, '<br>')}</p>
                <button type="button" class="btn-accept modal-accept" data-url="${urlAcc}">Accept</button>
                <button type="button" class="btn-reject modal-reject" data-url="${urlRej}">Reject</button>
            `;
            coffeechatModal.style.display = "flex";
        }


    });

    coffeechatCloseBtn.onclick = function() {
        coffeechatModal.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target == coffeechatModal) {
            coffeechatModal.style.display = "none";
        }
    }

    document.getElementById('profile_modal').addEventListener('click', function(event) {
        if (event.target.classList.contains('close-button') || event.target.id === 'profile_modal') {
            document.getElementById('profile_modal').style.display = "none";
            toggleModalCSS(false);  // CSS 파일 제거
        }
    });
});

function toggleModalCSS(load) {
    const modalCSSId = 'modal-css';
    if (load) {
        if (!document.getElementById(modalCSSId)) {
            var link = document.createElement('link');
            link.rel = 'stylesheet';
            link.href = '{% static "css/mypage/profile_modal.css" %}';
            link.id = modalCSSId;
            document.head.appendChild(link);
        }
    } else {
        var link = document.getElementById(modalCSSId);
        if (link) {
            document.head.removeChild(link);
        }
    }
}