<!DOCTYPE html>
<html>
<head>
	<title>TheWholeBank</title>
	<script src="/js/jquery-3.2.1.min.js"></script>
	<script type="text/javascript" src="/js/script.js"></script>
	<link rel="stylesheet" href="/css/bootstrap.css">
	<link rel="stylesheet" href="/css/main.css">
</head>
<body>
	<nav class="navbar navbar-expand-lg navbar-dark bg-primary" style="justify-content: center;flex-direction: column;">
		<button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarColor01" aria-controls="navbarColor01" aria-expanded="false" aria-label="Toggle navigation">
			<span class="navbar-toggler-icon"></span>
		</button>

		<div class="collapse navbar-collapse" id="navbarColor01">
			<ul class="navbar-nav mr-auto">
				<?php if(empty($_SESSION['userdata'])): ?>
					<li class="nav-item active">
						<a class="nav-link" href="/">Home</a>
					</li>
					<li class="nav-item">
						<a class="nav-link" href="/about">About</a>
					</li>
					<li class="nav-item">
						<a class="nav-link" href="/login">Login</a>
					</li>
					<li class="nav-item">
						<a class="nav-link" href="/register">Register</a>
					</li>
				<?php else: ?>
					<li class="nav-item active">
						<a class="nav-link" href="/">Home</a>
					</li>
					<li class="nav-item">
						<a class="nav-link" href="/about">About</a>
					</li>
					<li class="nav-item">
						<a class="nav-link" href="/card2card">Transactions</a>
					</li>
					<li class="nav-item">
						<a class="nav-link" href="/support">Support</a>
					</li>
					<li class="nav-item">
						<a class="nav-link" href="/settings">Settings</a>
					</li>
					<li class="nav-item">
						<a class="nav-link" href="/logout">Logout</a>
					</li>
				<?php endif; ?>
			</ul>
		</div>
	</nav>

	