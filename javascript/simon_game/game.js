
var userPattern = [];
var gamePattern = []
let level = 0;

// to start the game.
$(document).on("keydown", function(){
    if(level === 0){
        nextSquence();
    }
});

function checkAnswer(curr_lvl){
    if (gamePattern[curr_lvl] === userPattern[curr_lvl]){
        if(gamePattern.length === userPattern.length){
            setTimeout(function(){
                nextSquence();
            },1000);
        }
    }else{
        $("body").addClass("game-over");
        playSound("wrong");
        $("h1").text("press any key to restart.")
        restart();
              
    }

}

function restart(){
    userPattern = [];
    gamePattern =[];
    level = 0;
    setTimeout(function(){
        $("body").removeClass("game-over");
    }, 300);
    
}
// do{

// }while(gamePattern.length != userPattern.length);
// Get random color

function pressAnimate(id){
    $("#"+ id).addClass("pressed")
    setTimeout(function(){
        $("#" + id).removeClass("pressed")
    },100);
}

function nextSquence(){
    userPattern = []
    var color = getRandomColor();
    gamePattern.push(color);
    $("#"+ color).fadeOut();
    $("#"+ color).fadeIn();
    playSound(color);
    console.log(gamePattern);
    level++;
    $("h1").text("Level " + level);
}


function getRandomColor(){
    var color = Math.floor(Math.random() * 3) + 1;
    switch(color){
        case 0:
            return "green";
        case 1:
            return "red";
        case 2:
            return "blue";
        case 3:
            return "yellow";
        default:
            break;
    }
}
// listen to all buttons
$(".btn").on("click", function(event){
    userPattern.push(event.target.id);
    
    playSound(event.target.id);
    pressAnimate(event.target.id);
    
    console.log(userPattern);
    checkAnswer(userPattern.length-1);
});


function playSound(arg){
    new Audio("./sounds/" + arg + ".mp3").play();
}