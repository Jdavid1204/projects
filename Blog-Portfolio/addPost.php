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

$sql = "SELECT * FROM BLOG";
$query = mysqli_query($conn, $sql); 


if (($_SERVER['REQUEST_METHOD'] == 'POST')){
    $title = $_POST['title'];
    $content = $_POST['content'];
    $author = (string) $_SESSION['name'];
    $sql = "INSERT INTO BLOG (title, content, author) VALUES ('$title', '$content', '$author')";
    mysqli_query($conn, $sql);

    header("Location: viewBlog.php");

}

?>