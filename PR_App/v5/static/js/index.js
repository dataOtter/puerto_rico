/*===============================================================
$(this).hide() - hides the current element.
$("p").hide() - hides all <p> elements.
===============================================================*/
$(document).ready(function(){
//Once the page is fully loaded, do the below

    $.post("/show_init_filters", init_filters);

    //Spot switcher and update filter options function:
    $('.filters').on('click', ".rbutton", function(){
        //Update the class of the currently and previously clicked filter button
        $(this).parent().find(".rbutton").removeClass("rbutton-active");
        $(this).addClass("rbutton-active");

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
                update_buttons(theData);
            },
            error: function(error) {
                console.log("failure!! " + error)
            }
        });
    });


    $('.download').on('click', "#generate_download_button", function() {
        $.post("/generate_download_zip", make_download_link )
    })


    function make_download_link(zip_folder) { $('#download_link').attr('href', 'outputs/' + zip_folder.zip_folder_name); }


    function init_filters(fltrs){
    //Input: Dictionary of all possible filters and the numbers of their resulting project IDs if applied
    //Output: Creates in the webpage filter kind boxes and categories as per the information contained in the dictionary
        var filter_options_dict = eval(fltrs.filter_options_dict);
        window.all_participants = fltrs.total_participants;
        $("#results h3").empty().append(all_participants + "/" + all_participants);

        for (var kind in filter_options_dict) {
            //for every kind of filter, make a box/bundle for it's categories
            $(".filters").append("<div id='" + kind + "' class='rbutton-row'></div>");
            //make filter kind row label
            $("#" + kind).append("<div id='" + kind + "-label' class='rbutton'>" +
                "<div class='rblabel-spot'> <span class='rblabel-txt'>" + kind + "</span> </div> </div>");

            //make an "All" button inside each filter kind box
            $("#" + kind).append("<div id='" + kind + "-ALL' class='rbutton rbutton-active' data-value='ALL'>" +
            "<div class='rb-spot'> <span class='rb-txt'>ALL</span> </div> </div>");

            //for each category within this filter kind,
            $(filter_options_dict[kind]).each(function(i, e){
                //make a button for that category and it's resulting project IDs if applied
                $("#" + kind).append("<div id='" + kind + "-" + e[0] + "' class='rbutton' data-value='" + e[0] +
                "'> <div class='rb-spot'> <span class='rb-txt'>" + e[0] + " (" + e[1] + ")</span> </div> </div>");
            })

        }
    }


    function update_results_section(theData){
        //var active_fltrs = eval(theData.active_fltrs);
        //display the number of project IDs resulting from the current filter selection
        $("#results h3").empty().append(theData.res_pids_count + "/" + window.all_participants);
    }


    function update_buttons(theData){
        //extract the dictionary of all filter options and resulting project IDs
        var filter_options_dict = eval(theData.filter_options_dict);
        var active_fltrs = theData.active_fltrs;
        var to_append = "";

        $('.filters').removeClass('rbutton-active');
        $('.rbutton').removeClass('rbutton-inactive').prop("disabled", false);

        //make selected filter(s) active buttons
        for (var kind in active_fltrs) {
            cat = active_fltrs[kind];
            $("#" + kind + "-" + cat).addClass('rbutton-active').prop("disabled", true);
            $('#' + kind + "-" + cat + " .rb-txt").empty().append(cat);
        }
        //make button options for all addable filters with resulting project IDs if applied
        for (var kind in filter_options_dict) {
            $(filter_options_dict[kind]).each(function(i, e){
                if (e[1] == 0) {
                    $('#' + kind + "-" + e[0]).addClass('rbutton-inactive').prop("disabled", true);
                    to_append = e[0] + " (0)";
                } else {
                to_append = e[0] + " (" + e[1] + ")";
                }
                $('#' + kind + "-" + e[0] + " .rb-txt").empty().append(to_append);
            })
        }
    }


    function get_selected_filters(){
    //Returns a dictionary of filter kinds to selected filter categories.
    var fltr_dict = {};
    for (i=0; i<$(".rbutton-row").length; i++) {  //loop through each filter kind button bundle
            var kind = $(".rbutton-row")[i].id;  //get this bundle's filter kind
            ////get the bundle's clicked button's category
            var cat = $("#"+kind).find(".rbutton-active").attr("data-value");
            fltr_dict[kind] = cat;  //make dictionary of each filter kind to it's selected category
    }
    return JSON.stringify(fltr_dict);  //return that dictionary as a json object
    }
})
