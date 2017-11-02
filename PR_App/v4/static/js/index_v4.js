/*===============================================================
$(this).hide() - hides the current element.
$("p").hide() - hides all <p> elements.
===============================================================*/
$(document).ready(function(){
//Once the page is fully loaded, do the below

    //Spot switcher and update filter options function:
    $('.rb-box').on('click', ".rb-tab", function(){
        //Update the class of the currently and previously clicked filter button
        $(this).parent().find(".rb-tab").removeClass("rb-tab-active");
        $(this).addClass("rb-tab-active");

        var json_str_fltrs = get_selected_filters();  //Get the filter kinds and selected categories as json object/dict

        $.ajax({
            type: 'POST',
            contentType: 'application/json',
            data: json_str_fltrs,  //Send filter selection to Python/Flask REST service
            url: '/show_results',
            success: function(theData) {  //Use the data returned by the REST service
                console.log("success!! " + theData);
                //shows the currently applied filter kinds and cateogries, and the number of resulting project IDs
                update_results_section(theData);
                //makes all currently available filter buttons with the number of resulting project IDs if applied
                make_filter_buttons(theData);
            },
            error: function(error) {
                console.log("failure!! " + error)
            }
        });

    });


    //Shows the initial filter options after the begin button was clicked
    $('#begin_button').click(function() { $.post("/show_init_filters", init_filters) })


    function init_filters(fltrs){
    //Input: Dictionary of all possible filters and the numbers of their resulting project IDs if applied
    //Output: Creates in the webpage filter kind boxes and categories as per the information contained in the dictionary
        var filter_options_dict = eval(fltrs.filter_options_dict);
        var index = 1;
        //remove the begin screen text and start building the filter screen
        $(".rb-box").empty().append("<h2>Narrow down your results</h2>");

        for (var kind in filter_options_dict) {
            //for every kind of filter, make a box/bundle for it's categories
            $(".rb-box").append("<h3>" + index + ". " + kind + "</h3><div id='" + kind + "' class='rb'></div>");
            index += 1;
            //make an "All" button inside each filter kind box
            $("#" + kind).append("<div id='" + kind + "-ALL' class='rb-tab rb-tab-active' data-value='ALL'>" +
                "<div class='rb-spot'> <span class='rb-txt'>All</span> </div> </div>");

            $(filter_options_dict[kind]).each(function(i, e){  //for each category within this filter kind,
                //make a button for that category and it's resulting project IDs if applied
                $("#" + kind).append("<div id='" + kind + "-" + e[0] + "' class='rb-tab' data-value='" + e[0] +
                "'> <div class='rb-spot'> <span class='rb-txt'>" + e[0] + " (" + e[1] + ")</span> </div> </div>");
            })
        }
    }


    function update_results_section(theData){
        //var active_fltrs = eval(theData.active_fltrs);
        $("#results").show();  //"un-hide" the results section
        //display the number of project IDs resulting from the current filter selection
        $("#res-box h3").empty().append(theData.res_pids_count + " participants are:");
        $("#res-fltrs").empty();
        $(theData.active_fltrs).each(function(index, element){  //for each active filter
            $("#res-fltrs").append("<div class='res-tab'> <div class='res-spot'> <span class='res-txt'>" +
                element + "</span> </div> </div>");  //display it's kind and category in the results section
        })
    }


    function make_filter_buttons(theData){
        //extract the dictionary of all filter options and resulting project IDs
        var filter_options_dict = eval(theData.filter_options_dict);

        //make 'All' button option for every filter kind
        $(theData.all_fltr_kinds).each(function(index, element){
                        $("#" + element).empty().append("<div id='" + element +
                        "-ALL' class='rb-tab rb-tab-active' data-value='ALL'>" +
                        "<div class='rb-spot'><span class='rb-txt'>All</span></div></div>");
                    })

        //make 'Keep selection' button option for every active filter kind, and make this button the active one
        $(theData.active_fltr_kinds).each(function(index, element){
                        $("#" + element).append("<div id='" + element + "-ASIS' class='rb-tab rb-tab-active' data-value='ASIS'>" +
                        "<div class='rb-spot'><span class='rb-txt'>Keep selection</span></div></div>");
                        $("#" + element + "-ALL").removeClass('rb-tab-active');
                    })

        //make button options for all addable filters with resulting project IDs if applied
        for (var kind in filter_options_dict) {
            $(filter_options_dict[kind]).each(function(i, e){
                $("#" + kind).append("<div id='" + kind + "-" + e[0] + "' class='rb-tab' data-value='" + e[0]
                    + "'><div class='rb-spot'><span class='rb-txt'>" + e[0] + " (" + e[1] + ")</span></div></div>");
            })
        }
    }


    function get_selected_filters(){
    //Returns a dictionary of filter kinds to selected filter categories.
    var fltr_dict = {};
    for (i=0; i<$(".rb").length; i++) {  //loop through each filter kind button bundle
            var kind = $(".rb")[i].id;  //get this bundle's filter kind
            ////get the bundle's clicked button's category
            var cat = $("#"+kind).find(".rb-tab-active").attr("data-value");
            fltr_dict[kind] = cat;  //make dictionary of each filter kind to it's selected category
    }
    return JSON.stringify(fltr_dict);  //return that dictionary as a json object
    }
})
