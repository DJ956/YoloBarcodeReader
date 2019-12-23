<html>
  <head>
  	<meta charset="utf-8">
    <title>カート内</title>
    <link rel="stylesheet" href="css/bootstrap.css">
  </head>
  <body>
    <?php
      require("db.php");
      if(!isset($_GET["cart_id"])){return;}

      $cart_id = $_GET["cart_id"];
      print("<h2>カート".$cart_id."の中身</h2>");

      $db = new db("localhost", "rapit", "pass", "rapit_cart");
      $result = $db->get_items_info($cart_id);

      $sum = 0;
      foreach ($result as $row) {
          $sum += (int)$row["price"];
      }
      print("<h4>合計金額".$sum."￥</h4>");

      print("<a href='payment.php?cart_id=".$cart_id."&sum=".$sum."' class='btn btn-success'>決算</a>");
    ?>

    <a href="index.php" class="btn btn-primary">戻る</a>
    <hr>

    <table border="1" align="center">
      <tr>
        <th>商品名</th> <th>価格</th> <th>商品画像</th>
      </tr>

    <?php
      foreach($result as $row){
        print("<tr>");
        print("<td>".$row["title"]."</td>");
        print("<td>".$row["price"]."￥</td>");
        $img_raw = file_get_contents($row["image_url"]);
        $img_raw = "data:image/jpg;base64,".base64_encode($img_raw);
        print("<td><img src='".$img_raw."''></td>");
        print("</tr>");
      }
    ?>


    <script type="text/javascript" src="js/jquery-3.3.1.js"></script>
  	<script type="text/javascript" src="js/bootstrap.bundle.js"></script>
  </body>
</html>