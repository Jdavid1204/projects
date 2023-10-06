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

$sql = "SELECT * FROM COMMENTS";
$query = mysqli_query($conn, $sql); 


if (($_SERVER['REQUEST_METHOD'] == 'POST')){
    $comment = $_POST['comment'];
    $author = (string) $_SESSION['name'];
    $sql = "INSERT INTO COMMENTS (user, messages) VALUES ('$author', '$comment')";
    mysqli_query($conn, $sql);

    header("Location: viewBlog.php");

}

?>