<script lang="ts">
	import { goto } from '$app/navigation';
	import { onMount } from "svelte";
	import { refresh } from "$lib/api/token";
	import { login } from "$lib/api/user";
	import type { TokenPair } from "$lib/models/token";
	import type { UserLogin } from "$lib/models/user";


	let user: UserLogin = {
		email: '',
		password: ''
	};

	async function handleSubmit() {
		const result: TokenPair | Error = await login(user);

		if (Error.isError(result)) {
			console.log(result.message);
		} else {
			console.log("Authenticated");
			await goto('/');
		}
	}

	onMount(async () => {
		if (!Error.isError(await refresh())) {
			goto('/');
		}
	});
</script>

<div class="flex min-h-screen flex-col bg-gray-100 lg:flex-row">
	<div
		class="bg-linear-to-br flex w-full justify-center from-teal-700 via-violet-800
              to-teal-700 p-8 text-white lg:w-1/3"
	>
		<div class="absolute inset-0 z-0 backdrop-blur-3xl backdrop-filter"></div>
		<div class="relative z-10 max-w-md text-left lg:mt-20 lg:text-left">
			<h1 class="mb-4 text-4xl font-extrabold leading-tight opacity-90 lg:text-5xl">
				BrainBridge
			</h1>
			<p class="text-2xl font-semibold opacity-80 lg:text-3xl">The bridge between ideas. Brings people together.</p>
		</div>
	</div>

	<div class="lg:rounded-l-4xl z-10 flex w-full items-center justify-center bg-white p-8 lg:w-2/3">
		<div class="mb-52 w-full max-w-2xl">
			<h2 class="mb-20 text-center text-5xl font-bold text-gray-800 lg:text-left">Log in</h2>

			<form on:submit|preventDefault={handleSubmit} class="space-y-6">
				<div>
					<label for="username" class="block text-sm font-medium text-gray-700">Email</label>
					<input
						type="text"
						id="username"
						name="username"
						bind:value={user.email}
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
						bind:value={user.password}
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
						Log in
					</button>
				</div>
			</form>

			<p class="mt-8 text-left text-sm text-gray-600">
				Don't have an account yet?
				<a href="/register" class="font-medium text-indigo-600 hover:text-indigo-500"> Sign up </a>
			</p>
		</div>
	</div>
</div>
