function sendajax(eventstring){



    var url = "myroute";
            var hr = new XMLHttpRequest();
            //var wholedate = "20191101";
            //console.log("Date " + wholedate);
    //console.log(encodedVars);
            hr.open('POST', url, true);

           hr.setRequestHeader("Content-type", "application/json");
            hr.onreadystatechange = function(){
                if (hr.readyState ==4 && hr.status==200){
                    var return_data = hr.responseText;
                    document.getElementById('postevent').innerhtml = "";
                    document.getElementById("postevent").innerHTML = return_data;
                    console.log(return_data);
                }
            }
            hr.send(eventstring);
            //console.log();
            //document.getElementById("postevent").innerHTML = "processing ....";
        }