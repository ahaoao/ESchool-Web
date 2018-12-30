var div = document.getElementById("big_div");
var will_put = document.getElementById("will_put");
var put_text = document.getElementById("put");
var mytext = document.getElementById("mytext");
document.getElementById("btn_close").onclick = function () {
    div.style.display = "none";
};

will_put.onclick = function () {
    div.style.display = "block";
}

put_text.onclick = function () {
    function put_data() {

        var xhr = new XMLHttpRequest();
        xhr.open('GET', '/put_shudong.html?txt=' + mytext.value, true);
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4 && xhr.status == 200) {
                change_data(xhr.responseText);
            }
        };
        xhr.send();
    };
    put_data();
    mytext.value=""
    div.style.display = "none";
}









