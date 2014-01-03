var Helpers = {};
Helpers.initializePage = function() {
    LatLong.getLatLong(function() {
        $("input[name='latitude']").val(LatLong.latitude);
        $("input[name='longitude']").val(LatLong.longitude);
    });
    $("#mainForm").validate({
        rules: {
            miles: {
                required: true,
                number: true
            }, 
            pricePerGallon: {
                required: true,
                number: true
            }, 
            gallons: {
                required: true,
                number: true
            }
        }
    });

    // wire up click and entery key press events for form submission
    $("#submitButton").click(Helpers.submitMileage);
    $("#gallons").keypress(function(e) {
        if (e.which== 13) {
            submitMileage();
        }
    });

    $("#recentHistory").load("/recentHistory", function() {
        $("#recentHistory").show(400);
    });
}

Helpers.submitMileage = function() {
    if (!$("#mainForm").valid()) {
        return;
    }

    $("#loading").show();
    $.ajax({
        type: "POST",
        url: "/submitMileage",
        dataType: "json",
        data: {
            miles: $("#miles").val(),
            price: $("#pricePerGallon").val(),
            gallons: $("#gallons").val(), 
            latitude: $("#latitude").val(),
            longitude: $("#longitude").val()
        }, 
        success: function() {
            $("#form").hide(400); 
            $("#results").show(400);
            $("#recentHistory").load("/recentHistory");
        },
        error: function() {
            alert("Failed to submit mileage.");
        },
        complete: function() { $("#loading").hide(); }
    });
}
