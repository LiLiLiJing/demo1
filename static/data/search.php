<?php
header("Content-Type:text/plain;charset:UTF-8");
@$content=$_REQUEST['content'] or die("content required");
$conn=mysqli_connect("172.18.77.15","root","weiguang123","knowgraph","3306");
var_dump($conn);
$sql="SET NAMES LATIN1";
mysqli_query($conn,$sql);
$sql="SELECT Entity FROM know_graph WHERE Entity LIKE '%$content%'";
$r=mysqli_query($conn,$sql);
if(!$r){
   echo "err";
}else{
    $rows=mysqli_fetch_all($r,1);
	var_dump($rows);
};
for($i=0;$i<count($rows);$i++){
	echo $rows[$i]['Entity']."@";
};
?>