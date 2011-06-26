function getLatLong() {
    if(geo_position_js.init()){
        geo_position_js.getCurrentPosition(success_callback,error_callback,{enableHighAccuracy:true,options:5000});
    }
    else{
        alert("Functionality not available");
    }

    function success_callback(p)
    {
        //alert('lat='+p.coords.latitude.toFixed(2)+';lon='+p.coords.longitude.toFixed(2));
        $("#lat").html("Lat: " + p.coords.latitude);
        $("#long").html("Long: " + p.coords.longitue);
    }

    function error_callback(p)
    {
        alert('error='+p.message);
    }
}
