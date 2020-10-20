function viewHistory(id) {
      fetch("/clinician/view_patients/" + id, {
        method: "GET",
      })
      .then(res => {
        if (!res.ok) {
          console.log("Error", res);
        } else {
          console.log("Success", res);
          window.location.href = "/clinician/view_patients/" + id;
        }
      });
    
  }