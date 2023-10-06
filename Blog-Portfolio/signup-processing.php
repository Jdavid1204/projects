
<?php
    $servername = "127.0.0.1"; 
    $username = "root"; 
    $password = "root"; 
    $dbname = "ecs417"; 
    // Creates connection 
    $conn = new mysqli($servername, $username, $password, $dbname); 
    // Checks connection 
    if ($conn->connect_error) { die("Connection faileeddd: " . $conn->connect_error); } 
  // Checks connection 
  if ($conn->connect_error) { die("Connection faileeddd: " . $conn->connect_error); } 
  if ($_SERVER['REQUEST_METHOD'] == 'POST'){ 
    $fname = $_POST['fname'];
    $sname = $_POST['sname'];
    $email = $_POST['email'];
    $pass1 = $_POST['password'];
    $sql = "INSERT INTO USERS (firstName, lastName, email, password) VALUES ('$fname', '$sname', '$email', '$pass1')";
    if ($conn->query($sql) === TRUE) { 
        //YOUR CODE GOES HERE
            header("Location: index.php");
        } else { echo "Error: " . $sql . "<br>" . $conn->error; } 
        $conn->close(); 
}  
?>