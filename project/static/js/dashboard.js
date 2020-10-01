// TODO: Replace name with patient name from database
window.onload = function () {
  const today = new Date();
  const currentHour = today.getHours();
  var greeting = 'Welcome, ';

  greeting = currentHour < 12 ? "Good morning, " : currentHour < 18 ? "Good afternoon, " : "Good evening, ";

  document.getElementById("heading").innerHTML = greeting + document.getElementById("heading").innerHTML;
  document.getElementById("heading").style.display = "block";
};