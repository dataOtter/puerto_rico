/*
===============================================================

Basic syntax is: $(selector).action()

A $ sign to define/access jQuery
A (selector) to "query (or find)" HTML elements
A jQuery action() to be performed on the element(s)

$(this).hide() - hides the current element.

$("p").hide() - hides all <p> elements.

$(".test").hide() - hides all elements with class="test".

$("#test").hide() - hides the element with id="test".

https://www.w3schools.com/jquery/jquery_ref_selectors.asp

https://www.w3schools.com/jquery/jquery_ref_events.asp

===============================================================
*/
//Global:
var survey = [];
var s2 = [];

$(document).ready(function(){

    //Switcher function:
    $(".rb-tab").click(function(){
        //Spot switcher:
        $(this).parent().find(".rb-tab").removeClass("rb-tab-active");
        $(this).addClass("rb-tab-active");
    });


    $('#filter_button').click(function() {
        //Empty array:
        survey = {};
        s2 = [];
        //Push data:
        for (i=1; i<=$(".rb").length; i++) {
            var kind = $(".rb")[i-1].id;
            var rbValue = $("#"+kind).find(".rb-tab-active").attr("data-value");
            survey[kind] = rbValue;
            //survey.push([kind, rbValue]);
            //s2.push(kind + ' ' + rbValue);
        };
        var json_str_survey = JSON.stringify(survey);  // send this to python
        //alert(json_str_survey);
        //alert(survey);
        //alert("This is a test");

        $.ajax({
                type: 'POST',
                contentType: 'application/json',
                data: json_str_survey,
                url: '/testingJSON',
                success: function(response) {
                console.log("success!! " + response);
            },
            error: function(error) {
                console.log("failure!! " + error);
            }
        });


    });

});

/*
//Save data:
$(".trigger").click(function(){
  //Empty array:
  survey = [];
  s2 = [];
  //Push data:
  for (i=1; i<=$(".rb").length; i++) {
    var kind = $(".rb")[i-1].id;
    var rbValue = $("#"+kind).find(".rb-tab-active").attr("data-value");
    //Bidimensional array push:
    survey.push([kind, rbValue]); //Bidimensional array: [ [1,3], [2,4] ]
    s2.push(kind + ' ' + rbValue);
  };
  var json_str_survey = JSON.stringify(s2);  // send this to python
  alert(json_str_survey);
  alert(survey);
  //Debug:
  //debug();

  $.ajax({
            url: '/testingJSON',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });

});
*/


