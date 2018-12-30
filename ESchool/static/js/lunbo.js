window.onload = function () {
    var list = document.getElementById("img");
    var prev = document.getElementById("prev");
    var next = document.getElementById("next");
    var timer;

    function animate(offset) {
        var newleft = parseInt(list.style.left) + offset;
        list.style.left = newleft + 'px';
        if (newleft < -7675) {
            list.style.left = -1535 + 'px';
        }
        if (newleft > -1535) {
            list.style.left = -7675 + 'px';
        }
    }

    prev.onclick = function () {
        animate(1535);
    }

    next.onclick = function () {
        animate(-1535);
    }

    function play() {
        //重复执行的定时器
        timer = setInterval(function () {
            next.onclick();
        }, 8000)
    }

    var container = document.getElementById('container');

    function stop() {
        clearInterval(timer);
    }

    container.onmouseover = stop;
    container.onmouseout = play;

    play();
}
