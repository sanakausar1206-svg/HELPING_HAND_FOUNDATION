// Small JavaScript example: show a welcome message
function showWelcome() {
  alert("Welcome to Helping Hands Foundation!");
}

// Check that a form is ready to submit
function checkForm(form) {
  if (!form.checkValidity()) {
    alert("Please fill in all required fields correctly.");
    return false;
  }
  return true;
}