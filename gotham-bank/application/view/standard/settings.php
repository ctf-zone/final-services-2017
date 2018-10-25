<div class="settings-form">
	<h1>Settings</h1>
	<?php if(!empty($error)):?>
		<i style="color: red;"><?php echo $error; ?></i>
	<?php endif; ?>
	<form action="/settings" method="POST">
		<input type="text" placeholder="First name" name="fname" value="<?php echo htmlspecialchars($fname); ?>">
		<input type="text" placeholder="Second name" name="sname" value="<?php echo htmlspecialchars($sname); ?>">
		<input type="submit" value="Save">
	</form>
</div>