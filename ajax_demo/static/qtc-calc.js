function calculateQTc() {
    var prolonged;
    var heartRate = parseInt(document.getElementById("hr").value);
    var qtInt     = parseInt(document.getElementById("qt").value);
    var sex                = document.getElementsByName("sex");
    var qtcResult          = document.getElementById("qtc");
    var prolongedResult    = document.getElementById("prolonged");
    var resultsContainer   = document.getElementById("qtc-results");
    var numRows            = document.getElementById("num-rows");

    resultsContainer.style.display = "block";

    for(var i=0; i<sex.length; i++) {
	if(sex[i].checked) var selectedSex = sex[i].value;
    }

    qtSeconds = qtInt / 1000;
    rrInterval = (6000 / heartRate);
    QTc = qtSeconds / Math.sqrt(rrInterval);
    formattedQTc = Math.round((QTc * 1000) * 10, 0);
    qtcResult.innerHTML = formattedQTc;

    if((formattedQTc > 440 && selectedSex == 'm') ||
       (formattedQTc > 460 && selectedSex == 'f')) {
	prolongedResult.innerHTML = "This is a prolonged QT interval!!! Do something!";
	prolonged = "Prolonged QT";
    }
    else {
	prolongedResult.innerHTML = "This is a normal QT interval: well done!";
	prolonged = "Normal QT";
    }

    var server_data = {
	{"QTc": formattedQTc},
	{"prolonged": prolonged},
	{"HR": heartRate},
	{"QT": qtInt},
	{"Sex": selectedSex}
    }

    $.ajax({
	type: "POST",
	url:  "/process_qtc",
	data: JSON.stringify(server_data),
	contentType: "application/json",
	dataType:    'json',
	success:     function(result) {
	    numRows.innerHTML = result.rows;
	}
    });
}
