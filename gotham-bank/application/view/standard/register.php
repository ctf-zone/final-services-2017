<div class="register-form">
	<?php if(isset($error)): ?>
		<p style="color:red">
			<?php echo $error; ?>
		</p>
	<?php endif;?>
	<form action="/register" method="POST">
		<div>
			Username: <input type="text" name="username">
		</div>
		<br>
		<div>
			Password: <input type="password" name="password">
		</div>
		<div>
			<input type="submit" class="form-button" value="Register">
		</div>
	</form>
</div>

