<div class='card2card-form'>
	<h1>Transaction</h1>
	<?php if(isset($error)): ?>
		<p style='color:red'>
			<?php echo htmlspecialchars($error); ?>
		</p>
	<?php endif;?>
	<form action='/card2card/prepare' method='POST'>
		<select name='from_card'>
			<option value='' selected disabled hidden>Pick a card</option>
			<?php foreach ($cards as $card): ?>
				<?php echo '<option value=',$card,'>',$card,'</option>'; ?>
			<?php endforeach; ?>
		</select>
		
		<input type='text' name='to_card' placeholder='To card'>
		<input type='text' name='amount' placeholder='Amount'>
		<input type='submit' value='Prepare transaction'>
	</form>
</div>

<h3>Transaction history | <a href='/card2card/export'>Export</a></h3>
<?php if(!empty($history)): ?>
	<table class='table'>
		<thead>
			<tr>
				<th scope='col'>ID</th>
				<th scope='col'>Date</th>
				<th scope='col'>From</th>
				<th scope='col'>To</th>
				<th scope='col'>Amount</th>
				<th scope='col'>Message</th>
			</tr>
		</thead>
		<tbody>
		<?php foreach($history as $fields): ?>
			<tr id="<?php echo 'transaction_',$fields['id']; ?>">
				<th scope='row'>
					<i id="<?php echo 'transactionId_',$fields['id'] ?>">
						<?php echo $fields['id']; ?>
					</i>
				</th>
				<td>
					<i><?php echo $fields['date']; ?></i>
				</td>
				<td>
					<i><?php echo $fields['from_card'],' (',$fields['from_card_username'],')'; ?></i>
				</td>
				<td>
					<i><?php echo $fields['to_card'],' (',$fields['to_card_username'],')'; ?></i>
				</td>
				<td>
					<i><?php echo $fields['count'];?>$</i>
				</td>
				<td>
					<input 
						type='text'
						id="<?php echo 'transactionMessage_',$fields['id']; ?>"
						value='<?php echo $fields['message']; ?>'
					>
				</td>
			</tr>
		<?php endforeach; ?>
		</tbody>
	</table>
<?php else: ?>
	<h4>Transaction history is empty :)</h4>
<?php endif; ?>
