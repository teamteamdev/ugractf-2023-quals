////////////////////////
///////// Настройки
////////////////////////
 
// количество снежинок, которое будет на экране одновременно.
let snowmax=40
 
// Цвета для снежинок. Для каждой конкретной снежинки цвет выбирается случайно из этого массива.
let snowcolor=new Array("#b9dff5","#7fc7ff","#7fb1ff","#7fc7ff","#b9dff5")
 
// Шрифт для снежинок
let snowtype=new Array("Times")
 
// Символ (*) и есть снежинка, в место нее можно вставить любой другой символ.
let snowletter="&#10052;"
 
// Скорость движения снежинок (от 0.3 до 2)
let sinkspeed=0.4
 
// Максимальный размер для снежинок
let snowmaxsize=40
 
// Минимальный размер для снежинок
let snowminsize=10
 
// Зона для снежинок
// 1 для всей страницы, 2 в левой части страницы
// 3 в центральной части, 4 в правой части страницы
let snowingzone=1
 
////////////////////////
///////// Конец настроек
////////////////////////
 
let snow=new Array();
let marginbottom;
let marginright;
let timer;
let i_snow=0;
let x_mv=new Array();
let crds=new Array();
let lftrght=new Array();
function randommaker(range) {
    rand=Math.floor(range*Math.random());
    return rand;
}
function initsnow() {
    marginbottom = document.documentElement.clientHeight+50
    marginright = document.body.clientWidth-15
    let snowsizerange=snowmaxsize-snowminsize
    for (i=0;i<=snowmax;i++) {
        crds[i] = 0;
        lftrght[i] = Math.random()*15;
        x_mv[i] = 0.03 + Math.random()/10;
        snow[i]=document.getElementById("s"+i)
        snow[i].style.fontFamily=snowtype[randommaker(snowtype.length)]
        snow[i].size=randommaker(snowsizerange)+snowminsize
        snow[i].style.fontSize=snow[i].size+'px';
        snow[i].style.color=snowcolor[randommaker(snowcolor.length)]
        snow[i].style.zIndex=1000
        snow[i].sink=sinkspeed*snow[i].size/5
        if (snowingzone==1) {snow[i].posx=randommaker(marginright-snow[i].size)}
        if (snowingzone==2) {snow[i].posx=randommaker(marginright/2-snow[i].size)}
        if (snowingzone==3) {snow[i].posx=randommaker(marginright/2-snow[i].size)+marginright/4}
        if (snowingzone==4) {snow[i].posx=randommaker(marginright/2-snow[i].size)+marginright/2}
        snow[i].posy=randommaker(2*marginbottom-marginbottom-2*snow[i].size)
        snow[i].style.left=snow[i].posx+'px';
        snow[i].style.top=snow[i].posy+'px';
    }
    movesnow()
}
function movesnow() {
    for (i=0;i<=snowmax;i++) {
        crds[i] += x_mv[i];
        snow[i].posy+=snow[i].sink
        snow[i].style.left=snow[i].posx+lftrght[i]*Math.sin(crds[i])+'px';
        snow[i].style.top=snow[i].posy+'px';
        
        if (snow[i].posy>=marginbottom-2*snow[i].size || parseInt(snow[i].style.left)>(marginright-3*lftrght[i])){
            if (snowingzone==1) {snow[i].posx=randommaker(marginright-snow[i].size)}
            if (snowingzone==2) {snow[i].posx=randommaker(marginright/2-snow[i].size)}
            if (snowingzone==3) {snow[i].posx=randommaker(marginright/2-snow[i].size)+marginright/4}
            if (snowingzone==4) {snow[i].posx=randommaker(marginright/2-snow[i].size)+marginright/2}
            snow[i].posy=0
        }
    }
    let timer=setTimeout("movesnow()",50)
}
 
for (i=0;i<=snowmax;i++) {
    document.body.insertAdjacentHTML("beforeend", "<span id='s"+i+"' style='pointer-events:none;user-select:none;position:fixed;top:-"+snowmaxsize+"'>"+snowletter+"</span>")
}
document.addEventListener('DOMContentLoaded', initsnow)
