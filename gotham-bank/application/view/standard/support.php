<div class="support-form">
	<h1>Support</h1>
	<form action="/support" method="POST">
		<select name="theme">
			<option disabled>Choose theme</option>
			<option value="tech">Technical</option>
			<option value="simple">Simple</option>
		</select>
		<input type="textarea" name="message" placeholder="Your message">
		<input type="text" name="url" placeholder="URL">
		<input type="submit" value="Send">
	</form>	
</div>
<div class="history-block">
	<h3>Your history</h3>
	<?php if($messages): ?>
		<table class="table">
			<thead>
				<tr>
					<th scope="col">ID</th>
					<th scope="col">Theme</th>
					<th scope="col">Date</th>
					<th scope="col">Message</th>
					<th scope="col">URL</th>
					<th scope="col">View</th>
				</tr>
			</thead>
			<tbody>
				<?php foreach($messages as $message): ?>
				<tr>
					<th scope="row">
						<?php echo $message->id; ?>
					</th>
					<td>
						<i><?php echo $message->theme;?></i>
					</td>
					<td>
						<i><?php echo $message->date; ?></i>
					</td>
					<td>
						<i><?php echo $message->message; ?></i>
					</td>
					<td>
						<i><?php echo $message->url; ?>
					</td>
					<td>
						<iframe src="/support/iframe?url=<?php echo $message->url; ?>" width="500"></iframe>
					</td>
				</tr>
				<?php endforeach; ?>
			</tbody>
		</table>
	<?php else: ?>
		<h4><i>Empty :)</i></h4>
	<?php endif; ?>	
</div>

