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