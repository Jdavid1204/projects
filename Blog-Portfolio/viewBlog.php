<!-- Session start in every page in order to keep user's session. -->

<?php

    session_start();

    $servername = "127.0.0.1"; 
    $username = "root"; 
    $password = "root"; 
    $dbname = "ecs417"; 
    // Creates connection 
    $conn = new mysqli($servername, $username, $password, $dbname); 
    // Checks connection 
    if ($conn->connect_error) { die("Connection faileeddd: " . $conn->connect_error); } 
        $select = mysqli_query($conn,"SELECT * FROM BLOG");
        $counter = 0;
        $dates = array();


        while ($row = mysqli_fetch_array($select)) {
            //output a row here
            $dates[$counter] = $row['date'];
            $counter ++;
        }

        for ($i = 0; $i < count($dates); $i ++){
            for ($j =$i + 1; $j < count($dates); $j ++ ){
                if ($dates[$i] < $dates[$j]){
                    $temp = $dates[$i];
                    $dates[$i] = $dates[$j];
                    $dates[$j] = $temp;
                }

            }
        }


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
    <link rel="stylesheet" href="viewBlog.css?v=<?php echo time(); ?>">
    <link rel="stylesheet" title = "viewBlog-mobile" type = "text/css" href="viewBlog-mobile.css">
    <link rel="stylesheet" title = "reset" type = "text/css" href="reset.css">
    <script defer src="addComment.js"></script>


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
                                echo "<a href='login.html' id = 'login'>Log In</a>";
                            }
                        ?>
                    <a href="mailto: dmarin642@gmail.com" class = "nav-contact">Contact</a>

                </div>
            </header>
            <div class="form-container-blog">
                <section>
                    <div class="hgroup">
                        <h1 class ="the">The </h1>
                        <h1 class = "newsfeed">newsfeed</h1>
                        <p class="welcome">Welcome back , <?php echo $_SESSION['name'];?> 😎</p>
                    </div>
                </section>
                <div class="addpost-wrap">
                    <a href="addEntry.php" class="addpost">Add post</a>
                </div>
                <figure>
                    <img src="images/person-in-office.webp" alt="picture" class = "office-image">
                </figure>
                <div class="blog-posts-container">
                <?php 
                    $i = 0;
                    foreach($dates as $date){
                        $select = mysqli_query($conn,"SELECT * FROM BLOG WHERE date=  '$date'");
                        $row = mysqli_fetch_array($select);
                        $title = $row['title'];
                        $content = $row['content'];
                        $author = $row['author'];
                        $date = $row['date'];

                        $class = $i % 2;
                        if ($class === 0){
                            $class = '';
                        }

                        else {
                            $class = 'right';
                        }
                        $i++;

                        $emojis = ['💸', '📖', '💣','🔑', '🎉','📝','📌']; // an array for emojis
                        $random_number = rand(0, 6); // generate a random number between 0 and 2
                        $emoji = $emojis[$random_number]; // use the random number to select a corresponding emoji from the array


 



                        echo "
                            <div class='experience-container $class'>
                                <div class='experience-content'>
                                    <h1>$title</h1>
                                    $content
                                    <div class='footer-post'>
                                        <h4>By $author ✍️</h4>
                                        <p>🗓️ $date</p>
                                    </div>
                                    <div class='box3'>$emoji</div>
                                    <form id = 'commentForm' method = 'POST' action='addComment.php'>
                                    <p><?php ?></p>
                                        <label for = 'comment' id = 'commentLabel'>Add comment</label>
                                        <br>
                                        <textarea name = 'comment' id = 'comment' placeholder = 'Add comment' required></textarea>
                                        <br>
                                        <button type = 'submit' class = 'submit' >Comment</button>
                                    </form>
                                </div>
                            </div>
                        ";
                    }



                    ?>

                    <div class="comments">
                        <h3>Comments</h3>
                    </div>
                    <div class="comments">

                        <?php                                    
                        
                                //comments

                                $sql = "SELECT * FROM COMMENTS";
                                $resultCom = mysqli_query($conn, $sql);
                                                
                                if (mysqli_num_rows($resultCom) > 0){
                                    while($rowComment = mysqli_fetch_assoc($resultCom)){
                                        $userComment =  $rowComment['user'];
                                        $message = $rowComment['messages'];
                                        $time = $rowComment['date'];
                                        echo "<div class='comments-order'>";
                                        echo "<h4>Comment from $userComment</h4>";
                                        echo "<p> at $time</p>";
                                        echo "<p id = 'message'>$message</p>";
                                        echo "</div>";

                        
                        
                                    }
                                }



                                if ($_SESSION["id"]== 7){

                                    echo "
                                    <h1>Delete Entry or Comment</h1>
                                    <form method='post'>
                                        <p>
                                            <label for='id2'>ID:</label>
                                            <input type='number' name='id2' required>
                                        </p>
                                        <p>
                                        <label for='type'>Type:</label>
                                        <select name='type' required>
                                                <option value='entry'>Entry</option>
                                                <option value='comment'>Comment</option>
                                            </select>
                                        </p>
                                        <input type='submit' name='delete' value='delete'>
                                        </form>
                    
                                        </div>
                    
                    
                                    </div>
                    
                                </div>
                                    
                                    ";
                                // check if form is submitted
                                if ($_SERVER['REQUEST_METHOD'] == 'POST') {
                                    $id = $_POST['id2'];
                                    $type = $_POST['type'];

                                    // delete entry or comment from database
                                    if ($type == 'entry') {
                                        $sql = "DELETE FROM BLOG WHERE ID = '$id'";
                                    } else if ($type == 'comment') {
                                        $sql = "DELETE FROM COMMENTS WHERE ID = '$id'";
                                    }
                                }
                                $servername = "127.0.0.1"; 
                                $username = "root"; 
                                $password = "root"; 
                                $dbname = "ecs417"; 
                                // Creates connection 
                                $conn = new mysqli($servername, $username, $password, $dbname); 
                                $result = mysqli_query($conn, $sql);


 
                            }
                        ?>






        </div>
    </article>


</body>
</html>