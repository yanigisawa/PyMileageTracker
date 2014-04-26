var Helpers = {};
Helpers.initializePage = function() {
    LatLong.getLatLong(function() {
        $("#latitude").val(LatLong.latitude);
        $("#longitude").val(LatLong.longitude);
    });
    $("#mainForm").validate({
        rules: {
            miles: {
                required: true,
                number: true
            }, 
            price: {
                required: true,
                number: true
            }, 
            gallons: {
                required: true,
                number: true
            }
        }
    });

    // wire up click and enter key press events for form submission
    $("#submitButton").click(Helpers.submitMileage);
    $("#gallons").keypress(function(e) {
        if (e.which== 13) {
            submitMileage();
        }
    });

   var url = document.URL
   url = url.replace(window.location.origin, "")

   if (url.length <= 1) {
        $("#recentHistory").load("/recentHistory", function() {
            $("#recentHistory").show(400);
        });
    }
}

Helpers.submitMileage = function() {
    if (!$("#mainForm").valid()) {
        return;
    }

    $("#loading").show(100);
    $("#recentHistory").hide(400, function() {
        $.ajax({
            type: "POST",
            url: "/submitMileage",
            dataType: "json",
            data: {
                miles: $("#miles").val(),
                price: $("#price").val(),
                gallons: $("#gallons").val(), 
                latitude: $("#latitude").val(),
                longitude: $("#longitude").val()
            }, 
            success: function(result) {
                $("#form").hide(400); 
                $("#results").show(400);
                $("#recentHistory").load("/recentHistory", function() {
                    $("#recentHistory").show(400)
                });
            },
            error: function() {
                alert("Failed to submit mileage.");
            },
            complete: function() { $("#loading").hide(100); }
        });
    });
}

