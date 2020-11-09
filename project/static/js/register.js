window.onload = function () {
  var checkList = document.getElementById("multi-checklist");

  checkList.getElementsByClassName("anchor")[0].onclick = function(evt) {
    if (checkList.classList.contains("visible")) {
      checkList.classList.remove("visible");
    } else {
      checkList.classList.add("visible");
    }
    selectChanged();
}
};

function selectChanged() {
  var notype = document.getElementById("notype").checked;
  var unknowntype = document.getElementById("unknowntype").checked;
  items = document.getElementById("treatments").getElementsByTagName("LI");
  if (notype) {
    for (var i = 0; i < items.length; i++) {
      if (items[i].firstChild.id != "notype") {
        items[i].firstChild.checked = false;
        items[i].firstChild.disabled = true;
      }
    }
  } else if (unknowntype) {
    for (var i = 0; i < items.length; i++) {
      if (items[i].firstChild.id != "unknowntype") {
        items[i].firstChild.checked = false;
        items[i].firstChild.disabled = true;
      }
    }
  } else {
    for (var i = 0; i < items.length; i++) {
      items[i].firstChild.disabled = false;
    }
  }
};

function validateForm() {
  document.getElementById("error-message").innerText = "";
  const form = document.forms["register-form"];
  let valid = true;

  if (form["first-name"].value == "") {
    document.getElementById("error-message").innerText = "First name must be filled out";
    valid = false;
  }

  if (form["last-name"].value == "") {
    document.getElementById("error-message").innerText = "Last name must be filled out";
    valid = false;
  }

  if (form["email"].value == "") {
    document.getElementById("error-message").innerText = "Email must be filled out";
    valid = false;
  }

  if (form["password"].value !== form["confirm-password"].value) {
    document.getElementById("error-message").innerText = "Passwords do not match";
    valid = false;
  }

  return valid;
}
