
// $(document).keypress(function(event){
//     $("h1").addClass("text-color");
//     $("h1").text(event.key);
// });

$(document).on("keypress", function(event){
    $("h1").addClass("text-color");
    $("h1").text(event.key);
});