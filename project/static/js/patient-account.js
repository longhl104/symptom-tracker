function deleteClinician(email) {

    if (email == null) {
        console.log("Unknown error");
        return
    }

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