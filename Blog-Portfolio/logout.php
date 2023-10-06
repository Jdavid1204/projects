
<!-- Logging out by unsetting all global session variables -->
<!-- And destroying the session--> -->
<?php

    session_start();
    session_unset();
    session_destroy();
    
    header("Location: index.php");
    exit();
?>