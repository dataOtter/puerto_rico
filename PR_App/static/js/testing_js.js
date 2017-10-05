$(document).ready(function(){

    $("#filter_button").click(function(){
        alert("Hi there!");

        //$("#div1").load("PR_App/static/js/ajax_load_test.txt");

        $.ajax({url: "http://localhost:63342/puerto_rico/PR_App/static/js/ajax_load_test.txt", success: function(result){
            $("#div1").html(result);
        }});

        alert("Here we are!");
    });
});