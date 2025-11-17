<script lang="ts">
	import { onMount } from 'svelte';
	import backgroundImage from '$lib/assets/dashboard-bg.png';
	import { createIdea, getIdeas } from '$lib/api/ideasApi';
	import type { IdeaCreate, IdeaGet } from '$lib/models/ideaModels';

	// === ZMIENNE STANU DLA MODALA ===
	let isModalOpen = false;
	let title = '';
	let description = '';

	// === ZMIENNE STANU DLA POMYSŁÓW ===
	let ideas: Array<IdeaGet> = []; // Pełna lista pomysłów
	let currentIdea: IdeaGet | null = null; // Aktualnie wyświetlany losowy pomysł (Tinder Card)
	let isLoading = true;
	let errorFetchingIdeas = '';

	const HARDCODED_USER_ID = '60c72b2f9e4f500001010101';

	// === FUNKCJE ZARZĄDZANIA WIDOKAMI ===

	function toggleModal() {
		isModalOpen = !isModalOpen;
		if (!isModalOpen) {
			title = '';
			description = '';
		}
	}

	// Wybiera losowy pomysł z tablicy ideas i ustawia go jako currentIdea
	function pickRandomIdea() {
		if (ideas.length > 0) {
			const randomIndex = Math.floor(Math.random() * ideas.length);
			currentIdea = ideas[randomIndex];
		} else {
			currentIdea = null;
		}
	}

	// Ładowanie wszystkich pomysłów z API
	async function loadIdeas() {
		isLoading = true;
		errorFetchingIdeas = '';
		const result = await getIdeas();

		if (result instanceof Error) {
			console.error('Błąd ładowania pomysłów:', result);
			errorFetchingIdeas = result.message;
			ideas = [];
			currentIdea = null;
		} else {
			ideas = result;
			// Aby upewnić się, że widzisz coś na początku, dodajemy mock data
			// To usuniesz, gdy serwer będzie zwracał dane.
			if (ideas.length === 0) {
				ideas = [
					{
						id: 'mock1',
						title: 'Projekt Kosmiczny Statek',
						user_id: 'dev_user',
						desc: 'Opis super tajnego projektu tworzenia międzygalaktycznego statku handlowego z napędem warp.'
					},
					{
						id: 'mock2',
						title: 'SvelteKit CMS',
						user_id: 'dev_user',
						desc: 'Lekki i szybki system zarządzania treścią zbudowany w oparciu o SvelteKit i Tailwind CSS. Pełna obsługa API.'
					}
				];
			}
			pickRandomIdea();
		}
		isLoading = false;
	}

	onMount(loadIdeas);

	// === FUNKCJA WYSYŁANIA FORMULARZA ===
	async function handleSubmit() {
		if (!title.trim() || !description.trim()) {
			// Zamień alert() na element UI w rzeczywistej aplikacji
			alert('Tytuł i opis nie mogą być puste.');
			return;
		}

		const ideaData: IdeaCreate = {
			title: title,
			user_id: HARDCODED_USER_ID,
			desc: description
		};

		const result = await createIdea(ideaData);

		if (result instanceof Error) {
			console.error('Błąd podczas tworzenia pomysłu:', result);
			alert(`Wystąpił błąd: ${result.message}`);
		} else {
			console.log('Pomysł pomyślnie wysłany:', result);

			// Przeładuj listę i zamknij
			await loadIdeas();

			isModalOpen = false;
			title = '';
			description = '';
		}
	}

	function handleSwipe(action: string) {
		console.log(`Akcja: ${action} dla pomysłu ${currentIdea!.id}`);
		// W przyszłości: wysłanie POST do serwera z akcją (like/dislike)

		// Wyświetl następny losowy pomysł
		pickRandomIdea();
	}
</script>

<div class="relative h-screen w-screen overflow-hidden">
	<!-- Tło obrazkowe (bez zmian) -->
	<div
		class="absolute inset-[-10px] z-0 scale-110
            bg-cover bg-fixed bg-center
            blur-[40px]"
		style="background-image: url('{backgroundImage}')"
	></div>

	<!-- NAVBAR (bez zmian) -->
	<nav
		class="fixed left-0 right-0 top-0 z-20 flex
				h-[60px] items-center justify-end border-b
                border-white/10 bg-white/5 px-4 backdrop-blur-sm"
	>
		<button
			on:click={toggleModal}
			class="flex h-8 w-8 items-center justify-center rounded-full
                   bg-cyan-800 text-lg font-bold text-white
                   shadow-lg transition-transform hover:scale-110"
		>
			+
		</button>
	</nav>

	<!-- Sidebar (bez zmian) -->
	<aside
		class="fixed bottom-0 left-0 top-0 z-10 w-20
				  border-r border-white/10 bg-white/5 backdrop-blur-sm"
	></aside>

	<!-- Główny kontener na treść i Modal (Centrowanie) -->
	<main
		class="relative z-10 flex h-screen w-screen items-center justify-center
				 pl-20 pt-[60px]"
	>
		<!-- === WIDOK GŁÓWNY (Karta "Tinder") === -->

		<!-- Kontener na wyświetlanie pomysłów (wyśrodkowany) -->
		{#if !isModalOpen}
			<div class="flex flex-col items-center justify-center">
				{#if isLoading}
					<p class="rounded-lg bg-black/50 p-8 text-xl text-white backdrop-blur-sm">
						Ładowanie pomysłów...
					</p>
				{:else if errorFetchingIdeas}
					<p class="rounded-lg bg-black/50 p-8 text-xl text-red-400 backdrop-blur-sm">
						Błąd: {errorFetchingIdeas}
					</p>
				{:else if currentIdea}
					<!-- Karta Pomysłu (UŻYWA WYMIARÓW I STYLÓW Z DESIGNU) -->
					<div
						class="relative flex h-[600px] w-[500px] flex-col gap-5
                                rounded-4xl border border-white/20
                                bg-blue-800/40 p-8 backdrop-blur-sm shadow-2xl"
					>
						<!-- Frame 1: TITLE -->
						<div
							class="w-full rounded-lg bg-violet-800/30 p-3 text-center text-lg
                                    font-bold text-white shadow-inner shadow-black/20"
						>
							{currentIdea.title || 'Brak Tytułu'}
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
								<p class="whitespace-pre-wrap">{currentIdea.desc || 'Brak opisu.'}</p>
							</div>
						</div>

						<!-- Przyciski Akcji (Like/Dislike) -->
						<div class="mt-4 flex shrink-0 justify-center gap-16">
							<!-- Dislike (X) - Fuksja (Cancel) -->
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

							<!-- Like (✓) - Fiolet (Submit) -->
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
					<!-- Brak pomysłów -->
					<p class="rounded-lg bg-black/50 p-8 text-xl text-white backdrop-blur-sm">
						Brak pomysłów do wyświetlenia. Dodaj pierwszy!
					</p>
				{/if}
			</div>
		{/if}

		<!-- === MODAL (Dodawanie Pomysłu - ten sam, co wcześniej) === -->
		{#if isModalOpen}
			<form
				on:submit|preventDefault={handleSubmit}
				class="project-card relative flex
                        h-[70vh] w-1/3 min-w-[300px] max-w-[500px]
                        flex-col gap-5 rounded-2xl border
                        border-white/20 bg-violet-900/40 p-6
                        shadow-2xl backdrop-blur-xl"
			>
				<!-- IKONA ZAMKNIĘCIA -->
				<button
					on:click={toggleModal}
					type="button"
					class="absolute right-4 top-4 rounded-full
                           bg-transparent p-2 text-xl font-bold
                           text-fuchsia-600 transition-colors hover:bg-white/10"
				>
					×
				</button>

				<!-- Pole Title -->
				<input
					type="text"
					placeholder="Title"
					required
					bind:value={title}
					maxlength="200"
					class="w-full flex-shrink-0 rounded-lg border border-white/30
                        bg-white/15 p-3 text-center text-lg font-bold
                        text-white placeholder-white/70 outline-none
                        focus:border-white/50"
				/>

				<!-- Kontener na textareę -->
				<div
					class="flex min-h-0 flex-grow flex-col rounded-lg
                            border border-white/10 bg-teal-950/40 p-3"
				>
					<label for="description" class="mb-2 block flex-shrink-0 text-sm text-white/70">
						Description
					</label>
					<textarea
						id="description"
						required
						bind:value={description}
						class="h-full w-full flex-grow
                            resize-none overflow-y-auto border-none
                            bg-transparent text-white outline-none"
					>
					</textarea>
				</div>

				<!-- Kontener na przyciski -->
				<div class="mt-3 flex flex-shrink-0 justify-end gap-3">
					<!-- Przycisk Anuluj (Cancel) -->
					<button
						on:click={toggleModal}
						type="button"
						class="rounded-lg border-2 border-fuchsia-600
                               bg-teal-950 px-5 py-2
                               font-bold text-fuchsia-600
                               transition-colors hover:bg-fuchsia-600 hover:text-white"
					>
						Cancel
					</button>

					<!-- Przycisk Potwierdź (Submit) -->
					<button
						type="submit"
						class="rounded-lg bg-violet-900 px-5
                               py-2
                               font-bold text-white
                               transition-colors hover:bg-violet-700"
					>
						Submit
					</button>
				</div>
			</form>
		{/if}
	</main>
</div>
