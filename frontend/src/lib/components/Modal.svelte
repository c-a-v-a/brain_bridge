<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { fade, scale } from 'svelte/transition';

	export let show: boolean = false;

	const dispatch = createEventDispatcher();

	function close() {
		dispatch('close');
	}

	function handleKeydown(event: KeyboardEvent) {
		if (event.key === 'Escape') {
			close();
		}
	}
</script>

<svelte:window on:keydown={handleKeydown} />

{#if show}
	<!-- Backdrop -->
	<!-- svelte-ignore a11y-click-events-have-key-events -->
	<!-- svelte-ignore a11y-no-static-element-interactions -->
	<div
		class="fixed inset-0 z-50 flex h-full w-full cursor-default items-center justify-center border-none bg-black/80 backdrop-blur-sm"
		on:click={close}
		transition:fade={{ duration: 200 }}
		role="button"
		tabindex="-1"
		aria-label="Close modal"
	>
		<!-- Modal Content -->
		<!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
		<div
			class="relative max-h-[90vh] max-w-[90vw] cursor-auto overflow-auto rounded-lg bg-[#0f172a]/10 shadow-2xl"
			on:click|stopPropagation
			on:keydown|stopPropagation
			transition:scale={{ duration: 200, start: 0.95 }}
			role="document"
			tabindex="-1"
		>
			<button
				class="absolute right-4 top-4 z-10 rounded-full bg-black/30 p-2 text-white transition-colors hover:bg-black/70"
				on:click={close}
				aria-label="Close"
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					fill="none"
					viewBox="0 0 24 24"
					stroke-width="1.5"
					stroke="currentColor"
					class="h-6 w-6"
				>
					<path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
				</svg>
			</button>
			<slot />
		</div>
	</div>
{/if}
