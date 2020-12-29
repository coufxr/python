var li = $(".nr li")
var dhbox = $(".dhbox")
li.click(function() {
	is = $(this).index(); //2
	li.eq(is).addClass("active").siblings(li).removeClass("active");
	dhbox.eq(is).addClass("act").siblings(dhbox).removeClass("act");
});

var canvas = document.getElementById('canvas');
var ctx = canvas.getContext("2d");
var width = 1170;
var height = 400;
//用数组的方法实现插入弹幕和字体的颜色
var colorArr = ["yellow", "blue", "orange", "red", "green", "pink", "black", "darkblue", "purple", "yellow", "blue",
	"orange", "red", "green", "pink", "purple", "blue", "yellow", "purple"
];
var textArr = ["圣诞节来了！！！", "四年前那个夜晚,", "还记得么？", "二十四硬币的故事，", "依旧像当初平安夜的苹果一样新鲜。", "短暂又漫长的时光，", "转眼间第四个圣诞节来临了。",
	"在经过了1460个夜晚之后主角仍然是你，", "不同的是配角已换。", "当自己回首小诗一般的过去的时候，", "突然间发现，", "我们已经隔得很远很远，", "远的遥不可望。", "封陈的记忆阻隔了我们通讯的联系，",
	"却没法剥离我欲穿的望眼。", "博客里的日志成了我偷看你唯一的窗口，", "或许除了自己以外谁都不会知道，", "满心的祝福换来的是自己的失落，", "圣诞节又来了，", "圣诞节快乐！！！"
];
canvas.width = width;
canvas.height = height;
ctx.font = "24px Courier New"; //字体大小和字样
var numArrL = [400, 500, 700, 430, 1000, 400, 600, 500, 500, 700, 430, 800, 850]; //初始的X
var numArrT = [50, 70, 100, 130, 150, 360, 230, 320, 200, 270, 340, 300, 180, 50, 240, ]; //初始的Y
//setInterval实现动态效果
setInterval(function() {
	ctx.clearRect(0, 0, canvas.width, canvas.height); //清除矩形的区域（x:起点横坐标,y:起点纵坐标,长度，宽度）
	ctx.save(); //保存当前环境的状态
	for (var j = 0; j < textArr.length - 1; j++) {
		numArrL[j] -= (j + 1) * 0.6;
		ctx.fillStyle = colorArr[j] //填充样式：颜色
		ctx.fillText(textArr[j], numArrL[j], numArrT[j]); //填充文字
	}
	for (var i = 0; i < textArr.length - 1; i++) {
		if (numArrL[i] <= -500) {
			numArrL[i] = canvas.width; //如果长度小于等于500,画布宽度都是已设置的宽度
		}
	}
	ctx.restore(); //返回之前保存过的路径状态和属性
}, 10) //每个30秒显示一次

$('[data-toggle="popover"]').popover();
// 	$("#myModal").modal(options);