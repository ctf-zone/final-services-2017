<div class="export-menu">
	<h1>Export menu</h1>

	Choose export format:

	<form action="/card2card/export" method="POST">
		<p>
			<input type="radio" name="export" value="CSV"> CSV
			<br>
			<input type="radio" name="export" value="XML"> XML
			<br>
			<input type="hidden" name="id" value="<?php echo $_SESSION['userdata']['id']; ?>">
		</p>
		<input type="submit" value="Export" >
	</form>
</div>