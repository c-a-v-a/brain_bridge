<script lang="ts">
	import { onMount } from 'svelte';
	import backgroundImage from '$lib/assets/dashboard-bg.png';
	import { getIdeas } from '$lib/api/ideasApi';
	import type { IdeaGet } from '$lib/models/ideaModels';
	import { ideasStore } from '$lib/store/ideas';

	// === STATE VARIABLES FOR IDEAS ===
	let ideas: Array<IdeaGet> = []; // Full list of ideas
	let currentIdea: IdeaGet | null = null; // Currently displayed random idea (Tinder Card)
	let isLoading = true;
	let errorFetchingIdeas = '';

	const HARDCODED_USER_ID = '60c72b2f9e4f500001010101';

	// Picks a random idea from the ideas array and sets it as currentIdea
	function pickRandomIdea() {
		if (ideas.length > 0) {
			[currentIdea] = ideas.slice(-1);
			
			ideas = ideas.filter((x,i) => i !== ideas.length - 1);

			ideasStore.update(xs => [...xs, currentIdea as IdeaGet]);
		} else {
			currentIdea = null;
		}
	}

	function filterOutExisting(arr: IdeaGet[]): IdeaGet[] {
		let existing: IdeaGet[];
		ideasStore.subscribe(v => existing = v)();

		return arr.filter(x => !existing.some(e => e.id === x.id));
	}


	// Loading all ideas from API
	async function loadIdeas() {
		isLoading = true;
		errorFetchingIdeas = '';
		const result = await getIdeas();

		if (result instanceof Error) {
			console.error('Error loading ideas:', result);
			errorFetchingIdeas = result.message;
			ideas = [];
			currentIdea = null;
		} else {
			ideas = result;
			// To ensure you see something at the start, we add mock data
			// You will remove this when the server returns data.
			if (ideas.length === 0) {
				ideas = [
					{
						id: 'mock1',
						title: 'Spaceship Project',
						user_id: 'dev_user',
						description:
							'Description of a super secret project to create an intergalactic merchant ship with warp drive.'
					},
					{
						id: 'mock2',
						title: 'SvelteKit CMS',
						user_id: 'dev_user',
						description:
							'Lightweight and fast content management system built with SvelteKit and Tailwind CSS. Full API support.'
					}
				];
			}

			ideas = filterOutExisting(ideas);

			pickRandomIdea();
		}
		isLoading = false;
	}

	onMount(loadIdeas);

	function handleSwipe(action: string) {
		console.log(`Action: ${action} for idea ${currentIdea!.id}`);
		// In the future: send POST to server with action (like/dislike)

		// Display next random idea
		pickRandomIdea();
	}
</script>

<div class="relative h-screen w-screen overflow-hidden">
	<!-- Background image (unchanged) -->
	<div
		class="absolute inset-[-10px] z-0 scale-110
            bg-cover bg-fixed bg-center
            blur-[40px]"
		style="background-image: url('{backgroundImage}')"
	></div>

	<!-- NAVBAR (unchanged) -->
	<nav
		class="fixed left-0 right-0 top-0 z-20 flex
				h-[60px] items-center justify-end border-b
                border-white/10 bg-white/5 px-4 backdrop-blur-sm"
	>
		<a
			href="/add-idea"
			class="flex h-8 w-8 items-center justify-center rounded-full
                   bg-cyan-800 text-lg font-bold text-white
                   shadow-lg transition-transform hover:scale-110"
		>
			+
		</a>
	</nav>

	<!-- Sidebar (unchanged) -->
	<aside
		class="fixed bottom-0 left-0 top-0 z-10 w-20
				  border-r border-white/10 bg-white/5 backdrop-blur-sm"
	></aside>

	<!-- Main content container and Modal (Centering) -->
	<main
		class="relative z-10 flex h-screen w-screen items-center justify-center
				 pl-20 pt-[60px]"
	>
		<!-- === MAIN VIEW ("Tinder" Card) === -->

		<!-- Container for displaying ideas (centered) -->
		<div class="flex flex-col items-center justify-center">
			{#if isLoading}
				<p class="rounded-lg bg-black/50 p-8 text-xl text-white backdrop-blur-sm">
					Loading ideas...
				</p>
			{:else if errorFetchingIdeas}
				<p class="rounded-lg bg-black/50 p-8 text-xl text-red-400 backdrop-blur-sm">
					Error: {errorFetchingIdeas}
				</p>
			{:else if currentIdea}
				<!-- Idea Card (USES DIMENSIONS AND STYLES FROM DESIGN) -->
				<div
					class="rounded-4xl relative flex h-[600px] w-[500px] flex-col
                                gap-5 border border-white/20
                                bg-blue-800/40 p-8 shadow-2xl backdrop-blur-sm"
				>
					<!-- Frame 1: TITLE -->
					<div
						class="w-full rounded-lg bg-violet-800/30 p-3 text-center text-lg
                                    font-bold text-white shadow-inner shadow-black/20"
					>
						{currentIdea.title || 'No Title'}
					</div>

					<!-- Frame 2: DESCRIPTION -->
					<div
						class="flex grow flex-col rounded-lg border border-white/10
            bg-violet-500/40 p-4 shadow-inner shadow-black/50"
					>
						<label class="mb-2 block text-sm text-white/70"> Description: </label>
						<div
							class="grow overflow-y-auto text-base leading-relaxed
                text-white"
						>
							<p class="whitespace-pre-wrap">{currentIdea.description || 'No description.'}</p>
						</div>
					</div>

					<!-- Action Buttons (Like/Dislike) -->
					<div class="mt-4 flex shrink-0 justify-center gap-16">
						<!-- Dislike (X) - Fuchsia (Cancel) -->
						<button
							on:click={() => handleSwipe('dislike')}
							class="flex h-16 w-16 items-center justify-center
                                       rounded-full border-2
                                       border-fuchsia-600 bg-teal-950/90
                                       text-4xl font-bold leading-none text-fuchsia-600
                                       shadow-xl transition-all hover:scale-110 hover:bg-fuchsia-600 hover:text-white"
						>
							×
						</button>

						<!-- Like (✓) - Violet (Submit) -->
						<button
							on:click={() => handleSwipe('like')}
							class="flex h-16 w-16 items-center justify-center
                                       rounded-full border-2
                                       border-white/50 bg-violet-900/90
                                       text-4xl font-bold leading-none text-white
                                       shadow-xl transition-all hover:scale-110 hover:bg-white/80 hover:text-violet-900"
						>
							✓
						</button>
					</div>
				</div>
			{:else}
				<!-- No ideas -->
				<p class="rounded-lg bg-black/50 p-8 text-xl text-white backdrop-blur-sm">
					No ideas to display. Add the first one!
				</p>
			{/if}
		</div>
	</main>
</div>
