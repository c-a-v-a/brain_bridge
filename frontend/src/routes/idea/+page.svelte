<script lang="ts">
	import { onMount } from 'svelte';
	import backgroundImage from '$lib/assets/dashboard-bg.png';
	import { createIdea, getFullIdea, getIdeas } from '$lib/api/ideasApi';
	import type { IdeaCreate, IdeaFull, IdeaGet } from '$lib/models/ideaModels';
  import { page } from '$app/state';
  import { refresh } from '$lib/api/tokenApi';
  import { goto } from '$app/navigation';

  const ideaId = page.url.searchParams.get('id');
  let idea: IdeaFull | null = {
    id: "1",
    title: "Tytuł",
    description: "opis opis opis",
    long_description: "bardzo długi opisggggg ggggggggggg ggggggggggggg gggg ggg gggggggggggg ggggggggggg ggggggggggggg  ggggggg gggggggg gggggggggg gggggggggggg gggg ggggggg ggggggggg gggggg ggggggg gggggg gggggg ggggggggg ggggggggggg gggggggggg ggggggggggggggggg gggggggg",
    links: [{ url: "https://google.com", text: "Google"}, { url: "https://duckduckgo.com", text: "Drugi link" }], 
    wanted_contributors: "Jakich ludzi porzebujemy",
    user_id: "1"
  };
  let errorMessage: string | null;
  let loading: boolean = true;

  onMount(async () => {
    loading = true;

    if (!ideaId) {
      errorMessage = "No idea ID.";
      loading = false;
      return;
    }

    if (Error.isError(await refresh())) {
      goto("/login");
    }

    const maybeIdea = await getFullIdea(ideaId);

    if (Error.isError(maybeIdea)) {
      errorMessage = maybeIdea.message;
    } else {
      idea = maybeIdea;
    }
    loading = false;
  });
</script>

<div class="relative h-screen w-screen overflow-hidden">
	<!-- Tło obrazkowe (bez zmian) -->
	<div
		class="absolute inset-[-10px] z-0 scale-110
            bg-cover bg-fixed bg-center
            blur-[40px]"
		style="background-image: url('{backgroundImage}')"
	></div>
	<!-- Główny kontener na treść i Modal (Centrowanie) -->
	<main
		class="relative z-10 flex flex-col h-screen w-screen items-center justify-center"
	>
    {#if idea}
    <div
      class="px-10 rounded-4xl min-w-1/3 bg-violet-800/30 p-3 text-center text-lg mb-5
                            font-bold text-white shadow-inner shadow-black/20"
    >
      {idea.title || 'Brak Tytułu'}
    </div>
    {/if}
		<!-- Kontener na wyświetlanie pomysłów (wyśrodkowany) -->
    <div class="flex flex-col w-full items-center justify-center">
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
          class="relative flex min-h-[600px] w-4/5 flex-col gap-5
                              rounded-4xl border border-white/20
                              bg-blue-800/40 p-8 backdrop-blur-sm shadow-2xl"
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
            <div
              class="grow overflow-y-auto text-base leading-relaxed flex flex-col"
            >
              {#each idea.links as link}
                <a class="text-blue-300 underline" href="{link.url}">{link.text}</a>
              {/each}
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
        </div>
      {/if}
    </div>
	</main>
</div>
