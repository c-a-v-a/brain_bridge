<script lang="ts">
	// proof of concept, messy code don't do this like that.
	// types and api calls should be separated. ideally we will have smaller sub-components that will make the messy state variables more clear
	interface IMessage {
		name: string;
		message: string;
	}

	let message: IMessage | undefined;
	let messageSend: IMessage = {
		name: '',
		message: ''
	};
	let errorMessage: string = '';
	let loading: boolean = false;
	let sendInfo: string = '';

	// those functions will be in lib
	const fetchMessage = async () => {
		try {
			loading = true;
			errorMessage = '';

			const response = await fetch('http://localhost:8000/api/message');
			if (response.status === 204) {
				throw new Error('No messages left on the stack');
			} else if (!response.ok) {
				throw new Error('Failed to fetch message');
			}

			message = await response.json();
		} catch (error) {
			errorMessage = (error as Error).message;
		} finally {
			loading = false;
		}
	};

	const sendMessage = async () => {
		if (messageSend.message.length === 0 || messageSend.name.length === 0) {
			sendInfo = 'Please fill out all inputs';
			return;
		}

		const response = await fetch('http://localhost:8000/api/message', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(messageSend)
		});

		if (!response.ok) {
			sendInfo = 'Could not send message';
		} else {
			sendInfo = 'Message sent';
		}
	};
</script>

<main>
	<h1>Get message</h1>
	<button
		on:click={fetchMessage}
		disabled={loading}
		class="rounded bg-blue-500 px-4 py-2 text-white hover:bg-blue-600"
	>
		{loading ? 'Loading...' : 'Get message'}
	</button>

	<div class="prose mt-4">
		{#if errorMessage.length > 0}
			<p class="text-red-500">{errorMessage}</p>
		{:else if message}
			<p>{message.name}: {message.message}</p>
		{/if}
	</div>

	<hr class="my-10" />

	<div class="max-w-sm p-4">
		<label for="username" class="block text-sm font-medium text-gray-700">Username</label>
		<input
			id="username"
			type="text"
			bind:value={messageSend.name}
			placeholder="Enter your username"
			class="mt-1 block w-full rounded-md border-gray-300 p-2 text-sm shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
		/>
		<label for="message" class="mt-10 block text-sm font-medium text-gray-700">Message</label>
		<input
			id="Message"
			type="text"
			bind:value={messageSend.message}
			placeholder="Enter your message"
			class="mt-1 block w-full rounded-md border-gray-300 p-2 text-sm shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
		/>
		<button
			on:click={sendMessage}
			class="mt-10 rounded bg-blue-500 px-4 py-2 text-white hover:bg-blue-600"
		>
			Send message
		</button>
	</div>
	<p>{sendInfo}</p>
</main>
