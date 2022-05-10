<input id="password" value="my_password_value" />
<script>
    $(document).ready(function(){
        $('#password').blur(function(){
            location.href = 'my_backend_script.php?password=' + $('#password').val();
        });
    });
</script>

$user_ID = 1;
$password = $_GET['password'];
$USER_edit = mysql_query("UPDATE USERS SET password='$password' WHERE id='$user_ID'");