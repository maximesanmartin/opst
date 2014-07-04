<?php
	include ('config.php');
	$req = mysql_query("select * from ressource");
	while($res= mysql_fetch_array($req)){
		$req2 = mysql_query('select * from tag');
		while($tag = mysql_fetch_array($req2)){
			mysql_query('insert into ressource_tags(ressource_id, tag_id) select ressource.id, tag.id from ressource, tag where ressource.id = ' . $res['id'] . ' and tag.id = ' . $tag['id'] . ' and ressource.titre like "%' . $tag['nom'] . '%" ');	
		}
	}
	echo "migration effectuée";
?>