$(document).ready(function(){

// Make index table rows clickable
$(".clickable-row").click(function() {
    window.document.location = $(this).data("href");
});

// Update right-panel node list statuses
$.getJSON( "/nodes", function( resp ) {

    // Log each key in the response data
    $.each( resp, function( key, value ) {
        console.log( key + " : " + value );

        // add a [...] button for each node
        for (node in resp.nodes) {
            $("#node_table").append(
                "<tr id=\"tr-"+resp.nodes[node]+ "\">" +
                "<td class=\"active navbar-button status-tbd\">&hellip;</td><td class=\"active\">"
                + resp.nodes[node] + "</td></tr>"
            );
        }

        // fetch each node status and replace result
        for (node in resp.nodes) {
            $.getJSON( "/nodes/"+resp.nodes[node], function( zz ) {
                $("#tr-"+zz.node).replaceWith("<tr id=\"tr-"+zz.node+ "\">" +
                    "<td class=\"active navbar-button "+zz.state+"\">" + zz.label+"</td><td class=\"active\">"
                    + zz.node + "</td></tr>"
                );
            });
        }
    });
});
});
