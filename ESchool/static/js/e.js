var list = document.getElementsByClassName("imgs");
var img = document.getElementById("big_image");
var div = document.getElementById("big_img");
document.getElementById("btn_close").onclick = function () {
    div.style.display = "none";
};
for (var i = 0; i < list.length; i++) {
    list[i].onclick = iii;
}

function iii() {
    open(this);
}

function open(elem) {
    img.setAttribute("src", elem.getAttribute("src"));
    div.style.display = "block";
}