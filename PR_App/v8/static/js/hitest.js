$(document).ready(function(){

    $('.download').on('click', "#send_to_extractor", function() {
        $.ajax({
            type: 'GET',
            url: '/echo',
            dataType: 'html',
            success:
                function(theData) {
                    console.log("success!! " + theData);
                    document.write(theData);
                }
            ,
            error: function(error) {
                console.log("failure!! " + error)
            }
        });
        //window.location.href='../templates/testhi2.html';
    });


})
