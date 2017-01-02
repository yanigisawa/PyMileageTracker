var Helpers = {};
Helpers.initialized = false;
Helpers.initializePage = function () {
    if (Helpers.initialized) { return; }

    LatLong.getLatLong(function () {
        $("#latitude").val(LatLong.latitude);
        $("#longitude").val(LatLong.longitude);
    });
    var frm = $("#mainForm");
    if (frm) {
        frm.validate({
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
    }

    // wire up click and enter key press events for form submission
    $("#submitButton").click(Helpers.submitMileage);
    $("#gallons").keypress(function (e) {
        if (e.which == 13) {
            submitMileage();
        }
        Helpers.setFixedDecimal("#gallons", 3, e.which);
        e.preventDefault();
    });

    $("#miles").keypress(function (e) {
        Helpers.setFixedDecimal("#miles", 1, e.which)
        e.preventDefault();
    });

    $("#price").keypress(function (e) {
        Helpers.setFixedDecimal("#price", 3, e.which)
        e.preventDefault();
    });

    var url = document.URL
    url = url.replace(window.location.origin, "")

    if (url.length <= 1) {
        $("#recentHistory").load("/recentHistory", function () {
            $("#recentHistory").show(400);
        });
    }

    Helpers.initialized = true;
}

Helpers.submitMileage = function () {
    if (!$("#mainForm").valid()) {
        return;
    }

    $("#loading").show(100);
    $("#recentHistory").hide(400, function () {
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
            success: function (result) {
                $("#form").hide(400);
                $("#results").show(400);
                $("#recentHistory").load("/recentHistory", function () {
                    $("#recentHistory").show(400)
                });
            },
            error: function () {
                alert("Failed to submit mileage.");
            },
            complete: function () { $("#loading").hide(100); }
        });
    });
}

Helpers.setFixedDecimal = function (inputId, places, pressedKey) {
    var input = $(inputId);

    if (!input.val().trim()) { input.val("0.0"); }
    var divisor = Math.pow(10, places);
    var inputInt = String.fromCharCode(pressedKey);
    var newVal = parseFloat(input.val()) * 10 + parseInt(inputInt) / divisor;
    input.val(parseFloat(newVal).toFixed(places));
}
