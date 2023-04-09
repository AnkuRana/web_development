function throwdice(){
    var dice_no = Math.floor(Math.random() * 6) + 1;
    // var heading = document.querySelector("h1")[0].innerHTML
    return dice_no;
}

function check_winner(){
    var player_1 = throwdice();
    var player_2 = throwdice();
    var dice_1, dice_2;
    dice_1 = "./images/dice" + player_1 + ".png";
    dice_2 = "./images/dice" + player_2 + ".png";
    var images = document.getElementsByTagName("img")
    images[0].setAttribute("src", dice_1);
    images[1].setAttribute("src", dice_2);
    if (player_1 > player_2){
        document.querySelector("h1").innerHTML = "Player 1 wins.";
    }else if (player_1 < player_2){
        document.querySelector("h1").innerHTML = "Player 2 wins.";
    }else{
        document.querySelector("h1").innerHTML = "Draw!!!.";
    }
}