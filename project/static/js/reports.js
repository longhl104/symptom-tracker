function setDate() {
    var date = new Date();
  
    var day = date.getDate(),
        month = date.getMonth() + 1,
        year = date.getFullYear();
    
    month = (month < 10 ? "0" : "") + month;
    day = (day < 10 ? "0" : "") + day;
    
    var today = year + "-" + month + "-" + day;
    
    document.getElementById('startDate').value = today;
    document.getElementById('endDate').value = today;
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
    let name = getParameterByName('name');
    let location = getParameterByName('location');
    const startDate = getParameterByName('startDate');
    const endDate = getParameterByName('endDate');
  
    const form = document.forms["make-graph"];
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
    
    if (startDate) form["startDate"].value = startDate;
    if (endDate) form["endDate"].value = endDate;
  }
  
  window.onload = function() {
    //setDate();
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
  
    const form = document.forms["make-graph"];
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

  function editRecord(name, location, startDate, endDate) {
    window.location.href = '/patient/reports?' + encodeURI(`name=${name}&location=${location}&startDate=${startDate}&endDate=${endDate}`);
  }