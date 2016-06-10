$(document).ready(function(){

// Get JSON-formatted data from the server
$.getJSON( "/nodes", function( resp ) {

    // Log each key in the response data
    $.each( resp, function( key, value ) {
        console.log( key + " : " + value );

        for (node in resp.nodes) {
            $("#node_table").append(
                "<tr id=\"tr-"+resp.nodes[node]+ "\">" +
                "<td class=\"active navbar-button status-tbd\">&hellip;</td><td class=\"active\">"
                + resp.nodes[node] + "</td></tr>"
            );
        }

        for (node in resp.nodes) {
            $.getJSON( "/nodes/"+resp.nodes[node], function( zz ) {
                //$.each( zz, function( key, value ) {
                //    console.log( key + " : " + value );
                //});

                // replace the table row
                $("#tr-"+zz.node).replaceWith("<tr id=\"tr-"+zz.node+ "\">" +
                    "<td class=\"active navbar-button "+zz.state+"\">" + zz.label+"</td><td class=\"active\">"
                    + zz.node + "</td></tr>"
                );
            });
        }
    });
});
});

$(document).ready(function($) {
    $(".clickable-row").click(function() {
        window.document.location = $(this).data("href");
    });
});

