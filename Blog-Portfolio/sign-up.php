<!DOCTYPE html>
<html lang="en">
<head>
    <title>Sign up</title>
    <link rel = "stylesheet" title = "singup" type = "text/css" href = "signup.css">
    <link rel = "stylesheet" title = "reset" type = "text/css" href = "reset.css">
    <link rel="stylesheet" title = "signup-mobile" type = "text/css" href="signup-mobile.css">
    <script defer src="check-credentials.js"></script>
</head>
<body>
    <div class="wrapper">
        <header>
            <a href="index.php" id = "top-left-credit">&copy; Code by Jose David</a>

            <nav>
                <ul>
                    <li><a href="index.php">Home</a></li>
                    <li><a href="login.php"  class = "active">Blog</a></li>
                    <li><a href="projects.php">Projects & Skills</a></li>
                    <li><a href="about.php">About</a></li>
                </ul>
            </nav>

            <div class="nav-right"> 
                <a href="login.php" id = "login">Log In</a>
                <a href="mailto: dmarin642@gmail.com" class = "nav-contact">Contact</a>

            </div>

            
        </header>

        <main>
            <form method = "POST" action= "signup-processing.php" id = "form">
                <fieldset>
                        <h1>Sign up</h1>
                        <div class="fields fname">
                            <label for = "fname">Fisrt Name</label>
                            <br>
                            <input type = "text" name = "fname" id = "fname" placeholder = "John" required>
                            <br>
                        </div>

                        <div class="fields sname">
                            <label for = "sname">Second Name</label>
                            <br>
                            <input type = "text" name = "sname" id = "sname" placeholder = "Smith" required>
                            <br>
                        </div>

                        <div class="fields email">
                            <label for = "email">Email Address</label>
                            <br>
                            <input type = "email" name = "email" id = "email" placeholder = "example@gmail.com" required>
                            <br>
                        </div>

                        <div class="password">
                            <label for = "password">Password</label>
                            <br>
                            <input type = "password" name = "password" id = "password" minlength = "1" placeholder = "Enter password"required>
                            <br>
                        </div>

                        <div class="fields password">
                            <label for = "password-confirmation">Confirm Password</label>
                            <br>
                            <input type = "password" name = "password-confirmation" id = "password-confirmation" placeholder = "Re-enter password" required>
                            <br>
                        </div>
                        Already have an account?
                        <a href="login.html" class = "forgot-password"><strong>Log in!</strong></a>
                        <p id = "error"></p>
                        <div class="button-container">
                            <a href="blog.html"><button type = "submit">Sign Up</button></a>
                        </div>
                </fieldset>
            </form>
        </main>
        
        <footer>
            <ul>
                
                <li><a href="https://www.instagram.com/davidd.jj/" class = "instagram">Instagram</a></li>
                <li><a href="mailto: dmarin642@gmail.com" class = "Email">Email</a></li>
                <li><a href="https://www.linkedin.com/in/jose-david-marin-acosta-b7026825a/" class = "linkedIn">LinkedIn</a></li>
            </ul>
        </footer>
    </div>
</body>
</html>