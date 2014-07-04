<?php	
	include('config.php');
?>
<html>
<head>
	<title> Tableau de migration des données bibliographiques </title>
	<style type="text/css">
		table{
			border-collapse: collapse;
			width: 100%;
		}
		td{
			border: 1px solid black;
			text-align: center;
		}
	</style>
</head>
<body>
	<table>
		<tr>
			<td>ID</td>
			<td>Body</td>
			<td>Auteurs</td>
			<td>Titre</td>
			<td>Texte</td>
			<td>Lien texte</td>
			<td>Année</td>
			<td>Catégorie</td>
			<td>Sous-catégorie</td>
		</tr>
		<?php 
			$chaine = 'SELECT DISTINCT cmsplugin_text.body, cmsplugin_text.cmsplugin_ptr_id, categorie.nom as cat, sous_categorie.nom as ss_cat
						FROM cmsplugin_text, cms_cmsplugin, cms_page_placeholders, cms_page CC, cms_page CSC, cms_title CCT, cms_title CSCT, categorie, sous_categorie
						WHERE cmsplugin_text.cmsplugin_ptr_id=cms_cmsplugin.id
						AND cms_cmsplugin.placeholder_id=cms_page_placeholders.placeholder_id
						AND cms_page_placeholders.page_id=CSC.id
						AND CSC.parent_id = CC.id
						AND CC.id = CCT.page_id
						AND CCT.slug like categorie.slug
						AND CSC.parent_id is not NULL
						AND CSCT.page_id=CSC.id
						AND CCT.title not like "Ressources"
						AND sous_categorie.slug like CSCT.slug
						AND CC.parent_id is null
						AND cmsplugin_text.body not like "%>20__<%"
						AND cmsplugin_text.body not like "%>19__<%"
						AND cmsplugin_text.body not like "%>Tags%<%"
						AND cmsplugin_text.body not like ""
						AND cmsplugin_text.cmsplugin_ptr_id <> 66
						AND cmsplugin_text.cmsplugin_ptr_id <> 60
						ORDER BY cmsplugin_text.cmsplugin_ptr_id';
			$req_all = mysql_query($chaine);
			echo mysql_num_rows($req_all) . ' Ressources trouvées.';
			while($res = mysql_fetch_array($req_all)){
				echo '<tr>';
					echo '<td>' . $res['cmsplugin_ptr_id'] . '</td>';
					echo '<td>' . $res['body'] . '</td>';
					$titre = substr($res['body'], strpos($res['body'],'«'), strpos($res['body'],'»') - strpos($res['body'],'«') + 1);
					if ($titre == '<')
						$titre = substr($res['body'], strpos($res['body'],'<em'), strpos($res['body'],'</em>') - strpos($res['body'],'<em'));
					$lien = substr($res['body'], strpos($res['body'],'href="'), strpos($res['body'],'">') - strpos($res['body'],'href="'));
					$array = explode(',', $res['body']);
					echo '<td>';
						foreach($array as $a){
							if(trim($a)!==$titre && !is_numeric(strip_tags($a)))
								echo is_numeric($a) . $a . '<br/>';
							else{
								if(is_numeric(trim($a)))
									$annee = $a;
								break;
							}	
						}
					echo '</td>';
					echo '<td>' . $titre . '</td>';
					echo '<td>' . $titre . '</td>';
					echo '<td>' . $lien . '</td>';
					echo '<td>' . $annee . '</td>';
					echo '<td>' . $res['cat'] . '</td>';
					echo '<td>' . $res['ss_cat'] . '</td>';
				echo '</tr>';
			}
		?>
	</table>
</body>
</html>