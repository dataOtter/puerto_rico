/*===============================================================
$(this).hide() - hides the current element.
$("p").hide() - hides all <p> elements.
$(".test").hide() - hides all elements with class="test".
$("#test").hide() - hides the element with id="test".
===============================================================*/
//Global:
var fltr_dict = {};

$(document).ready(function(){

    //Spot switcher function:
    $('.rb-box').on('click', ".rb-tab", function(){
        $(this).parent().find(".rb-tab").removeClass("rb-tab-active");
        $(this).addClass("rb-tab-active");
    })

    $('#begin_button').click(function() { $.post("/show_init_filters", init_filters) })

    $(".rb-box").on('click', '#filter_button', function() {
        var json_str_fltrs = get_selected_filters();

        $.ajax({
            type: 'POST',
            contentType: 'application/json',
            data: json_str_fltrs,
            url: '/show_results',
            success: function(theData) {
                console.log("success!! " + theData);

                update_results_section(theData);

                make_filter_buttons(theData);
            },
            error: function(error) {
                console.log("failure!! " + error)
            }
        });

    })

    function init_filters(fltrs){
        var filter_options_dict = eval(fltrs.filter_options_dict);
        var index = 1;

        $(".rb-box").empty().append("<h2>Narrow down your results</h2>");

        for (var kind in filter_options_dict) {
            $(".rb-box").append("<h3>" + index + ". " + kind + "</h3><div id='" + kind + "' class='rb'></div>");
            index += 1;

            $("#" + kind).append("<div id='" + kind + "-ALL' class='rb-tab rb-tab-active' data-value='ALL'>" +
                "<div class='rb-spot'> <span class='rb-txt'>All</span> </div> </div>");

            $(filter_options_dict[kind]).each(function(i, e){
                $("#" + kind).append("<div id='" + kind + "-" + e[0] + "' class='rb-tab' data-value='" + e[0] +
                "'> <div class='rb-spot'> <span class='rb-txt'>" + e[0] + " (" + e[1] + ")</span> </div> </div>");
            })
        }

        $(".rb-box").append("<div class='button-box'> <button id='filter_button' class='button trigger'>Submit</button> </div>");
    }

    function update_results_section(theData){
        //var active_fltrs = eval(theData.active_fltrs);
        $("#results").show();
        $("#res-box h3").empty().append(theData.res_pids_count + " participants are:");
        $("#res-fltrs").empty();
        $(theData.active_fltrs).each(function(index, element){
            $("#res-fltrs").append("<div class='res-tab'> <div class='res-spot'> <span class='res-txt'>" +
                element + "</span> </div> </div>")
        })
    }

    function make_filter_buttons(theData){
        var filter_options_dict = eval(theData.filter_options_dict);

        //make 'All' button option for every filter kind
        $(theData.all_fltr_kinds).each(function(index, element){
                        $("#" + element).empty().append("<div id='" + element +
                        "-ALL' class='rb-tab rb-tab-active' data-value='ALL'>" +
                        "<div class='rb-spot'><span class='rb-txt'>All</span></div></div>");
                    })

        //make 'Keep selection' button option for every active filter kind
        $(theData.active_fltr_kinds).each(function(index, element){
                        $("#" + element).append("<div id='" + element + "-ASIS' class='rb-tab' data-value='ASIS'>" +
                        "<div class='rb-spot'><span class='rb-txt'>Keep selection</span></div></div>");
                    })

        //make button options for all addable filters with result project IDs if applied
        for (var kind in filter_options_dict) {
            $(filter_options_dict[kind]).each(function(i, e){
                $("#" + kind).append("<div id='" + kind + "-" + e[0] + "' class='rb-tab' data-value='" + e[0]
                    + "'><div class='rb-spot'><span class='rb-txt'>" + e[0] + " (" + e[1] + ")</span></div></div>");
            })
        }
    }

    function get_selected_filters(){
    fltr_dict = {};
    for (i=0; i<$(".rb").length; i++) {
            var kind = $(".rb")[i].id;  //get div id as kind
            //get the clicked button's data-value as category
            var cat = $("#"+kind).find(".rb-tab-active").attr("data-value");
            fltr_dict[kind] = cat;
    }
    var json_str_fltrs = JSON.stringify(fltr_dict);  // send this to python REST
    return json_str_fltrs;
    }
})
