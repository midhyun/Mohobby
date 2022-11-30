var id = document.querySelector('#id');
var pw1 = document.querySelector('#pswd1');
var pw2 = document.querySelector('#pswd2');
var error = document.querySelectorAll('.error_next_box');

id.addEventListener("focusout", checkId);
pw1.addEventListener("focusout", checkPw);
pw2.addEventListener("focusout", comparePw);

function checkId() {
    if(id.value === "") {
        error[0].innerHTML = "필수 정보입니다.";
        error[0].style.color = "red";
        error[0].style.display = "block";
        error[0].style.fontSize = "12px";
    } else {
        error[0].innerHTML = "사용 가능합니다.";
        error[0].style.color = "#08A600";
        error[0].style.display = "block";
        error[0].style.fontSize = "12px";
    }
}

function checkPw() {
    var pwPattern = /[a-zA-Z0-9~!@#$%^&*()_+|<>?:{}]{8,16}/;
    if(pw1.value === "") {
        error[1].innerHTML = "필수 정보입니다.";
        error[1].style.display = "block";
        error[1].style.color = "red";
        error[1].style.fontSize = "12px";
    } else if(!pwPattern.test(pw1.value)) {
        error[1].innerHTML = "8~16자 영문 대 소문자, 숫자, 특수문자를 사용하세요.";
        error[1].style.display = "block";
    } else {
        error[1].style.display = "block";
        error[1].innerHTML = "사용 가능합니다.";
        error[1].style.color = "#08A600";
    }
}

function comparePw() {
    if(pw2.value === pw1.value && pw2.value != "") {
        error[2].style.display = "none";
    } else if(pw2.value !== pw1.value) {
        error[2].innerHTML = "비밀번호가 일치하지 않습니다.";
        error[2].style.display = "block";
        error[2].style.color = "red";
        error[2].style.fontSize = "12px";
    } 

    if(pw2.value === "") {
        error[2].innerHTML = "필수 정보입니다.";
        error[2].style.display = "block";
        error[2].style.color = "red";
        error[2].style.fontSize = "12px";
    }
}