<?php if(!empty($_SESSION['userdata'])): ?>
<div>
	<?php if(empty($_SESSION['userdata']['card_numbers'])): ?>
		<div class="main-page">
		<h1>Register your card!</h1>
			<form action="/index/cardRegister" method="POST" id="card-register">
				<input type="hidden" name="register" value="true">
				<input type="submit" value="Register card">
			</form>
		</div>
	<?php else: ?>
		<?php if(count($_SESSION['userdata']['card_numbers']) < 3): ?>
			<p>
				<form action="/index/cardRegister" method="POST" id="card-register">
					<input type="hidden" name="register" value="true">
					<input type="submit" id="card-register" value="Register another one">
				</form>
			</p>
		<?php endif; ?>
		<table class="table">
			<thead>
				<tr>
					<th scope="col">Register date</th>
					<th scope="col">Card number</th>
					<th scope="col">Balance</th>
				</tr>
			</thead>
			<tbody>
				<?php foreach($card_numbers as $card): ?>
					<tr>
						<th scope="row">
							<?php echo $card->created_date; ?>		
						</th>
						<td>
							<?php echo $card->card_number; ?>
						</td>
						<td>
							<?php echo $card->balance; ?>
						</td>
					</tr>
				<?php endforeach; ?>
			</tbody>
		</table>
	<?php endif; ?>
</div>
<?php endif; ?>