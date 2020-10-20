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

clinicians = document.currentScript.getAttribute('clinicians').split(",");
window.onload = function() {
    var ul = document.getElementById('cl-list-container');

    if (clinicians == null || clinicians == '' || clinicians.length == 0) {
        empty = document.createElement("div");
        empty.appendChild(document.createTextNode("You have not linked any clinicians."))
        ul.appendChild(empty);
    }
    else {
        for (var i = 0; i < clinicians.length; i++) {
            var li = document.createElement("li");
            li.appendChild(document.createTextNode(clinicians[i]));

            var span = document.createElement("span");
            span.setAttribute('class', 'close');
            span.setAttribute('id', clinicians[i]);
            span.setAttribute('onclick', 'deleteClinician(id)');
            span.appendChild(document.createTextNode("x"));

            li.appendChild(span);
            ul.appendChild(li);
        }
    }
};