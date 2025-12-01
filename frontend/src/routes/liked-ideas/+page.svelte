<script lang="ts">
	import backgroundImage from '$lib/assets/dashboard-bg.png'; // Załóżmy, że masz ten obraz
	// Import potrzebnych typów, funkcji API i nawigacji
	import { getIdeas } from '$lib/api/ideasApi';
	import type { IdeaGet } from '$lib/models/ideaModels';
	import { onMount } from 'svelte';
	import { refresh } from '$lib/api/tokenApi';
	import { goto } from '$app/navigation'; // Fikcyjne dane do celów demonstracyjnych, zastąpione danymi z API
	let ideas: IdeaGet[] = [
		{ id: '1', author: 'Michał', title: 'AntCasino' },
		{ id: '2', author: 'Anna', title: 'AI Photo Editor' },
		{ id: '3', author: 'Piotr', title: 'Decentralized Chat' },
		{ id: '4', author: 'Karolina', title: 'Green Energy Monitor' },
		{ id: '5', author: 'Tomasz', title: 'Gamified Learning Platform' },
		{ id: '6', author: 'Ewa', title: 'Local Food Delivery' },
		{ id: '7', author: 'Rafał', title: 'Smart Home Security' },
		{ id: '8', author: 'Magda', title: 'Travel Planner AI' },
		{ id: '9', author: 'Krzysztof', title: 'Open Source CRM' }
	];

	let searchQuery: string = '';
	let errorMessage: string | null;
	let loading: boolean = true; // Logika ładowania danych, podobna do Twojego przykładu

	onMount(async () => {
		loading = true; // Opcjonalna weryfikacja tokenu
		// if (Error.isError(await refresh())) {
		//   goto("/login");
		// }
		// const maybeIdeas = await getIdeas(); // Odkomentuj, aby użyć prawdziwego API
		// if (Error.isError(maybeIdeas)) {
		//   errorMessage = maybeIdeas.message;
		// } else {
		//   ideas = maybeIdeas;
		// }

		loading = false;
	}); // Filtrowanie listy na podstawie zapytania

	$: filteredIdeas = ideas.filter(
		(idea) =>
			idea.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
			idea.author.toLowerCase().includes(searchQuery.toLowerCase())
	);
</script>

<div class="relative h-screen w-screen overflow-hidden">
	<div
		class="absolute inset-[-10px] z-0 scale-110
            bg-cover bg-fixed bg-center
            blur-[40px]"
		style="background-image: url('{backgroundImage}')"
	></div>
	<main class="relative z-10 flex flex-col h-screen w-screen items-center justify-center p-4">
		{#if loading}
			<p class="rounded-lg bg-black/50 p-8 text-xl text-white backdrop-blur-sm">
				Ładowanie pomysłów...
			</p>
		{:else if errorMessage}
			<p class="rounded-lg bg-black/50 p-8 text-xl text-red-400 backdrop-blur-sm">
				Błąd: {errorMessage}
			</p>
		{:else}
			<div
				class="w-full max-w-4xl max-h-[80vh] flex flex-col p-6 sm:p-10
                rounded-[40px]
                bg-blue-900/40 text-white backdrop-blur-sm
                shadow-2xl shadow-violet-900/50"
			>
				<div class="relative mb-8">
					<input
						type="text"
						bind:value={searchQuery}
						placeholder="Search..."
						class="w-full h-12 px-6 pr-12 rounded-full
                   bg-white/10 border border-white/20
                   placeholder-white/70 text-lg
                   focus:outline-none focus:ring-2 focus:ring-fuchsia-500
                   shadow-inner shadow-black/20"
					/> <span class="absolute right-4 top-1/2 -translate-y-1/2 text-white/70"> 🔍 </span>
				</div>
				<div class="grid grid-cols-12 gap-4 mb-3 px-4 text-sm font-semibold text-white/70">
					<div class="col-span-4">Author</div>
					<div class="col-span-8">Title</div>
				</div>
				<div class="flex flex-col gap-4 overflow-y-auto pr-2">
					{#each filteredIdeas as idea}
						<button
							class="grid grid-cols-12 gap-4 items-center h-12 px-4 rounded-xl
                    bg-violet-800/50 border border-white/10
                    shadow-inner shadow-black/20 text-white text-base text-left
                    transition-all duration-200 hover:bg-violet-700/60
                    focus:outline-none focus:ring-2 focus:ring-fuchsia-500"
							on:click={() => goto(`/idea?id=${idea.id}`)}
						>
							<div class="col-span-4 truncate">{idea.author}</div>
							<div class="col-span-8 truncate">{idea.title}</div>
						</button>
					{:else}
						<p class="text-center text-white/70 py-4">Brak pomysłów do wyświetlenia.</p>
					{/each}
				</div>
			</div>
		{/if}
	</main>
</div>
