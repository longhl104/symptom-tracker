function deleteClinician(email) {

    if (email == null) {
        console.log("Unknown error");
        return
    }

    const confirmation = confirm("Are you sure you would like to remove this clinician from your account?");
    if (confirmation) {
    fetch("/patient/account/" + email, { method: "DELETE", })
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