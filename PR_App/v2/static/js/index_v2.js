/*===============================================================
$(this).hide() - hides the current element.

$("p").hide() - hides all <p> elements.

$(".test").hide() - hides all elements with class="test".

$("#test").hide() - hides the element with id="test".
===============================================================*/
//Global:
var fltr_dict = {};

$(document).ready(function(){

    //Switcher function:
    $('.rb-box').on('click', ".rb-tab", function(){
        //alert("hello");
        //Spot switcher:
        $(this).parent().find(".rb-tab").removeClass("rb-tab-active");
        $(this).addClass("rb-tab-active");
    });


    $('#filter_button').click(function() {
        fltr_dict = {};
        for (i=0; i<$(".rb").length; i++) {
            var kind = $(".rb")[i].id;  //get div id as kind
            //get the clicked button's data-value as category
            var cat = $("#"+kind).find(".rb-tab-active").attr("data-value");
            fltr_dict[kind] = cat;
        };
        var json_str_fltrs = JSON.stringify(fltr_dict);  // send this to python REST

        $.ajax({
            type: 'POST',
            contentType: 'application/json',
            data: json_str_fltrs,
            url: '/show_results',
            success: function(theData) {
                console.log("success!! " + theData);
                //alert(theData.filters);
                //alert(theData.results);
                $('#results').empty().append("<div id='res-box' class='res-box'>");
                $('#res-box').append("<h2>Results</h2> <h3>" + theData.results + " participants are:</h3>" +
                    "<div id='res-fltrs' class='rb'>");
                $(theData.filters).each(function(index, element){
                    $("#res-fltrs").append("<div class='res-tab'> <div class='res-spot'> <span class='res-txt'>" +
                        element + "</span> </div> </div>");
                });
                $('#res-box').append("</div>");
                $('#results').append("</div>");

                //$(".rb").find(".rb-tab").removeClass("rb-tab-active");
                //$('.rb-tab[data-value="ALL"]').addClass("rb-tab-active");

                $("#Gender").empty().append("<div id='Gender-ALL' class='rb-tab rb-tab-active' data-value='ALL'>" +
                "<div class='rb-spot'><span class='rb-txt'>All</span></div></div>");

                $("#Age").empty().append("<div id='Age-ALL' class='rb-tab rb-tab-active' data-value='ALL'>" +
                "<div class='rb-spot'><span class='rb-txt'>All</span></div></div>");

                $("#MinDrugUse").empty().append("<div id='MinDrugUse-ALL' class='rb-tab rb-tab-active' data-value='ALL'>" +
                "<div class='rb-spot'><span class='rb-txt'>Any</span></div></div>");

                $("#MaxDrugUse").empty().append("<div id='MaxDrugUse-ALL' class='rb-tab rb-tab-active' data-value='ALL'>" +
                "<div class='rb-spot'><span class='rb-txt'>Any</span></div></div>");

                $(theData.fltr_kinds).each(function(index, element){
                $("#" + element).prepend("<div id='" + element + "-ASIS' class='rb-tab' data-value='ASIS'>" +
                "<div class='rb-spot'><span class='rb-txt'>Keep selection</span></div></div>");
                });

                for (i=0; i<$(theData.testing).length; i+=3) {
                    var kind = theData.testing[i];
                    var cat = theData.testing[i+1];
                    var new_id = kind + "-" + cat;
                    var new_txt = '';
                    if (cat == 'M'){
                        new_txt = "Male";
                    }else if (cat == 'F'){
                        new_txt = "Female";
                    }else if (cat == 'TG'){
                        new_txt = "Transgender";
                    }else {
                        new_txt = cat;
                    }
                    $("#" + kind).prepend("<div id='" + new_id + "' class='rb-tab' data-value='" + cat
                    + "'><div class='rb-spot'><span class='rb-txt'>" + new_txt + " (" + theData.testing[i+2] + ")</span></div></div>");

                    //$("#" + kind).prepend("<div id='" + new_id + "' class='rb-tab' data-value='" + cat
                    //+ "'><div class='rb-spot'></div><span class='rb-txt'>" + new_txt + " (" + theData.testing[i+2] + ")</span></div>");

                };
            },

            error: function(error) {
                console.log("failure!! " + error);
            }
        });

    });

});
