function checkvalue(elem) {
  if (elem.value === "Other") {
    document.getElementById(elem.name).style.display = "block";
    document.getElementById(elem.name).style.marginTop = "5px";
  } else {
    document.getElementById(elem.name).style.display = "none";
  }
}