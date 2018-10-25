<div class='payment_info' name='payment_info'>
	<?php if(isset($error)): ?>
		<p style='color:red'>
	<?php echo $error; ?>
		</p>
	<?php endif;?>
	<table style='width:40%'>
		<form action='/card2card/submit' method='POST'>
			<?php if($userdata): ?>
				<tr>
					<td>First name</td>
					<td>
						<input type='text' name='first_name' value='<?php echo htmlspecialchars($userdata->first_name); ?>' disabled>
					</td> 
				</tr>
				<tr>
					<td>Second name</td>
					<td>
						<input type='text' name='second_name' value='<?php echo htmlspecialchars($userdata->second_name); ?>' disabled>
					</td> 
				</tr>
			<?php endif; ?>
			<tr>
				<td>Source card</td>
				<td>
					<input type='text' name='from_card' value='<?php echo htmlspecialchars($payment_info['from_card']); ?>' readonly>
				</td> 
			</tr>
			<tr>
				<td>Destination card</td>
				<td>
					<input type='text' name='to_card' value='<?php echo htmlspecialchars($payment_info['to_card']); ?>' readonly>
				</td> 
			</tr>
			<tr>
				<td>Amount</td>
				<td>
					<input type='text' name='amount' value='<?php echo htmlspecialchars($payment_info['amount']); ?>' readonly>
				</td> 
			</tr>
			<tr>
				<td>Message</td>
				<td>
					<input type='text' name='message'>
				</td> 
			</tr>
			<tr>
				<td>
					<input type='submit' value='Submit Transaction'>
				</td>
			</tr>
		</form>
	</table>
	<br><br>
</div>