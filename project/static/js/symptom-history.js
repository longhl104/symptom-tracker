function deleteRecord(id) {
  const confirmation = confirm("Are you sure you would like to delete this record?");
  if (confirmation) {
    fetch("/patient/record-symptom/" + id, {
      method: "DELETE",
    })
    .then(res => {
      if (!res.ok) {
        console.log("Error", res);
      } else {
        console.log("Success", res);
        location.reload();
      }
    });
  }
}

function editRecord(id, name, location, severity, occurence, date, notes) {
  window.location.href = '/patient/record-symptom?' + encodeURI(`id=${id}&name=${name}&location=${location}&severity=${severity}&occurence=${occurence}&date=${date}&notes=${notes}`);
}

function showHideNotes(id) {
  var notes = document.getElementById(`notes-${id}`);
  var notesIcon = document.getElementById(`expand-text-${id}`);
  if (notes.style.display === "none") {
    notes.style.display = "block";
    notesIcon.setAttribute("style", "-webkit-transform: rotate(180deg);-moz-transform: rotate(180deg);-o-transform: rotate(180deg);-ms-transform: rotate(180deg);transform: rotate(180deg);")
  } else {
    notes.style.display = "none";
    notesIcon.removeAttribute("style");
  }
}

