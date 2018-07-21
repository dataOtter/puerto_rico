$(document).ready(function(){

    $(document).ajaxStart(function(){
        $.LoadingOverlay("show");
    });
    $(document).ajaxStop(function(){
        $.LoadingOverlay("hide");
    });

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

    //On button click send to extractor page
    $('.download').on('click', "#send_to_extractor", function() {
        $.ajax({
            type: 'GET',
            url: '/send_to_extractor',
            dataType: 'html',
            success: function(template) {
                    $("body").empty().append(template);
                    //$("body").empty().load("../../templates/extractor.html");
                    console.log("success!! ");

                    $.post("/send_available_cols", init_cols_selector);
                    $('.flex-container').on('click', "#generate_download_button", make_zip_download);

                    $('.flex-container').on('click', ".cols-button", add_rem_all_cols);

                    $('.flex-container').on('click', ".list-group-item", add_rem_one_col);
                },
            error: function(error) {
                console.log("failure!! " + error)
            }
        });
    });
    /////////////////////////////////////////////////////////////////////////////
    // extractor jquery
    /////////////////////////////////////////////////////////////////////////////
    //$.post("/send_available_cols", init_cols_selector);

    //$('.flex-container').on('click', "#generate_download_button", make_zip_download);

    //$('.flex-container').on('click', ".cols-button", add_rem_all_cols);

    //$('.flex-container').on('click', ".list-group-item", add_rem_one_col);


    /////////////////////////////////////////////////////////////////////////////
    // faceted search functions
    /////////////////////////////////////////////////////////////////////////////
    function init_filters(fltrs){
    //Input: Dictionary of all possible filters and the numbers of their resulting project IDs if applied
    //Output: Creates in the webpage filter kind boxes and categories as per the information contained in the dictionary
        var filter_options_dict = eval(fltrs.filter_options_dict);
        window.all_participants = fltrs.total_participants;
        window.prev_participants = fltrs.total_participants;

        circle(window.all_participants, window.all_participants, window.prev_participants);

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
        //display the number of project IDs resulting from the current filter selection
        circle(window.all_participants, theData.res_pids_count, window.prev_participants);
        window.prev_participants = theData.res_pids_count;
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
            $(active_fltrs[kind]).each(function(i, cat){
                $("#" + kind + "-" + cat).addClass('rbutton-active').prop("disabled", true);
                $('#' + kind + "-" + cat + " .rb-txt").empty().append(cat);
            });
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


    function circle(total, selected, prev_selected) {

        var inner_radius = 200, outer_radius = 215;

        var startPercent = prev_selected/total, endPercent = selected/total;

        var twoPi = Math.PI * 2;
        var count = Math.abs((endPercent - startPercent) / 0.01);
        var step = endPercent < startPercent ? -0.01 : 0.01;

        var arc = d3.svg.arc()
            .startAngle(0)
            .innerRadius(inner_radius)
            .outerRadius(outer_radius);

        d3.select('#meter').attr('d', arc.endAngle(twoPi));

        function updateProgress(progress) {
            d3.select('#foreground').attr('d', arc.endAngle(twoPi * progress));
            d3.select('#front').attr('d', arc.endAngle(twoPi * progress));
            d3.select('#text').text(selected + "/" + total);
        }

        var progress = startPercent;

        (function loops() {
            updateProgress(progress);

            if (count > 0) {
                count--;
                progress += step;
                setTimeout(loops, 10);
            }
        })();
    }

    /////////////////////////////////////////////////////////////////////////////
    // extractor functions
    /////////////////////////////////////////////////////////////////////////////
    function make_zip_download() {
        $.ajax({
            type: 'POST',
            contentType: 'application/json',
            data: get_selected_cols(),  // send selected columns as dict of phases to dict of tables to array of columns
            url: '/receive_selected_cols',
            success: function(zip_folder) {  //use the data returned by the REST service
                console.log("success!! " + zip_folder);
                make_download_link(zip_folder);
            },
            error: function(error) {
                console.log("failure!! " + error)
            }
        });

    }


    function make_download_link(zip_folder) {
        $('#download_link').attr('href', 'outputs/' + zip_folder.zip_folder_name).show();
        $('#generate_download_button').attr("disabled", true);
    }


    function get_selected_cols() {
    // Returns dictionary of phases to dictionary of tables to array of columns, as Json object
        var phase_tbl_cols_dict = {};

        $(".cols-flex").each( function() {  // for each .cols-flex,

            var temp_phase_name = $(this).prev('h2').text();  // get the preceding h2 as the current phase
            //alert(temp_phase_name);
            var temp_tbl_dict = {};
            // walk down to the .cols-scroll section whose id contains selected - here it is hard coded to be the second
            var selected_section_id = $(this).find('.cols-scroll').eq(1).attr('id');

            if ( selected_section_id.includes('selected') ) {  // just to double check that this is the selected section
                $("#" + selected_section_id + ' .panel-group').each( function() {  // for each .panel-group,

                    var temp_table_name = $(this).find("a").text();  // get the text of 'a' as the table name
                    //alert(temp_table_name);
                    var temp_collapse_id = $(this).find("a").attr('href').slice(1);
                    var temp_col_labels = [];

                    $("#" + temp_collapse_id + ' li').each( function() {  // for each li,
                        temp_col_labels.push($(this).text());  // get its text as the column label and put in array
                    })
                    //alert(temp_col_labels);
                    temp_tbl_dict[temp_table_name] = temp_col_labels;  // key: table name, value: array of its columns
                })
            }
            phase_tbl_cols_dict[temp_phase_name] = temp_tbl_dict;  // key: phase name, value: table dict
        })
        /*for ( var phase in phase_tbl_cols_dict) {
            for ( var tbl in phase_tbl_cols_dict[phase]) {
                for ( var i = 0; i < phase_tbl_cols_dict[phase][tbl].length; i++ ) {
                    alert(phase + ': ' + tbl + ': ' + phase_tbl_cols_dict[phase][tbl][i]);
                }
            }
        }*/
        return JSON.stringify(phase_tbl_cols_dict);  // return as Json object
    }


    function init_cols_selector(cols){
        var phase_dict = eval(cols.result);
        var counter = 10;

        for (var phase in phase_dict) {
            make_phase_html(phase);
            for (var tbl in phase_dict[phase]){
                counter += 1;
                make_tbl_in_phase_html(tbl, counter, phase + "_avail_cols_scroll");
                $(phase_dict[phase][tbl]).each(function(i, col){
                    make_col_in_tbl_html(counter, col);
                })
            }
        }
    }


    function add_rem_one_col() {
    // $(this) is assumed to be the column li element that was clicked on
        var cols_scroll_id = $(this).closest('.cols-scroll').attr('id');

        if ( cols_scroll_id.includes('avail') ) {  // to make sure the correct counter number is used
            var counter_orig = $(this).closest('div').attr('id').substr(-2);
            var counter_dest = counter_orig + 's';
            move_one_col($(this), 'avail', 'selected', counter_dest, counter_orig, cols_scroll_id);
        }
        else if ( cols_scroll_id.includes('selected') ) {
            var counter_orig = $(this).closest('div').attr('id').substr(-3);
            var counter_dest = counter_orig.slice(0,2);
            move_one_col($(this), 'selected', 'avail', counter_dest, counter_orig, cols_scroll_id);
        }
        enable_disable_generate_download_button();
    }


    function add_rem_all_cols() {
        // $(this) is assumed to be the add/rem all button that was clicked on
        var cols_scroll_id = $(this).closest('.cols-box').find('.cols-scroll').attr('id');

        if ( cols_scroll_id.includes('avail') ) {
            move_all_cols(cols_scroll_id, 'avail', 'selected');
        }
        else if ( cols_scroll_id.includes('selected') ) {
            move_all_cols(cols_scroll_id, 'selected', 'avail');
        }
        enable_disable_generate_download_button();
    }


    function move_one_col(this_col_li_element, move_from, move_to, counter_dest, counter_orig, cols_scroll_id) {
        var col_label = this_col_li_element.text();
        var tbl_name = this_col_li_element.closest('.panel').find('a').text();
        var move_to_cols_scroll_id = cols_scroll_id.replace(move_from, move_to);

        // if the table does not already exist, make the table
        if ($('#' + move_to_cols_scroll_id + ':contains("' + tbl_name + '")').length <= 0) {
            //alert('making ' + tbl_name);
            make_tbl_in_phase_html(tbl_name, counter_dest, move_to_cols_scroll_id);
        }
        // either way, add and remove the column
        make_col_in_tbl_html(counter_dest, col_label);
        remove_col_from_tbl_html(counter_orig, col_label);

        // if the origin table is now empty, remove it
        if ( $('#collapse' + counter_orig + ' ul').children().length <= 0 ) {
            remove_tbl_from_phase_html(cols_scroll_id, tbl_name);
        }
    }

    function move_all_cols(cols_scroll_id, move_from, move_to){
        while ( $('#' + cols_scroll_id).children().length > 0 ) {  // while there are columns left,
            // get the next column element
            var this_col_object = $('#' + cols_scroll_id).find('li').first();
            //alert(this_col_object.text());
            if ( move_from == 'avail' ) {  // to make sure the correct counter number is used
                var counter_orig = this_col_object.closest('div').attr('id').substr(-2);
                var counter_dest = counter_orig + 's';
                move_one_col(this_col_object, 'avail', 'selected', counter_dest, counter_orig, cols_scroll_id);
            }
            else if ( move_from == 'selected' ) {
                var counter_orig = this_col_object.closest('div').attr('id').substr(-3);
                var counter_dest = counter_orig.slice(0,2);
                move_one_col(this_col_object, 'selected', 'avail', counter_dest, counter_orig, cols_scroll_id);
            }
        }
    }

    function make_phase_html(phase){
        var to_append = "<h2>" + phase + "</h2>" +
        "<div id='" + phase + "_flex' class='cols-flex'>" +
        "<div id='" + phase + "_avail_cols' class='cols-box'>" +
        "<div class='cols-header'><h3>Available Table Columns</h3><div id='add-button' class='cols-button'>Add All</div></div>" +
        "<div id='" + phase + "_avail_cols_scroll' class='cols-scroll'></div></div>" +
        "<div id='" + phase + "_selected_cols' class='cols-box'>" +
        "<div class='cols-header'><h3>Selected Table Columns</h3><div id='rem-button' class='cols-button'>Remove All</div></div>" +
        "<div id='" + phase + "_selected_cols_scroll' class='cols-scroll'></div></div></div>";

        $("#phase_flex").append(to_append);
    }

    function make_tbl_in_phase_html(tbl, counter, cols_scroll_id){
        var to_append = "<div class='panel-group'><div class='panel panel-default'><div class='panel-heading'>" +
        "<h4 class='panel-title'><a data-toggle='collapse' href='#collapse" + counter + "'>" + tbl + "</a></h4></div>" +
        "<div id='collapse" + counter + "' class='panel-collapse collapse'><ul class='list-group'></ul></div></div></div>";

        $("#" + cols_scroll_id).append(to_append);
    }

    function make_col_in_tbl_html(counter, col){
        var to_append = "<li class='list-group-item tbl-col-label'>" + col + "</li>";

        $("#collapse" + counter + " .list-group").append(to_append);
    }

    function remove_col_from_tbl_html(counter, col) {
        $('#collapse' + counter + ' li:contains("' + col + '")').filter(function() {
            return $(this).text() == col;  // to make sure only exact matches are removed
        }).remove();
    }

    function remove_tbl_from_phase_html(cols_scroll_id, tbl_name) {
        $('#' + cols_scroll_id + ' .panel-group:contains("' + tbl_name + '")').filter(function() {
            return $(this).text() == tbl_name;  // to make sure only exact matches are removed
        }).remove();
    }

    function enable_disable_generate_download_button() {
        $(".cols-scroll").each( function() {
            if ( $(this).attr('id').includes('selected') && $(this).children().length > 0 ) {
                $('#generate_download_button').attr("disabled", false);
                return false;  // must return false in order to break out of each - return true == continue
            } else {
                $('#generate_download_button').attr("disabled", true);
                $('#download_link').hide();
            }
        })
    }

})
