var LatLong = {}

LatLong.getLatLong = function (callback) {
    function success_callback(p)
    {
        //alert('lat='+p.coords.latitude.toFixed(2)+';lon='+p.coords.longitude.toFixed(2));
        LatLong.latitude = p.coords.latitude;
        LatLong.longitude = p.coords.longitude;
        if (callback !== null) { callback(); }
    }

    function error_callback(p)
    {
        alert('error fetching Lat/Long='+p.message);
    }

    if(geo_position_js.init()){
        geo_position_js.getCurrentPosition(success_callback,error_callback,{enableHighAccuracy:true,options:5000});
    }
    else{
        alert("Functionality not available");
    }

}
