var modal = document.getElementById("myModal");
var btn = document.getElementById("openModalBtn");
var span = document.getElementsByClassName("close")[0];

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