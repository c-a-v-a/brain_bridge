<script lang="ts">
	import backgroundImage from '$lib/assets/dashboard-bg.png';
	import { getIdeas, likedIdeas } from '$lib/api/idea';
	import type { IdeaGet } from '$lib/models/idea';
	import { onMount } from 'svelte';
	import { refresh, validate } from '$lib/api/token';
	import { goto } from '$app/navigation';
	import type { UserGet } from '$lib/models/user';

	let ideas: IdeaGet[] = [];
	let user: UserGet;
	let searchQuery: string = '';
	let errorMessage: string | null;
	let loading: boolean = true;

	onMount(async () => {
		loading = true;

		const maybeUser = await validate();

		if (Error.isError(maybeUser)) {
			goto('/login')
		} else {
			user = maybeUser;
		}

		if (Error.isError(await refresh())) {
		  goto("/login");
		}

		const maybeIdeas = await likedIdeas(user._id);
		if (Error.isError(maybeIdeas)) {
		  errorMessage = maybeIdeas.message;
		} else {
		  ideas = maybeIdeas;
		}

		loading = false;
	});

	$: filteredIdeas = ideas.filter(
		(idea) =>
			idea.title.toLowerCase().includes(searchQuery.toLowerCase())
	);
</script>

<div class="relative min-h-screen w-full overflow-hidden">
	<div
		class="absolute inset-[-10px] z-0 scale-110
            bg-cover bg-fixed bg-center
            blur-[40px]"
		style="background-image: url('{backgroundImage}')"
	></div>
	<main class="relative z-10 flex min-h-screen w-full items-start justify-center">
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
				class="w-full max-w-4xl max-h-[90vh] flex flex-col p-6 sm:p-10
                rounded-[40px] mt-15
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
							class="grid grid-cols-12 gap-4 items-center min-h-12 px-4 rounded-xl
                    bg-violet-800/50 border border-white/10
                    shadow-inner shadow-black/20 text-white text-base text-left
                    transition-all duration-200 hover:bg-violet-700/60
                    focus:outline-none focus:ring-2 focus:ring-fuchsia-500"
							on:click={() => goto(`/idea?id=${idea._id}`)}
						>
							<div class="col-span-4 truncate">{idea.author ?? "Author"}</div>
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