function setDate() {
  var date = new Date();

  var day = date.getDate(),
      month = date.getMonth() + 1,
      year = date.getFullYear();
  
  month = (month < 10 ? "0" : "") + month;
  day = (day < 10 ? "0" : "") + day;
  
  var today = year + "-" + month + "-" + day;
  
  document.getElementById('date').value = today;
}

window.onload = function() {
  setDate();
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

  return valid;
}