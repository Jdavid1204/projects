<!-- Session start in every page in order to keep user's session. -->

<?php

    session_start();

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Londrina+Outline&family=Londrina+Shadow&family=Nabla&family=Noto+Serif+Khmer:wght@300&display=swap" rel="stylesheet">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Russo+One&display=swap" rel="stylesheet">
    <link rel = "stylesheet" type = "text/css" href = "index.css">
    <link rel="stylesheet" title = "index-mobile" type = "text/css" href="index-mobile.css">
    <link rel="stylesheet" title = "reset" type = "text/css" href="reset.css">


</head>
<body>
    <div class="wrapper">
        <header>
            <a href="index.php" id = "top-left-credit">&copy; Code by Jose David</a>

            <nav>
                <ul>
                    <li><a href="index.php" class = "active">Home</a></li>
                    <!-- Checks if user has logged in by checking a and set id.-->
                    <!-- If id is set then the user can access blog direclty without logging in.-->
                    <?php
                        if (isset($_SESSION["id"])) {
                            echo "<li><a href='viewBlog.php'>Blog</a></li>";
                        }
                        else {
                            echo "<li><a href='login.php'>Blog</a></li>";
                        }
                    ?>
                    <li><a href="projects.php">Projects & Skills</a></li>
                    <li><a href="about.php" class = "top-buttons">About</a></li>
                </ul>
            </nav>

            <div class="nav-right"> 
                        <?php
                            if (isset($_SESSION["id"])) {
                                echo "<a href='logout.php' class = 'active'>Log out</a>";
                            }
                            else {
                                echo "<a href='login.php' id = 'login'>Log In</a>";
                            }
                        ?>
                <a href="mailto: dmarin642@gmail.com" class = "nav-contact">Contact</a>

            </div>

            
        </header>

        <div class="intro-content-wrapper">
            <span>👋, Hello my name is Jose David and this is my...</span>
            <div class="heading1"><a href="about.html">Webdesigner</a></div>
            <div class="heading2"><a href="about.html">Portfolio</a></div>
            <div class="version"><a href="#">version number 1.</a></div>
            <img src="images/mypicture Background Removed.png" alt="Picture of Jose David" class = "main-image">
        </div>


    </div>
</body>
</html>