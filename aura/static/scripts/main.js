/*$(function init() {

	$('#btStart').click(function(){
	
		require(["util"], function (util) {
		console.log("init");
		
		randomArr(arr);
		
		randomArrCards(arrCards);
		
		randomPositions(positions);
		
		
		//var typc = document.getElementById('typ_c');
		//typc.firstChild.data=arr;
		
		//var masc = document.getElementById('mas_c');
		//masc.firstChild.data=arrCards;
		
		//var posc = document.getElementById('pos_c');
		//posc.firstChild.data=positions;
		
		InitCards(Cards);
		
		Start();
	});})

});*/


$(document).ready(function(){
	$(".btStart").click(function(){go();});
	$(".btStop").click(function(){window.location.reload();});
})


function go()
{
	randomArr(arr);
	randomArrCards(arrCards);
	randomPositions(positions);
	InitCards(Cards);
	Start();
}



var clickedID;

var gameStarted=0;

var clicked1=-1;//номер значения первой нажатой карты
var clicked1ID="";//индекс первой нажатой карты
var clicked2=-1;//номер значения второй нажатой карты
var clicked2ID="";//индекс второй нажатой карты


var arr = Array(0,0,0,0,0,0,0,0);
var arrCards = Array([0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]);
var positions = Array([0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]);
var Cards=Array(
["static/images/game/bub2.png","static/images/game/tref2.png","static/images/game/heart2.png","static/images/game/pick2.png"],
["static/images/game/bub3.png","static/images/game/tref3.png","static/images/game/heart3.png","static/images/game/pick3.png"],
["static/images/game/bub4.png","static/images/game/tref4.png","static/images/game/heart4.png","static/images/game/pick4.png"],
["static/images/game/bub5.png","static/images/game/tref5.png","static/images/game/heart5.png","static/images/game/pick5.png"],
["static/images/game/bub6.png","static/images/game/tref6.png","static/images/game/heart6.png","static/images/game/pick6.png"],
["static/images/game/bub7.png","static/images/game/tref7.png","static/images/game/heart7.png","static/images/game/pick7.png"],
["static/images/game/bub8.png","static/images/game/tref8.png","static/images/game/heart8.png","static/images/game/pick8.png"],
["static/images/game/bub9.png","static/images/game/tref9.png","static/images/game/heart9.png","static/images/game/pick9.png"],
["static/images/game/bub10.png","static/images/game/tref10.png","static/images/game/heart10.png","static/images/game/pick10.png"],
["static/images/game/bubJ.png","static/images/game/trefJ.png","static/images/game/heartJ.png","static/images/game/pickJ.png"],
["static/images/game/bubQ.png","static/images/game/trefQ.png","static/images/game/heartQ.png","static/images/game/pickQ.png"],
["static/images/game/bubK.png","static/images/game/trefK.png","static/images/game/heartK.png","static/images/game/pickK.png"],
["static/images/game/bubA.png","static/images/game/trefA.png","static/images/game/heartA.png","static/images/game/pickA.png"]);


function randomArr(arr)//выбирает пары
{ 
	for(var i=0;i<8;i++)
	{
		var y=1;
        while(y!=0)
        {
            y=0;
        
            rand=Math.round(Math.random() * 13)%13;
            for(var l=0;l<8;l++)//просматривает весь массив
			{
                if(arr[l]==rand)//если хоть одна ячейка уже заполнена этим числом
                    y=1;
			}
							
            if(y==0)
				arr[i]=rand;
        } 
    }
}


function randomArrCards(arrCards)
{
	for(var i=0;i<8;i++)
	{
		for(var j=0;j<2;j++)
		{
			var y=1;
			while(y!=0)
			{
				y=0;
        
				rand=Math.round(Math.random() * 4)%4;//исключая 0
			
				if(j!=0)
					if(arrCards[i][j-1]==rand)//если хоть одна ячейка уже заполнена этим числом
						y=1;
			
				if(y==0)//если же y по-прежнему равен 0
				arrCards[i][j]=rand;
			} 
		}
	}
}


function randomPositions(positions)
{
	//positions.clear();
	//positions = Array([0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]);
	
	for(var i=0;i<8;i++)
	{
		for(var j=0;j<2;j++)
		{
			var y=1;
			while(y!=0)//пока игрек не равен 0
            {
				y=0;
        
				rand=Math.round(Math.random() * 16)%16+1;
				for(var l=0;l<8;l++)//просматривает весь массив
					for(var g=0;g<2;g++)
                    {
						if(positions[l][g]==rand)//если хоть одна ячейка уже заполнена этим числом
							y=1; //ставим единицу
                    }
				if(y==0)//если же y по-прежнему равен 0
				positions[i][j]=rand;
            }
		}
	}
}


function InitCards(Cards) 
{
    var image;
	var backImage;
	
	for(var i=0;i<8;i++)//просматривает весь массив
	{
		for(var j=0;j<2;j++)
        {
			var row=parseInt((positions[i][j]-1) / 4);//нахождение номера строки, соответствующей позиции карты
			var column=positions[i][j]-row*4-1;//нахождение номера столбца, соответствующей позиции карты
			
			var imageID=row+'-'+column;//получение индекса изображения карты
			var backImageID='b'+imageID;//получение индекса изображения рубашки этой карты
			
			image=document.getElementById(imageID);
			image.src=Cards[arr[i]][arrCards[i][j]];
			backImage=document.getElementById(backImageID);
			backImage.title=arr[i];
        }
	}
} 

var findPares=0;//количество найденных пар
var doed=1;//запущена ли игра
var clickPause=0;//включена ли блокировка нажатия карты (во время задержки показа несовпадающей карты), чтобы не держать нажатыми более двух карт

  
function simple_timer(tm, block, direction)
{
    var time    = tm;
	
	var min    = parseInt(time / 6000);
    if ( min < 1 ) min = 0;
    time = parseInt(time - min * 6000);
    if ( min < 10 ) min = '0'+min;
 
    var sec = parseInt(time / 100);
    if ( sec < 1 ) sec = 0;
    time = parseInt(time - sec * 100);
    if ( sec < 10 ) sec = '0'+sec;
 
    var subsec = time;
    if ( subsec < 10 ) subsec = '0'+subsec;
	
	
	if(doed==0)//если все карты открыты
	{
		alert('Вы успели! Ваше время: '+(39-sec)+'.'+(99-subsec)+' секунд.');
	}
	
	else//если остались неоткрытые карты
	{
		//block.innerHTML = hour+':'+minutes+':'+seconds;
		block.innerHTML = min+':'+sec+':'+subsec;
 
		if ( direction )
		{
			tm++;
	
			setTimeout(function(){ simple_timer(tm, block, direction); }, 1000);
		}
		else
		{
			tm--;
 
			if ( tm > 0 )
			{
				//setTimeout(function(){ simple_timer(sec, block, direction); }, 1000);
				setTimeout(function(){ simple_timer(tm, block, direction); }, 10);
			}
			else
			{
				gameStarted=0;//отметить, что игра окончена
				block.innerHTML = min+':'+sec+':00';
				alert('Время вышло!');
				doed=0;
				//block.innerHTML = hour+':'+minutes+':'+sec;
			}
		}
	}
}

function returnCard()//поворачивает карты рубашкой вверх в случае их несовпадения
{
	var back;
	
	back=document.getElementById(clicked1ID);
	back.hidden=false;
	
	back=document.getElementById(clicked2ID);
	back.hidden=false;
	
	clicked1=-1;
	clicked1ID="";
	
	clicked2=-1;
	clicked2ID="";
	
	clickPause=0;//снять блокировку нажатия карты
}
  
  
 function onMouseDown(clickedID)
 {
	if(clickPause==0)//если нет блокировки нажатия карты
	{
		var clickedBack=document.getElementById(clickedID);
		clickedBack.hidden=true;
	
	
		if(clicked1==-1)//если первая карта не открыта
		{
			clicked1=clickedBack.title;
			clicked1ID=clickedID;
		}
		else//если первая карта открыта
		{
			clicked2=clickedBack.title;
			clicked2ID=clickedID;
		
			if(clicked2==clicked1)//если перевёрнутые карты совпали
			{
				clicked1=-1;
				clicked1ID="";
	
				clicked2=-1;
				clicked2ID="";
			
				findPares++;//увеличить количество найденных пар
			
				if(findPares==8)//если открыто 8 пар
					doed=0;//остановить игру
			}
			else//если перевёрнутые карты не совпали
			{
				clickPause=1;
		
				setTimeout(function(){ returnCard(); }, 500);
			}
		}
	}
}
  
  
 function Start()
 {
	gameStarted=1;
 
	var block = document.getElementById('timerBoard');//индекс блока вывода для таймера
    setTimeout(simple_timer(4000, block), 1000);//запуск таймера
	
	
	$('#b0-0').click(
		function()
		{
			clickedID='b0-0';
			onMouseDown(clickedID);
		}
	);
	
	$('#b0-1').click(
		function()
		{
			clickedID='b0-1';
			onMouseDown(clickedID);
		}
	);
	
	$('#b0-2').click(
		function()
		{
			clickedID='b0-2';
			onMouseDown(clickedID);
		}
	);
	
	$('#b0-3').click(
		function()
		{
			clickedID='b0-3';
			onMouseDown(clickedID);
		}
	);
	
	$('#b1-0').click(
		function()
		{
			clickedID='b1-0';
			onMouseDown(clickedID);
		}
	);
	
	$('#b1-1').click(
		function()
		{
			clickedID='b1-1';
			onMouseDown(clickedID);
		}
	);
	
	$('#b1-2').click(
		function()
		{
			clickedID='b1-2';
			onMouseDown(clickedID);
		}
	);
	
	$('#b1-3').click(
		function()
		{
			clickedID='b1-3';
			onMouseDown(clickedID);
		}
	);
	
	$('#b2-0').click(
		function()
		{
			clickedID='b2-0';
			onMouseDown(clickedID);
		}
	);
	
	$('#b2-1').click(
		function()
		{
			clickedID='b2-1';
			onMouseDown(clickedID);
		}
	);
	
	$('#b2-2').click(
		function()
		{
			clickedID='b2-2';
			onMouseDown(clickedID);
		}
	);
	
	$('#b2-3').click(
		function()
		{
			clickedID='b2-3';
			onMouseDown(clickedID);
		}
	);
	
	$('#b3-0').click(
		function()
		{
			clickedID='b3-0';
			onMouseDown(clickedID);
		}
	);
	
	$('#b3-1').click(
		function()
		{
			clickedID='b3-1';
			onMouseDown(clickedID);
		}
	);
	
	$('#b3-2').click(
		function()
		{
			clickedID='b3-2';
			onMouseDown(clickedID);
		}
	);
	
	$('#b3-3').click(
		function()
		{
			clickedID='b3-3';
			onMouseDown(clickedID);
		}
	);
	
 }
