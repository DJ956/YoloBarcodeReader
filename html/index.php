<html>
  <head>
    <title>rabit</title>
  </head>
  <body>
    <p>hello</p>
    <?php
      require("db.php");

      $db = new db("localhost", "rapid", "pass", "rapid_cart");
      $result = $db->get_items_info(1);

      foreach($result as $row){
        print($row);
        print("<br>");
      }
    ?>
  </body>
</html>