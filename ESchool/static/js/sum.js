var inputs = document.getElementsByTagName("input");//获取所有的input标签对象
var checkboxArray = [];//初始化空数组，用来存放checkbox对象。
for (var i = 0; i < inputs.length; i++) {
    var obj = inputs[i];
    if (obj.type == 'checkbox') {
        checkboxArray.push(obj);
    }
}

var count = document.getElementById('sum');
var money = document.getElementById('money')

for (var i = 0; i < checkboxArray.length; i++) {
    checkboxArray[i].onclick = function () {
        var shuju = this.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling;
        var shuliang = shuju.lastElementChild;
        if (this.checked) {  // 如果选中
            count.innerText = parseInt(count.innerText) + 1;
            shuliang.value = '1';
            shuliang.disabled = '';
        } else {
            count.innerText = parseInt(count.innerText) - 1;
            shuliang.value = '0';
            shuliang.disabled = 'true';
        }
    }
}


var shuliangs = document.getElementsByClassName('buyn')
for (var i = 0; i < shuliangs.length; i++) {
    shuliangs[i].onblur = function () {
        var danjia = this.previousElementSibling;
        money.innerHTML = parseFloat(money.innerHTML) + parseInt(this.value) * parseFloat(danjia.innerHTML)
    }
}






































