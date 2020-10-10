function setDateAndTime() {
  var date = new Date();

  var day = date.getDate(),
      month = date.getMonth() + 1,
      year = date.getFullYear(),
      hour = date.getHours(),
      min  = date.getMinutes();
  
  month = (month < 10 ? "0" : "") + month;
  day = (day < 10 ? "0" : "") + day;
  hour = (hour < 10 ? "0" : "") + hour;
  min = (min < 10 ? "0" : "") + min;
  
  var today = year + "-" + month + "-" + day,
      displayTime = hour + ":" + min; 
  
  document.getElementById('date').value = today;      
  document.getElementById("time").value = displayTime;
}

function getParameterByName(name) {
  url = window.location.href;
  name = name.replace(/[\[\]]/g, '\\$&');
  var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
      results = regex.exec(url);
  if (!results) return null;
  if (!results[2]) return '';
  return decodeURIComponent(results[2].replace(/\+/g, ' '));
}

function checkQueryParams() {
  const id = getParameterByName('id');
  const name = getParameterByName('name');
  const location = getParameterByName('location');
  const activity = getParameterByName('activity');
  const severity = getParameterByName('severity');
  const occurence = getParameterByName('occurence');
  const date = getParameterByName('date');
  const time = getParameterByName('time');
  const notes = getParameterByName('notes');
  console.log(id, name, location, activity, severity, occurence, date, time, notes)
  const form = document.forms["record-symptom"];
  form["id"].value = id;
  // What about others?
  form["symptom"][0].value = name;
  form["location"][0].value = location;
  form["activity"][0].value = activity;
  // Should be converted to 0-4
  form["severity"].value = severity;
  form["occurence"].value = occurence;
  form["date"].value = date;
  form["time"].value = time;
  form["notes"].value = notes;
}

window.onload = function() {
  setDateAndTime();
  checkQueryParams();
};

function checkvalue(elem) {
  if (elem.value === "Other") {
    document.getElementById(elem.name).style.display = "block";
    document.getElementById(elem.name).style.marginTop = "5px";
  } else {
    document.getElementById(elem.name).style.display = "none";
  }
}

function validateForm() {
  document.getElementById("symptom-error-message").innerText = "";
  document.getElementById("location-error-message").innerText = "";
  document.getElementById("activity-error-message").innerText = "";

  const form = document.forms["record-symptom"];
  let valid = true;
  if (form["symptom"][0].value === "Other" && !document.getElementById("symptom").value.length) {
    document.getElementById("symptom-error-message").innerText = "Please specify a symptom";
    valid = false;
  }

  if (form["location"][0].value === "Other" && !document.getElementById("location").value.length) {
    document.getElementById("location-error-message").innerText = "Please specify a location";
    valid = false;
  }

  if (form["activity"][0].value === "Other" && !document.getElementById("activity").value.length) {
    document.getElementById("activity-error-message").innerText = "Please specify an activity";
    valid = false;
  }

  return valid;
}