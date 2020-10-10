function deleteRecord(id) {
  fetch("/patient/record-symptom/" + id, {
    method: "DELETE",
  })
  .then(res => {
    if (!res.deleted) {
      console.log("Error", res);
    } else {
      console.log("Success", res);
      location.reload();
    }
  })
}

function editRecord(id, name, location, activity, severity, occurence, date, time, notes) {
  // console.log(id, name, location, activity, severity, occurence, date, time, notes)
  window.location.href = '/patient/record-symptom?' + encodeURI(`id=${id}&name=${name}&location=${location}&activity=${activity}&severity=${severity}&occurence=${occurence}&date=${date}&time=${time}&notes=${notes}`);
}