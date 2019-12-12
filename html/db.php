<?php
	class db
	{
		function __construct($host, $user, $pw, $db){
			$this->host = $host;
			$this->user = $user;
			$this->pw = $pw;
			$this->db = $db;
		}

		private $host;
		private $user;
		private $pw;
		private $db;

		private function connect(){
			$con = mysqli_connect($this->host, $this->user, $this->pw, $this->db);
			if(mysqli_connect_errno()){
				prntf("Connect failed: %s\n", mysqli_connect_errno());
				exit();
			}
			return $con;
		}

		public function delete_cart_items($cart_id){
			$con = $this->connect();
			if($delete_cart_items_stmt = mysqli_prepare($con, "DELETE FROM cart WHERE cart_id = ?")){
				$delete_cart_items_stmt->bind_param("i", $cart_id);

				$delete_cart_items_stmt->execute();

				$delete_cart_items_stmt->close();
			}
		}

		private function get_jans($cart_id){
			$con = $this->connect();
			if($jans_stmt = mysqli_prepare($con, "SELECT jan FROM cart WHERE cart_id = ?")){
				$jans_stmt->bind_param("i", $cart_id);

				$jans_stmt->execute();
				$jans_stmt->bind_result($jan);
				
				$result = array();
				while($jans_stmt->fetch()){
					array_push($result, $jan);
				}
				
				$jans_stmt->close();				

				return $result;
			}
		}

		public function get_items_info($cart_id){
			$con = $this->connect();
			$jans = $this->get_jans($cart_id);

			$result = array();
			foreach($jans as $jan){
				if($item_stmt = mysqli_prepare($con, "SELECT title, price, image_url FROM item WHERE jan = ?")){
					$item_stmt->bind_param("i", $jan);

					$item_stmt->execute();

					$item_stmt->bind_result($title, $price, $image_url);

					$item_stmt->fetch();
					$items = array(
						"title" => $title,
						"price" => $price,
						"image_url" => $image_url);
					array_push($result, $items);
					$item_stmt->close();
				}
			}
			return $result;
		}


		public function get_balance($customer_id){
			$con = $this->connect();
			if($balance_stmt = mysqli_prepare($con, "SELECT balance FROM customer WHERE id = ?")){
				$balance_stmt->bind_param("i", $customer_id);

				$balance_stmt->execute();
				$balance_stmt->bind_result($balance);
				$balance_stmt->fetch();

				$balance_stmt->close();

				return $balance;
			}
		}

		public function update_balance($customer_id, $total){
			$con = $this->connect();
			$balance = $this->get_balance($customer_id);
			$remain = $balance - $total;

			if($remain < 0){return -1;}

			if($update_balance_stmt = mysqli_prepare($con, "UPDATE customer SET balance = ? WHERE id = ?")){
				$update_balance_stmt->bind_param("ii", $remain, $customer_id);
				$update_balance_stmt->execute();
				$update_balance_stmt->close();
			}

			$balance = $this->get_balance($customer_id);
			return $balance;	
		}
		

	}
?>