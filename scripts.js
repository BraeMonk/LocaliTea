// Login functionality
document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    const loginError = document.getElementById('login-error');

    // Check if the user exists in localStorage
    const storedUser = JSON.parse(localStorage.getItem(username));

    if (storedUser && storedUser.password === password) {
        if (storedUser.verified) {
            switchToHomePage();
        } else {
            loginError.textContent = 'Please verify your email before logging in.';
        }
    } else {
        loginError.textContent = 'Invalid username or password. Please try again.';
    }
});

// Signup functionality
document.getElementById('signUpButton').addEventListener('click', () => {
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;

    fetch('http://localhost:5000/send-verification-email', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, email })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        alert(data.message);  // Show success message to the user
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to send verification email');
    });
});

// Toggle between login and signup forms
function toggleForms() {
    const loginPage = document.getElementById('login-page');
    const signupPage = document.getElementById('signup-page');

    if (loginPage.style.display === 'none') {
        loginPage.style.display = 'block';
        signupPage.style.display = 'none';
    } else {
        loginPage.style.display = 'none';
        signupPage.style.display = 'block';
    }
}

// Switch to home page after successful login
function switchToHomePage() {
    document.getElementById('login-page').style.display = 'none';
    document.getElementById('signup-page').style.display = 'none';
    document.getElementById('navbar').style.display = 'flex';
    document.getElementById('home').style.display = 'block';
    document.getElementById('bottom-nav').style.display = 'flex';
}

// Toggle messages tab
function toggleMessages() {
    const messagesTab = document.getElementById('messages-tab');
    messagesTab.style.display = (messagesTab.style.display === 'none') ? 'block' : 'none';
}

// Show content of selected tab
function showTab(tabName) {
    const tabs = document.getElementsByClassName('tab-content');
    for (const tab of tabs) {
        tab.style.display = 'none';
    }
    document.getElementById(tabName).style.display = 'block';
}

// Logout functionality
function logout() {
    document.getElementById('navbar').style.display = 'none';
    document.getElementById('home').style.display = 'none';
    document.getElementById('bottom-nav').style.display = 'none';
    document.getElementById('login-page').style.display = 'block';
}

// Save user profile information
function saveUserProfile() {
    const username = document.getElementById('login-username').value;
    const user = JSON.parse(localStorage.getItem(username));
    user.name = document.getElementById('user-name-input').value;
    user.bio = document.getElementById('user-bio-input').value;
    user.businessName = document.getElementById('business-name-input').value;
    user.businessAddress = document.getElementById('business-address-input').value;
    localStorage.setItem(username, JSON.stringify(user));
}
