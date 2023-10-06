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
    <title>About Me</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Acme&family=Londrina+Outline&family=Londrina+Shadow&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="about.css?v=<?php echo time(); ?>">
    <link rel="stylesheet" title = "mobile" type = "text/css" href="about-mobile.css">
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
                    <li><a href="projects.php">Projects & Skills</a></li>
                    <li><a href="about.php" class = "active">About</a></li>
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
        <div class="about-section-wrapper">
            <div class="top-container">
                <div class="left-column">
                    <article> <!--Left column-->
                        <hgroup>
                            <h1>Hi again,</h1>
                            <h1> this is</h1>
                            <h1>Jose David</h1>
                        </hgroup>

                       <div class="relevant-links"> 
                            <ul>
                                <li><a href="https://www.instagram.com/davidd.jj/" class = "social-link">Instagram</a></li>
                                <li><a href="mailto: dmarin642@gmail.com" class = "social-link">Email</a></li>
                                <li><a href="https://www.linkedin.com/in/jose-david-marin-acosta-b7026825a" class = "resume">Resume</a></li>
                            </ul>
                        </div>
                    </article>
                </div>

                <img class = "right-column"src="images/IMG_3849.jpeg" alt="Picture of Jose David ">
            </div>

            <div class="aboutme-container">
                <h1>About Me</h1>
                <div class="about-me">
                    Hello! I'm a computer enthusiast with a passion for learning about the intricacies of computer 
                    hardware, cloud computing, and the theory of computation. I find it fascinating to understand how the 
                    components of a computer work together to produce powerful computing capabilities, and how 
                    cloud computing has revolutionized the way we store and access data. I also enjoy diving into the abstract 
                    world of theory of computation and exploring the fundamental principles of computation. When I'm not busy exploring 
                    these topics, you can find me playing video games or on the football field. I am a very sociable and charismatic person, and 
                    I love meeting new people and making new connections.
                    <div class="box">👈👈</div>
                </div>
            </div>
            <div class="education-container">
                <h1>Education</h1>
                <div class="education-content">
                    <div id = "secondary">
                        <p class = "year">2015-&emsp;&emsp;Secondary School - The Elmgreen School</p>
                        <p>2020</p>
                    </div>
                    <div id = "sixth">
                        <p class = "year">2020-&emsp;&emsp;Sixth Form - The Elmgreen School Sixth Form</p>
                        <p>2022</p>
                    </div>
                    <p>2022-&emsp;&emsp;BSc Computer Science - Queen Mary University of London</p>
                    <div class="box2">✍️</div>
                </div>
            </div>

            <div class="experience-container">
                <h1>Experience</h1>
                <div class="experience-content">
                    I have been working with HTML and CSS for several weeks 
                    now, and I am very comfortable with both languages
                    . I have used them to build a variety of websites.
                     When I start a new project, I am always excited to dive into 
                    the code and start building the layout and structure of the site. I have a good understanding of responsive design principles, and 
                    I am able to create websites that look great on any device. Overall, I feel confident in my abilities with HTML and CSS, and I am always eager to continue learning and improving my skills.

                    <div class="box3">📖</div>
                </div>
            </div>
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