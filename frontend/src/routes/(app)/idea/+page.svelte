<script lang="ts">
	import { onMount } from 'svelte';
	import backgroundImage from '$lib/assets/dashboard-bg.png';
	import { createIdea, getFullIdea, getIdeas } from '$lib/api/ideasApi';
	import type { IdeaCreate, IdeaFull, IdeaGet } from '$lib/models/ideaModels';
	import { page } from '$app/state';
	import { refresh } from '$lib/api/tokenApi';
	import { goto } from '$app/navigation';
	import Modal from '$lib/components/Modal.svelte';

	const ideaId = page.url.searchParams.get('id');
	let idea: IdeaFull | null = null;
	let errorMessage: string | null;
	let loading: boolean = true;
	let comment: string = "";
	let comments: any[] = [];

	let showModal = false;
	let currentImageIndex = 0;

	function openModal(index: number) {
		currentImageIndex = index;
		showModal = true;
	}

	function closeModal() {
		showModal = false;
	}

	function nextImage() {
		if (idea && idea.images) {
			currentImageIndex = (currentImageIndex + 1) % idea.images.length;
		}
	}

	function prevImage() {
		if (idea && idea.images) {
			currentImageIndex = (currentImageIndex - 1 + idea.images.length) % idea.images.length;
		}
	}

	async function addComment() {
			const response = await fetch(`http://localhost:8000/api/comments`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({
					content: comment,
					idea_id: ideaId
				})
			});

			if (!response.ok) {
				const errorText = await response.text();
				const error: Error = new Error(`Błąd serwera (${response.status}): ${errorText}`);
				alert(`An error occurred: ${error.message}`);
			}

			comment = "";

			let res = await fetch(`http://localhost:8000/api/comments/${ideaId}`);
			comments = await res.json();
	}

	onMount(async () => {
		loading = true;

		if (!ideaId) {
			errorMessage = 'No idea ID.';
			loading = false;
			return;
		}

		if (Error.isError(await refresh())) {
			goto('/login');
		}

		const maybeIdea = await getFullIdea(ideaId);

		if (Error.isError(maybeIdea)) {
			errorMessage = maybeIdea.message;
		} else {
			idea = maybeIdea;
		}

		let res = await fetch(`http://localhost:8000/api/comments/${ideaId}`);
		comments = await res.json();

		loading = false;
		console.log(idea);
	});
</script>

<div class="relative min-h-screen w-full overflow-hidden">
	<!-- Tło obrazkowe (bez zmian) -->
	<div
		class="absolute inset-[-10px] z-0 scale-110
            bg-cover bg-fixed bg-center
            blur-[40px]"
		style="background-image: url('{backgroundImage}')"
	></div>
	<!-- Główny kontener na treść i Modal (Centrowanie) -->
	<div class="relative z-10 flex min-h-screen w-full flex-col items-center justify-center mt-103421">
		{#if idea}
			<div
				class="rounded-4xl min-w-1/3 mb-5 bg-violet-800/30 p-3 px-10 text-center text-lg
                            font-bold text-white shadow-inner shadow-black/20"
			>
				{idea.title || 'Brak Tytułu'}
			</div>
		{/if}
		<!-- Kontener na wyświetlanie pomysłów (wyśrodkowany) -->
		<div class="flex w-full flex-col items-center justify-start">
			{#if loading}
				<p class="rounded-lg bg-black/50 p-8 text-xl text-white backdrop-blur-sm">
					Ładowanie pomysłu...
				</p>
			{:else if errorMessage}
				<p class="rounded-lg bg-black/50 p-8 text-xl text-red-400 backdrop-blur-sm">
					Error: {errorMessage}
				</p>
			{:else if idea}
				<!-- Karta Pomysłu (UŻYWA WYMIARÓW I STYLÓW Z DESIGNU) -->
				<div
					class="rounded-4xl relative flex min-h-[600px] w-4/5 flex-col
                              gap-5 border border-white/20
                              bg-blue-800/40 p-8 shadow-2xl backdrop-blur-sm"
				>
					<!-- Frame 2: DESCRIPTION -->
					<div
						class="flex grow flex-col rounded-lg border border-white/10
          bg-violet-500/40 p-4 shadow-inner shadow-black/50"
					>
						<label class="mb-2 block text-sm text-white/70"> Short description: </label>
						<div
							class="grow overflow-y-auto text-base leading-relaxed
              text-white"
						>
							<p class="whitespace-pre-wrap">{idea.description || 'Brak opisu.'}</p>
						</div>
					</div>

					<div
						class="flex grow flex-col rounded-lg border border-white/10
          bg-violet-500/40 p-4 shadow-inner shadow-black/50"
					>
						<label class="mb-2 block text-sm text-white/70"> Links: </label>
						<div class="flex grow flex-col overflow-y-auto text-base leading-relaxed">
							{#each idea.links as link}
								<a class="text-blue-300 underline" href={link.url}>{link.text}</a>
							{/each}
						</div>
					</div>

					<div
						class="flex grow flex-col rounded-lg border border-white/10
          bg-violet-500/40 p-4 shadow-inner shadow-black/50"
					>
						<label class="mb-2 block text-sm text-white/70"> Images: </label>
						<div class="flex flex-wrap gap-4 overflow-y-auto p-2">
							{#if idea.images && idea.images.length > 0}
								{#each idea.images as image, index}
									<button
										class="relative h-24 w-24 overflow-hidden rounded-lg border border-white/20 shadow-md transition-transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-blue-400"
										on:click={() => openModal(index)}
									>
										<img
											src={`http://localhost:8000/api/${image}`}
											alt={`Idea image ${index + 1}`}
											class="h-full w-full object-cover"
										/>
									</button>
								{/each}
							{:else}
								<p class="text-white/50">No images available.</p>
							{/if}
						</div>
					</div>

					<div
						class="flex grow flex-col rounded-lg border border-white/10
          bg-violet-500/40 p-4 shadow-inner shadow-black/50"
					>
						<label class="mb-2 block text-sm text-white/70"> Long description: </label>
						<div
							class="grow overflow-y-auto text-base leading-relaxed
              text-white"
						>
							<p class="whitespace-pre-wrap">{idea.long_description || 'Brak opisu.'}</p>
						</div>
					</div>

					<div
						class="flex grow flex-col rounded-lg border border-white/10
          bg-violet-500/40 p-4 shadow-inner shadow-black/50"
					>
						<label class="mb-2 block text-sm text-white/70"> Wanted contributors: </label>
						<div
							class="grow overflow-y-auto text-base leading-relaxed
              text-white"
						>
							<p class="whitespace-pre-wrap">{idea.wanted_contributors || 'Brak opisu.'}</p>
						</div>
					</div>
					<div
						class="flex grow flex-col rounded-lg border border-white/10
          bg-violet-500/40 p-4 shadow-inner shadow-black/50"
					>
						<label class="mb-2 block text-sm text-white/70"> Comments: </label>
						<div
							class="grow overflow-y-auto text-base leading-relaxed
              text-white"
						>
							
						</div>
						<div
							class="grow overflow-y-auto text-base leading-relaxed text-white w-full flex flex-col justify-center"
						>
							{#each comments as com}
								<p>User: {com.content}</p>
							{/each}
							<input
								type="text"
								placeholder="Comment"
								bind:value={comment}
								class="flex-2 mt-5 rounded-lg border border-white/30
																	bg-white/15 p-2 text-white placeholder-white/70 outline-none
																	focus:border-white/50"
							/>
							<button
								on:click={addComment}
								class="rounded-lg bg-violet-900 px-2 py-2 text-white transition-colors hover:bg-violet-700"
							>
								Add comment
							</button>
						</div>
					</div>
				</div>
			{/if}
		</div>
	</div>
</div>

<Modal show={showModal} on:close={closeModal}>
	{#if idea && idea.images && idea.images.length > 0}
		<div
			class="flex items-center justify-center gap-4 p-4 outline-none"
			role="dialog"
			tabindex="-1"
		>
			{#if idea.images.length > 1}
				<!-- svelte-ignore a11y_consider_explicit_label -->
				<button
					class="shrink-0 rounded-full bg-white/10 p-3 text-white transition-colors hover:bg-white/20 focus:outline-none focus:ring-2 focus:ring-white/50"
					on:click|stopPropagation={prevImage}
				>
					<svg
						xmlns="http://www.w3.org/2000/svg"
						fill="none"
						viewBox="0 0 24 24"
						stroke-width="2"
						stroke="currentColor"
						class="h-4 w-4"
					>
						<path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
					</svg>
				</button>
			{/if}

			<img
				src={`http://localhost:8000/api/${idea.images[currentImageIndex]}`}
				alt={`Full size ${currentImageIndex + 1}`}
				class="max-h-[85vh] max-w-[70vw] rounded-lg object-contain shadow-2xl"
			/>

			{#if idea.images.length > 1}
				<!-- svelte-ignore a11y_consider_explicit_label -->
				<button
					class="shrink-0 rounded-full bg-white/10 p-3 text-white transition-colors hover:bg-white/20 focus:outline-none focus:ring-2 focus:ring-white/50"
					on:click|stopPropagation={nextImage}
				>
					<svg
						xmlns="http://www.w3.org/2000/svg"
						fill="none"
						viewBox="0 0 24 24"
						stroke-width="2"
						stroke="currentColor"
						class="h-4 w-4"
					>
						<path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
					</svg>
				</button>
			{/if}
		</div>
	{/if}
</Modal>
