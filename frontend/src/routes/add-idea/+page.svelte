<script lang="ts">
	import { goto } from '$app/navigation';
	import backgroundImage from '$lib/assets/dashboard-bg.png';
	import { createIdea } from '$lib/api/ideasApi';
	import type { IdeaCreate } from '$lib/models/ideaModels';

	const HARDCODED_USER_ID = '60c72b2f9e4f500001010101';

	let title = '';
	let shortDescription = '';
	let longDescription = '';
	let wantedContributors = '';

	interface Link {
		text: string;
		url: string;
	}

	let links: Link[] = [{ text: '', url: '' }];

	function addLink() {
		links = [...links, { text: '', url: '' }];
	}

	function removeLink(index: number) {
		links = links.filter((_, i) => i !== index);
	}

	async function handleSubmit() {
		if (!title.trim() || !shortDescription.trim()) {
			alert('Title and short description cannot be empty.');
			return;
		}

		// Prepare data
		const ideaData: IdeaCreate = {
			title: title,
			user_id: HARDCODED_USER_ID,
			description: shortDescription,
			long_description: longDescription,
			links: links.filter((h) => h.text.trim() || h.url.trim()),
			wanted_contributors: wantedContributors
		};

		const result = await createIdea(ideaData);

		if (result instanceof Error) {
			console.error('Error creating idea:', result);
			alert(`An error occurred: ${result.message}`);
		} else {
			console.log('Idea successfully sent:', result);
			goto('/');
		}
	}

	function handleCancel() {
		goto('/');
	}
</script>

<div class="relative min-h-screen w-full">
	<!-- Background image -->
	<div
		class="fixed inset-[-10px] z-0 scale-110
            bg-cover bg-fixed bg-center
            blur-2xl"
		style="background-image: url('{backgroundImage}')"
	></div>

	<!-- NAVBAR -->
	<nav
		class="fixed left-0 right-0 top-0 z-20 flex
				h-[60px] items-center justify-end border-b
                border-white/10 bg-white/5 px-4 backdrop-blur-sm"
	>
		<!-- Placeholder for navbar items if any -->
	</nav>

	<!-- Sidebar -->
	<aside
		class="fixed bottom-0 left-0 top-0 z-10 w-20
				  border-r border-white/10 bg-white/5 backdrop-blur-sm"
	></aside>

	<!-- Main Content -->
	<main
		class="relative z-10 flex min-h-screen w-full items-center justify-center
				 pb-10 pl-20 pt-[60px]"
	>
		<form
			on:submit|preventDefault={handleSubmit}
			class="relative my-10 flex w-3/4 min-w-[600px]
                    max-w-[1000px] flex-col gap-5
                    rounded-2xl border border-white/20
                    bg-violet-900/40 p-8 shadow-2xl backdrop-blur-xl"
		>
			<h2 class="mb-4 text-center text-2xl font-bold text-white">Add New Idea</h2>

			<!-- Title -->
			<div class="flex flex-col gap-2">
				<label for="title" class="font-semibold text-white/80">Title</label>
				<input
					id="title"
					type="text"
					placeholder="Project Title"
					required
					bind:value={title}
					maxlength="200"
					class="w-full rounded-lg border border-white/30
                        bg-white/15 p-3 text-lg font-bold
                        text-white placeholder-white/70 outline-none
                        focus:border-white/50"
				/>
			</div>

			<!-- Short Description -->
			<div class="flex flex-col gap-2">
				<label for="shortDesc" class="font-semibold text-white/80">Short Description</label>
				<textarea
					id="shortDesc"
					required
					bind:value={shortDescription}
					rows="3"
					placeholder="Brief overview of the project..."
					class="w-full resize-none rounded-lg border border-white/30
                        bg-white/15 p-3 text-white placeholder-white/70 outline-none
                        focus:border-white/50"
				></textarea>
			</div>

			<!-- Long Description -->
			<div class="flex flex-col gap-2">
				<label for="longDesc" class="font-semibold text-white/80">Long Description</label>
				<textarea
					id="longDesc"
					bind:value={longDescription}
					rows="6"
					placeholder="Detailed explanation of the project..."
					class="w-full resize-none rounded-lg border border-white/30
                        bg-white/15 p-3 text-white placeholder-white/70 outline-none
                        focus:border-white/50"
				></textarea>
			</div>

			<!-- Hyperlinks -->
			<div class="flex flex-col gap-2">
				<span class="font-semibold text-white/80">External Links</span>
				{#each links as link, i}
					<div class="mb-2 flex gap-2">
						<input
							type="text"
							placeholder="Label (e.g. GitHub)"
							bind:value={link.text}
							class="flex-1 rounded-lg border border-white/30
                                bg-white/15 p-2 text-white placeholder-white/70 outline-none
                                focus:border-white/50"
						/>
						<input
							type="text"
							placeholder="URL (https://...)"
							bind:value={link.url}
							class="flex-2 rounded-lg border border-white/30
                                bg-white/15 p-2 text-white placeholder-white/70 outline-none
                                focus:border-white/50"
						/>
						<button
							type="button"
							on:click={() => removeLink(i)}
							class="rounded-lg bg-red-500/20 px-3 py-2 text-red-300 hover:bg-red-500/40"
							disabled={links.length === 1}
						>
							✕
						</button>
					</div>
				{/each}
				<button
					type="button"
					on:click={addLink}
					class="self-start rounded-lg bg-white/10 px-4 py-2 text-sm text-white hover:bg-white/20"
				>
					+ Add Link
				</button>
			</div>

			<!-- Roles -->
			<div class="flex flex-col gap-2">
				<label for="wantedContributors" class="font-semibold text-white/80">Wanted Roles</label>
				<textarea
					id="wantedContributors"
					bind:value={wantedContributors}
					rows="4"
					placeholder="Describe the roles you are looking for..."
					class="w-full resize-none rounded-lg border border-white/30
                        bg-white/15 p-3 text-white placeholder-white/70 outline-none
                        focus:border-white/50"
				></textarea>
			</div>

			<!-- Buttons -->
			<div class="mt-8 flex justify-end gap-4 pb-4">
				<button
					type="button"
					on:click={handleCancel}
					class="rounded-lg border-2 border-fuchsia-600
                           bg-teal-950 px-8 py-3
                           font-bold text-fuchsia-600
                           transition-colors hover:bg-fuchsia-600 hover:text-white"
				>
					Cancel
				</button>

				<button
					type="submit"
					class="rounded-lg bg-violet-900 px-8 py-3
                           font-bold text-white
                           transition-colors hover:bg-violet-700"
				>
					Submit
				</button>
			</div>
		</form>
	</main>
</div>
