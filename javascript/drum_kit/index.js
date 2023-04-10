var buttons = document.querySelectorAll(".drum")

//To listen to button press.
for (let index = 0; index < buttons.length; index++) {
    buttons[index].addEventListener("click", function() {
        this.style.color = "white";
        buttonAnimation(this.innerHTML);
        playSound(this.innerHTML);  
    });
}

// To listen for the key press.
document.addEventListener("keydown", function(event){
   var downKey = event.key;
   buttonAnimation(downKey);
   playSound(downKey);
});

function playSound(key){
    switch(key){
        case 'w':
            new Audio("./sounds/tom-1.mp3").play();            
            break;
        case 'a':
            new Audio("./sounds/tom-2.mp3").play();
            break;
        case 's':
            new Audio("./sounds/tom-3.mp3").play();
            break;
        case 'd':
            new Audio("./sounds/tom-4.mp3").play();
            break;
        case 'j':
            new Audio("./sounds/snare.mp3").play();
            break;
        case 'k':
            new Audio("./sounds/crash.mp3").play();
            break;
        case 'l':
            new Audio("./sounds/kick-bass.mp3").play();
            break;
        default:
            console.log("logging default response");
    }

}

function buttonAnimation(key){
    var keys = ["w","a","s","d","j","k","l"];
    if (keys.includes(key)){
        var buttonPressed = document.querySelector("." + key);
        buttonPressed.classList.add("pressed")
        setTimeout(function(){
            buttonPressed.classList.remove("pressed")
        },100)
    }else{
        console.log("Key presses does not have associated action.")
    }
    
}