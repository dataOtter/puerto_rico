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

$(document).ready(function(){

    //Switcher function:
    $(".rb-tab").click(function(){
        //Spot switcher:
        $(this).parent().find(".rb-tab").removeClass("rb-tab-active");
        $(this).addClass("rb-tab-active");
    });


    $('#filter_button').click(function() {
        survey = {};
        for (i=1; i<=$(".rb").length; i++) {
            var kind = $(".rb")[i-1].id;
            var rbValue = $("#"+kind).find(".rb-tab-active").attr("data-value");
            survey[kind] = rbValue;
        };
        var json_str_survey = JSON.stringify(survey);  // send this to python

        $.ajax({
            type: 'POST',
            contentType: 'application/json',
            data: json_str_fltrs,
            url: '/show_results',
            success: function(theData) {
                console.log("success!! " + theData);
                //alert(theData.filters);
                //alert(theData.results);
                $('#res-fltrs').empty();
                $("#res-header").empty().append(theData.results + " participants are:");
                $(theData.filters).each(function(index, element){
                    $("#res-fltrs").append("<div class='res-tab'> <div class='res-text-box'> <span class='res-txt'>" +
                    element + "</span> </div> </div>");
                });

                $(".rb").find(".rb-tab").removeClass("rb-tab-active");
                $('.rb-tab[data-value="ALL"]').addClass("rb-tab-active");
            },

            error: function(error) {
                console.log("failure!! " + error);
            }
        });

    });

});