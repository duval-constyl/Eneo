// Initialization for ES Users
import { Input, initMDB } from "mdb-ui-kit";

initMDB({ Input });

// Icon Example
const passwordInput1 = document.getElementById('show-password-input-1');
const toggleIcon = document.getElementById('show-password-toggle-icon');

toggleIcon.addEventListener('pointerdown', (e) => {
  e.preventDefault();

    // Toggle input type between password and text
    if (passwordInput1.type === 'password') {
      passwordInput1.type = 'text';
      toggleIcon.classList.remove('fa-eye');
      toggleIcon.classList.add('fa-eye-slash');
    } else {
      passwordInput1.type = 'password';
      toggleIcon.classList.remove('fa-eye-slash');
      toggleIcon.classList.add('fa-eye');
    }
  });

// Checkbox example
const passwordInput2 = document.getElementById('show-password-input-2');
const toggleCheckbox = document.getElementById('show-password-toggle-checkbox');

toggleCheckbox.addEventListener('change', () => {
  passwordInput2.type = toggleCheckbox.checked ? 'text' : 'password';
});