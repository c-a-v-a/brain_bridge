<script lang="ts">
	import type { UserCreate, UserGet } from '$lib/models/user.models';
	const PUBLIC_API_URL = "http://localhost:5173"

	let newUser: UserCreate = {
		username: '',
		name: '',
		surname: '',
		email: '',
		password: '',
		is_admin: false
	};

	async function handleSubmit() {
		let error = null;

		try {
			const response = await fetch(`${PUBLIC_API_URL}/register`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(newUser)
			});

			if (response.ok) {
				const registeredUser: UserGet = await response.json();
				// console.log('Zarejestrowano użytkownika:', registeredUser);
				// goto('/login');
			} else {
				const errorData = await response.json();
				error = errorData.detail || `Server error: ${response.status}`;
			}
		} catch (e) {
			error = 'Couldnt connect to API.';
			console.error(e);
		}
	}
</script>

<div class="flex min-h-screen flex-col bg-gray-100 lg:flex-row">
	<div
		class="bg-linear-to-br flex w-full justify-center from-teal-700 via-violet-800
              to-teal-700 p-8 text-white lg:w-1/3"
	>
		<div class="absolute inset-0 z-0 backdrop-blur-3xl backdrop-filter"></div>
		<div class="relative z-10 max-w-md text-left lg:mt-20 lg:text-left">
			<h1 class="mb-4 text-4xl font-extrabold leading-tight opacity-90 lg:text-5xl">
				The bridge between ideas.
			</h1>
			<p class="text-2xl font-semibold opacity-80 lg:text-3xl">Brings people together.</p>
		</div>
	</div>

	<div class="lg:rounded-l-4xl z-10 flex w-full items-center justify-center bg-white p-8 lg:w-2/3">
		<div class="mb-40 w-full max-w-2xl">
			<h2 class="mb-20 text-center text-5xl font-bold text-gray-800 lg:text-left">
				Create an Account
			</h2>

			<form on:submit|preventDefault={handleSubmit} class="space-y-6">
				<div class="grid grid-cols-1 gap-6 md:grid-cols-2">
					<div>
						<label for="name" class="block text-sm font-medium text-gray-700">Name</label>
						<input
							type="text"
							id="name"
							name="name"
							bind:value={newUser.name}
							class="mt-1 block w-full rounded-lg border border-gray-300 px-4 py-3 shadow-sm
                     focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
							placeholder="Your name"
							required
						/>
					</div>
					<div>
						<label for="surename" class="block text-sm font-medium text-gray-700">Last name</label>
						<input
							type="text"
							id="surename"
							name="surename"
							bind:value={newUser.surname}
							class="mt-1 block w-full rounded-lg border border-gray-300 px-4 py-3 shadow-sm
                     focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
							placeholder="Your last name"
							required
						/>
					</div>
				</div>

				<div>
					<label for="username" class="block text-sm font-medium text-gray-700">Username</label>
					<input
						type="text"
						id="username"
						name="username"
						bind:value={newUser.username}
						class="mt-1 block w-full rounded-lg border border-gray-300 px-4 py-3 shadow-sm
                   focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
						placeholder="einstein9000"
						required
					/>
				</div>

				<div>
					<label for="email" class="block text-sm font-medium text-gray-700">Email</label>
					<input
						type="email"
						id="email"
						name="email"
						bind:value={newUser.email}
						class="mt-1 block w-full rounded-lg border border-gray-300 px-4 py-3 shadow-sm
                   focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
						placeholder="your.email@example.com"
						required
					/>
				</div>

				<div>
					<label for="password" class="block text-sm font-medium text-gray-700">Password</label>
					<input
						type="password"
						id="password"
						name="password"
						bind:value={newUser.password}
						class="mt-1 block w-full rounded-lg border border-gray-300 px-4 py-3 shadow-sm
                   focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
						placeholder="Minimum 8 characters"
						required
					/>
				</div>

				<div>
					<button
						type="submit"
						class="flex w-full justify-center rounded-lg border border-transparent bg-teal-950 px-4
                   py-3 text-lg font-medium text-white shadow-sm hover:bg-cyan-800
                   focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
					>
						Create an Account
					</button>
				</div>
			</form>

			<p class="mt-8 text-left text-sm text-gray-600">
				Do you already have an account?
				<a href="/login" class="font-medium text-indigo-600 hover:text-indigo-500"> Log in. </a>
			</p>
		</div>
	</div>
</div>
