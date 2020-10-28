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
  var notesIcon = document.getElementById(`notes-arrow-${id}`);
  if (notes.style.display === "none") {
    notes.style.display = "block";
    notesIcon.classList.remove('fa-caret-down');
    notesIcon.classList.add('fa-caret-up');
  } else {
    notes.style.display = "none";
    notesIcon.classList.remove('fa-caret-up');
    notesIcon.classList.add('fa-caret-down');
  }
}

