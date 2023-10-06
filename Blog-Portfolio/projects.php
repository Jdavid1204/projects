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
    <title>Projects</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Londrina+Outline&family=Londrina+Shadow&family=Nabla&family=Noto+Serif+Khmer:wght@300&display=swap" rel="stylesheet">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Russo+One&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="projects.css?v=<?php echo time(); ?>">
    <link rel="stylesheet" title = "projects-mobile" type = "text/css" href="projects-mobile.css">
    <link rel="stylesheet" title = "reset" type = "text/css" href="reset.css">
</head>
<body>


    <div class="wrapper">
        <header>
            <a href="index.php" id = "top-left-credit">&copy; Code by Jose David</a>

            <nav>
                <ul>
                    <li><a href="index.php">Home</a></li>
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
                    <li><a href="projects.php" class = "active">Projects & Skills</a></li>
                    <li><a href="about.php">About</a></li>
                </ul>
            </nav>

            <div class="nav-right">
                        <!-- Checks is user has loggend in by checking if an id has been set -->
                        <!-- If it has set then the option of logging out appears. Otherwise just log in button-->
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
        <section>
            <h1>My Projects</h1>
            <div class="projects-container">
                <div class="flexbox-container">
                    <a href="project1.html"  class="project project1">
                    </a>
                    <a href="project2.html"  class="project project2">
                    </a>
                </div>
            </div>
        </section>
        <aside class = "skills">
            <h1 class = "title-aside">Top 3 Skills</h1>
            <div class="skill-container">
                <div class="bar">
                    <label for = "text">HTML</label>
                    <progress id = "text" value = "80" max = "100"> 80% </progress>
                </div>
                <div class="bar">
                    <label for = "text">CSS</label>
                    <progress id = "text" value = "75" max = "100"> 75% </progress>
                </div>
                <div class="bar">
                    <label for = "text">JavaScript</label>
                    <progress id = "text" value = "40" max = "100"> 40% </progress>
                </div>
            </div>
        </aside>
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