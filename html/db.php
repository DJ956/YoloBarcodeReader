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

		public function delete(){

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
				if($item_stmt = mysqli_prepare($con, "SELECT title FROM item WHERE jan = ?")){
					$item_stmt->bind_param("i", $jan);

					$item_stmt->execute();

					$item_stmt->bind_result($item);

					$item_stmt->fetch();
					
					array_push($result, $item);
					$item_stmt->close();
				}
			}
			return $result;
		}

	}
?>