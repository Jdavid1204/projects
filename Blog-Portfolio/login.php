<?php
$servername = "127.0.0.1"; 
    $username = "root"; 
    $password = "root"; 
    $dbname = "ecs417"; 
    // Creates connection 
    $conn = new mysqli($servername, $username, $password, $dbname); 
    // Checks connection 
    if ($conn->connect_error) { die("Connection faileeddd: " . $conn->connect_error); } 
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <title>Log in</title>
    <link rel="stylesheet" href="login.css?v=<?php echo time(); ?>">
    <link rel="stylesheet" title = "login-mobile" type = "text/css" href="login-mobile.css">
    <link rel = "stylesheet" title = "reset" type = "text/css" href = "reset.css">
</head>
<body>
    <div class="wrapper">
        <header>
            <a href="index.php" id = "top-left-credit">&copy; Code by Jose David</a>

            <nav>
                <ul>
                    <li><a href="index.php">Home</a></li>
                    <li><a href="login.php">Blog</a></li>
                    <li><a href="projects.php">Projects & Skills</a></li>
                    <li><a href="about.php">About</a></li>
                </ul>
            </nav>

            <div class="nav-right"> 
                <a href="sign-up.php" id = "login">Sign up</a>
                <a href="mailto: dmarin642@gmail.com" class = "nav-contact">Contact</a>

            </div>

            
        </header>

        <main>
            <form method = "POST" action= "login.php">
                <fieldset>
                        <h1>Log In</h1>
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
                        <p id = "error"></p>
                        Not registered?
                        <a href="sign-up.php" class = "forgot-password"><strong>Sign up!</strong></a>
                        <div class="button-container">
                            <a href="blog.html"><button type = "submit">Submit</button></a>
                        </div>
                </fieldset>
            </form>
        </main>
        <?php
        if ($_SERVER['REQUEST_METHOD'] == 'POST'){ 

        $email = $_POST['email'];
        $pass = $_POST['password'];

        $select = mysqli_query($conn,"SELECT * FROM USERS WHERE email=  '$email' AND password = '$pass' ");
        $row = mysqli_fetch_array($select);

        if(is_array($row)){
            session_start();
            $_SESSION["id"] = $row['ID'];
            $_SESSION["email"] = $row['email'];
            $_SESSION["password"] = $row['password'];
            $_SESSION["name"] = $row['firstName'];
        } else {
            echo '<script>const error = document.getElementById("error");</script>';
            echo '<script>error.innerHTML = "Username and password do not match";</script>';
        }
        }

        if (isset($_SESSION["id"])){
            header("Location: viewBlog.php");
        }
        ?>
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