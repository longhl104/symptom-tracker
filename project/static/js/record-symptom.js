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

window.onload = function() {
  setDateAndTime();
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
  document.getElementById("activity-error-message").innerText = "";

  const form = document.forms["record-symptom"];
  let valid = true;
  if (form["symptom"][0].value === "Other" && !document.getElementById("symptom").value.length) {
    document.getElementById("symptom-error-message").innerText = "Please specify a symptom";
    valid = false;
  }

  if (form["activity"][0].value === "Other" && !document.getElementById("activity").value.length) {
    document.getElementById("activity-error-message").innerText = "Please specify an activity";
    valid = false;
  }

  return valid;
}