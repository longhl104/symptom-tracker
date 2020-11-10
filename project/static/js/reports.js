function getConfirmation(type) {

  let message = ""
  if (type === "image") {
    message = "Export a graph of this symptom data? This will download a .svg file to your device."
  } else {
    message = "Export this symptom data? This will download a .csv file to your device."
  }

  console.log(message)

  let confirmation = confirm(message);
  if (confirmation) {
    return true
  } else {
    return false;
  }
}

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
  
  function checkQueryParams() {
    let symptomList = document.getElementById('symptom-list');
    let locationList = document.getElementById('location-list');
    
    if (symptomList.selectedIndex == 1) {
      locationList.getElementsByTagName("option")[1].disabled = true;
    }

    if (locationList.selectedIndex == 1) {
      symptomList.getElementsByTagName("option")[1].disabled = true;
    }

  }
  
  window.onload = function() {
    checkQueryParams();
  };
  
  function checkvalue(elem) {
    if (elem) {
      if (elem.name === "symptom") {
        var toGreyOut = "location-list"
      }
      else if (elem.name === "location") {
          var toGreyOut = "symptom-list"
      }
      if (toGreyOut) {
        if (elem.value === "All") {
          var options = document.getElementById(toGreyOut).getElementsByTagName("option"); 
          for (var i = 0; i < options.length; i++) {
            if (options[i].value == "All") {
              options[i].disabled = true;
            }
          }
        } else {
          var options = document.getElementById(toGreyOut).getElementsByTagName("option");
          for (var i = 0; i < options.length; i++) {
              options[i].disabled = false;
          }
        }
      }
        
      if (elem.value === "Other") {
        document.getElementById(elem.name).style.display = "block";
        document.getElementById(elem.name).style.marginTop = "5px";
      } else {
        document.getElementById(elem.name).style.display = "none";
      }
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
    if (form["symptom"][0].value === "All" && form["location"][0].value === "All") {
      document.getElementById("both-error-message").innerText = "Cannot select both 'All Symptoms' and 'All Locations'";
      valid = false;
    }
  
    return valid;
  }

  function editRecord(name, location, startDate, endDate) {
    window.location.href = '/patient/reports?' + encodeURI(`name=${name}&location=${location}&startDate=${startDate}&endDate=${endDate}`);
  }