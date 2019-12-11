<html>
  <head>
  	<meta charset="utf-8">
    <title>rabit</title>
    <link rel="stylesheet" href="css/bootstrap.css">
  </head>
  <body>
    <center>

    <?php
        require("db.php");
        if(!isset($_GET["cart_id"])){ return; }
        if(!isset($_GET["sum"])){ return;}
        $cart_id = $_GET["cart_id"];
        $sum = $_GET["sum"];

        $db = new db("localhost", "rabit", "pass", "rapid_cart");
        $balance = $db->update_balance(1, $sum);
        if($balance < 0){
          print("<h1>残高が不足しています</h1>");
          print("<a href='index.php' class='btn btn-danger'>戻る</a>");
          return;
        }

        $db->delete_cart_items($cart_id);

        print("<h2>カート番号".$cart_id."</h2>");
        print("<h3>お支払金額".$sum."￥</h3>");
        print("<h3>残高".$balance."￥</h3>");
    ?>
    <a href="index.php" class="btn btn-primary">戻る</a>
  </center>
    <script type="text/javascript" src="js/jquery-3.3.1.js"></script>
  	<script type="text/javascript" src="js/bootstrap.bundle.js"></script>
  </body>
</html>