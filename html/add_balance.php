<html>
  <head>
  	<meta charset="utf-8">
    <title>rabit</title>
    <link rel="stylesheet" href="css/bootstrap.css">
  </head>
  <body>
    <?php 
      if(!isset($_POST["amount"])){return;}

      $amount = $_POST["amount"];

      require("db.php");
      $db = new db("localhost", "rabit", "pass", "rapid_cart");
      $balance = $db->update_balance(1, -$amount);
    ?>


    <h1>カスタマーID:1</h1>
    <?php print("<h3>".$amount."￥入金完了しました</h3>");?>
    <hr>

    <?php
      print("<h3>所持金額".$balance."￥</h3>");
    ?>

    <a href="index.php" class="btn btn-primary">戻る</a>

    <script type="text/javascript" src="js/jquery-3.3.1.js"></script>
  	<script type="text/javascript" src="js/bootstrap.bundle.js"></script>
  </body>
</html>