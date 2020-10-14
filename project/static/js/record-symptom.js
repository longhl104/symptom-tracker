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
  const severityScale = ["Not at all", "A little bit", "Somewhat", "Quite a bit", "Very much"];
  const id = getParameterByName('id');
  let name = getParameterByName('name');
  let location = getParameterByName('location');
  let severity = severityScale.indexOf(getParameterByName('severity'));
  severity = severity > -1 ? severity : 0;
  const occurence = getParameterByName('occurence');
  const date = getParameterByName('date');
  const notes = getParameterByName('notes');

  const form = document.forms["record-symptom"];
  if (id) form["id"].value = id;

  const validSymptoms = ["Cramping", "Discomfort", "Numbness", "Pain", "Tingling", "Weakness"];
  if (name) {
    if (validSymptoms.indexOf(name) < 0) {
      form["symptom"][0].value = "Other";
      form["symptom"][1].value = name;
      checkvalue(form["symptom"][0]);
    } else {
      form["symptom"][0].value = name;
    }
  }

  const validLocations = ["Hands", "Arms", "Feet", "Legs"];
  if (location) {
    if (validLocations.indexOf(location) < 0) {
      form["location"][0].value = "Other";
      form["location"][1].value = location;
      checkvalue(form["location"][0]);
    } else {
      form["location"][0].value = location;
    }
  }

  form["severity"].value = severity;
  
  if (occurence) form["occurence"].value = occurence;
  if (date) form["date"].value = date;
  if (notes) form["notes"].value = notes;
  setupSlider();
}

window.onload = function() {
  setDate();
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

function setupSlider() {
  let allRanges = document.querySelectorAll(".range-wrap");
  allRanges.forEach(wrap => {
    const range = wrap.querySelector(".range");
    const bubble = wrap.querySelector(".bubble");

    range.addEventListener("input", () => {
      setBubble(range, bubble);
    });
    setBubble(range, bubble);
  });
}

function setBubble(range, bubble) {
  const val = range.value;
  const min = range.min ? range.min : 0;
  const max = range.max ? range.max : 100;
  const newVal = Number(((val - min) * 100) / (max - min));
  const severity = val == 0 ? "Not at all" : val == 1 ? "A little bit" : val == 2 ? "Somewhat" : val == 3 ? "Quite a bit" : "Very much"
  bubble.innerText = severity;

  const translateX = val == 0 ? '-10%' : val == 4 ? '-90%' : '-50%';

  // Shift the bubble to the left based on the current value of the range
  bubble.style.left = `calc(${newVal}% + (${8 - newVal * 0.15}px))`;
  bubble.style.transform = `translateX(${translateX})`;
}