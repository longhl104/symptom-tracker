window.onload = function () {
  const today = new Date();
  const currentHour = today.getHours();
  var greeting = 'Welcome, ';

  greeting = currentHour < 12 ? "Good morning, " : currentHour < 18 ? "Good afternoon, " : "Good evening, ";

  document.getElementById("heading").innerHTML = greeting + document.getElementById("heading").innerHTML;
  document.getElementById("heading").style.display = "block";

  todays_date();
  setup_tab_onchange();
  on_questionnaire_change();
  delete_form_submit_override();
};

function todays_date() {
  document.getElementById("end-date").valueAsDate = new Date();
}

function show_form_content(id) {
  for (let i = 1; i < 4; i++) {
    document.getElementById(`content-${i}`).style.display = i === id ? 'block' : 'none';
  }
}

function setup_tab_onchange() {
  var radios = document.querySelectorAll('input[type=radio][name="tab-group-1"]');

  function changeHandler(event) {
    show_form_content(parseInt(this.id.slice(this.id.length - 1)));
    const modifyForm = document.getElementById('modify-form');
    const modifyFormActive = modifyForm.action.slice(modifyForm.action.length - 7) !== '/admin/';
    if (this.id === 'tab-1') {
      document.getElementById('modify-form-div').style.display = 'none';
      document.getElementById("tabs").style.minHeight = '480px';
    } else if (this.id === 'tab-2') {
      if (modifyFormActive) {
        document.getElementById('modify-form-div').style.display = 'grid';
        document.getElementById("tabs").style.minHeight = '430px';
      } else {
        document.getElementById("tabs").style.minHeight = '200px';
      }
    } else if (this.id === 'tab-3') {
      document.getElementById('modify-form-div').style.display = 'none';
      document.getElementById("tabs").style.minHeight = '200px';
    }  
  }

  Array.prototype.forEach.call(radios, function(radio) {
    radio.addEventListener('change', changeHandler);
  });
}

function clean_up_modify_form(name='', link='', date=null) {
  let form = document.forms['modify-form'];
  if (form) {
    form['questionnaire-name'].value = name;
    form['survey-link'].value = link;
    form['end-date'].value = date;
  }
}

function on_questionnaire_change() {
  document.getElementById('modify-questionnaire').addEventListener('change', function() {
    const id = document.getElementById('modify-questionnaire').value;
    if (id !== 'None') {
      fetch("/admin/questionnaire/" + id, {
        method: "GET",
      })
        .then(res => res.json())
        .then(res => {
          if (res.questionnaire && res.questionnaire.length) {
            const questionnaire = res.questionnaire[0];
            let form = document.forms['modify-form'];
            form['questionnaire-name'].value = questionnaire.name;
            form['survey-link'].value = questionnaire.link;
            form['end-date'].valueAsDate = new Date(questionnaire.start_date);
            document.getElementById('modify-form').action = '/admin/questionnaire/' + questionnaire.id;
            document.getElementById('modify-form-div').style.display = 'grid';
            document.getElementById('modify-form-div').style.marginTop = '10px';
            document.getElementById("tabs").style.minHeight = '480px';
          } else {
            document.getElementById('modify-form-div').style.display = 'none';
            document.getElementById('modify-form-div').style.marginTop = '0px';
            document.getElementById('modify-message').classList.remove("success-message");
            document.getElementById('modify-message').classList.add("error-message");
            document.getElementById('modify-message').innerText = "Failed to load questionnaire";
            document.getElementById("tabs").style.minHeight = '200px';
          }
        });
    } else {
      clean_up_modify_form();
      document.getElementById('modify-form').action = '/admin/';
      document.getElementById('modify-form-div').style.display = 'none';
      document.getElementById('modify-form-div').style.marginTop = '0px';
      document.getElementById("tabs").style.minHeight = '200px';
    }
  });
}
  
function delete_form_submit_override() {
  document.getElementById('delete-form').onsubmit = function(event) {
    event.preventDefault();
    const id = document.getElementById('delete-questionnaire').value;
    const confirmation = confirm("Are you sure you would like to delete this questionnaire?");
    if (confirmation) {
      fetch("/admin/questionnaire/" + id, {
        method: "DELETE",
      })
        .then(res => {
          if (!res.ok) {
            document.getElementById('delete-message').classList.remove("success-message");
            document.getElementById('delete-message').classList.add("error-message");
            document.getElementById('delete-message').innerText = "Failed to delete questionnaire!";
          } else {
            document.getElementById('delete-message').classList.remove("error-message");
            document.getElementById('delete-message').classList.add("success-message");
            document.getElementById('delete-message').innerText = "Questionnaire was deleted successfully!";
            let select = document.getElementById('delete-questionnaire');
            for (let i = 0; i < select.length; i++) {
              if (select.options[i].value == id) select.remove(i);
            }
            let modifyForm = document.getElementById('modify-questionnaire');
            console.log('modifyForm', modifyForm)
            if (modifyForm) {
              modifyForm.selectedIndex = 0;
              for (let i = 0; i < modifyForm.length; i++) {
                if (modifyForm.options[i].value == id) modifyForm.remove(i);
              }
            clean_up_modify_form();
            document.getElementById('modify-form-div').style.display = 'none';
            document.getElementById('modify-form-div').style.marginTop = '0px';
            document.getElementById("tabs").style.minHeight = '200px';
            }
          }
        });
    }
    return false;
  }
}