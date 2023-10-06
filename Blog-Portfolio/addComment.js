// Get the button element by its ID
const addCommentBtn = document.getElementById('addCommentBtn');

// Add a click event listener to the button
addCommentBtn.addEventListener('click', function() {
  // Check if the form already exists
  if (document.getElementById('commentForm') === null) {
    // Create a new form element
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = 'addComment.php';
    form.id = 'commentForm';

    // Create a new label element
    const label = document.createElement('label');
    label.setAttribute('for', 'comment');
    label.innerText = 'Add comment';

    // Create a new textarea element
    const textarea = document.createElement('textarea');
    textarea.name = 'comment';
    textarea.id = 'comment';
    textarea.placeholder = 'Add comment';

    // Append the label and textarea elements to the form
    form.appendChild(label);
    form.appendChild(document.createElement('br'));
    form.appendChild(textarea);
    form.appendChild(document.createElement('br'));

    // Append the form to the body of the HTML document
    document.body.appendChild(form);
  }
});