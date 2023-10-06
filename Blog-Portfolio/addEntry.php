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
    <link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Tiro+Telugu&display=swap" rel="stylesheet">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Acme&family=Londrina+Outline&family=Londrina+Shadow&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="addEntry.css?v=<?php echo time(); ?>">
    <link rel="stylesheet" title = "addEntry-mobile" type = "text/css" href="addEntry-mobile.css">
    <link rel="stylesheet" title = "reset" type = "text/css" href="reset.css">

    <script defer src="addEntry.js"></script>
</head>
<body>
    <article>
        <div class="wrapper">
            <header>
                <a href="index.php" id = "top-left-credit">&copy; Code by Jose David</a>

                <nav>
                    <ul>
                        <li><a href="index.php">Home</a></li>
                        <!-- Checks if user has logged in by checking a and set id.-->
                        <!-- If id is set then the user can access blog direclty without logging-->
                        <?php
                            if (isset($_SESSION["id"])) {
                                echo "<li><a href='viewBlog.php' class = 'active'>Blog</a></li>";
                            }
                            else {
                                echo "<li><a href='login.php' class = 'active'>Blog</a></li>";
                            }
                        ?>
                        <li><a href="projects.php">Projects & Skills</a></li>
                        <li><a href="about.php">About</a></li>
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
            <div class="form-container-blog">
                <section>
                    <div class="hgroup">
                        <h1 class ="first">Add a</h1>
                        <h1 class = "second">Post</h1>
                        <a href="#Blog-form" class="welcome">Just do it here 👀👇</a>
                    </div>
                </section>
                <main>
                    <form method = "POST" action= "addPost.php" id ="Blog-form">
                        <fieldset>
                                <div class="hgroup-in-blog">
                                    <h1 class = "heading heading1-blog">Wanna add a post to our blog?</h1>
                                </div>
                                <div class="fields headline">
                                    <label for = "title">Headline</label>
                                    <br>
                                    <input type = "text" name = "title" id = "title" placeholder = "Global Warming">
                                    <br>
                                </div>

                                <div class="fields main-content">
                                    <label for = "content">Content</label>
                                    <br>
                                    <textarea name = "content" id = "content" placeholder = "Global warming, also known as climate change, is one of the most pressing issues in our planet."></textarea>
                                    <br>
                                </div>
                                <p id="error"></p>
                                <div class="button-container">
                                    <a href="blog.html"><button type = "submit" class = "submit" >Post</button></a>
                                    <button class = "clear" type = "button" onclick="clearIt()">Clear</button>
                                </div>
                        </fieldset>
                    </form>
                </main>
            </div>
        <footer>
            <ul>
                
                <li><a href="https://www.instagram.com/davidd.jj/" class = "instagram">Instagram</a></li>
                <li><a href="mailto: dmarin642@gmail.com" class = "Email">Email</a></li>
                <li><a href="https://www.linkedin.com/in/jose-david-marin-acosta-b7026825a/" class = "linkedIn">LinkedIn</a></li>
            </ul>
        </footer>
        </div>
    </article>

</body>
</html>