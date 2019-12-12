<html>
  <head>
  	<meta charset="utf-8">
    <title>rabit</title>
    <link rel="stylesheet" href="css/bootstrap.css">
  </head>
  <body>
    <?php 
      require("db.php");
      $db = new db("localhost", "rabit", "pass", "rapid_cart");
      $balance = $db->get_balance(1);
    ?>


    <h1>カスタマーID:1</h1>
    <hr>
    <?php
      print("<h3>所持金額".$balance."￥</h3>");
    ?>

    <form action="add_balance.php" method="post">
      入金金額: <input type="number" name="amount" value=0> ￥
      <br>
      <input class="btn btn-primary" type="submit" value="チャージ">
    </form>
    
    <script type="text/javascript" src="js/jquery-3.3.1.js"></script>
  	<script type="text/javascript" src="js/bootstrap.bundle.js"></script>
  </body>
</html>