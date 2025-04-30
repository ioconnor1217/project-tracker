<?php
require 'config.php';

function db_connect() {
    if (function_exists('mysqli_connect')) {
        $conn = mysqli_connect(DB_HOST, DB_USER, DB_PASS, DB_NAME);
        if (!$conn) {
            die("MySQLi connection failed: " . mysqli_connect_error());
        }
        return $conn;
    } elseif (function_exists('mysql_connect')) {
        $conn = mysql_connect(DB_HOST, DB_USER, DB_PASS);
        if (!$conn) {
            die("MySQL connection failed: " . mysql_error());
        }
        if (!mysql_select_db(DB_NAME, $conn)) {
            die("Database selection failed: " . mysql_error());
        }
        return $conn;
    } else {
        die("No supported MySQL extension available.");
    }
}

function search_username($username) {
    $conn = db_connect();

    if (function_exists('mysqli_connect') && is_object($conn) && get_class($conn) === 'mysqli') {
        $stmt = mysqli_prepare($conn, "SELECT LoginID, UserName, Password FROM Login WHERE UserName = ?");
        mysqli_stmt_bind_param($stmt, "s", $username);
        mysqli_stmt_execute($stmt);
        $result = mysqli_stmt_get_result($stmt);
        $row = mysqli_fetch_assoc($result);
        mysqli_stmt_close($stmt);
        mysqli_close($conn);
        return $row ? $row : null;
    } elseif (function_exists('mysql_connect')) {
        $escaped = mysql_real_escape_string($username, $conn);
        $sql = "SELECT LoginID, UserName, Password FROM Login WHERE UserName = '$escaped'";
        $result = mysql_query($sql, $conn);
        if (!$result) {
            die("Query failed: " . mysql_error($conn));
        }
        $row = mysql_fetch_assoc($result);
        mysql_close($conn);
        return $row ? $row : null;
    }

    return null;
}