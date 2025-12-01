<script lang="ts">
	import { page } from '$app/stores';

	let { children } = $props();
</script>

<div class="min-h-screen w-full bg-[#0f172a] text-white">
	<!-- Sidebar -->
	<aside
		class="fixed left-0 top-0 z-40 h-screen w-64 border-r border-white/10 bg-slate-900/90 backdrop-blur-md"
	>
		<!-- Title Area -->
		<div class="flex h-16 items-center border-b border-white/10 px-6">
			<h1 class="text-xl font-bold tracking-wider text-white">
				<span class="text-cyan-400">Brain</span>Bridge
			</h1>
		</div>

		<!-- Navigation -->
		<nav class="mt-6 px-4">
			<ul class="space-y-2">
				<!-- Dashboard -->
				<li>
					<a
						href="/"
						class="flex items-center gap-3 rounded-lg px-4 py-3 text-sm font-medium transition-colors hover:bg-white/10 {$page
							.url.pathname === '/'
							? 'bg-white/10 text-cyan-400'
							: 'text-slate-300'}"
					>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							fill="none"
							viewBox="0 0 24 24"
							stroke-width="1.5"
							stroke="currentColor"
							class="h-6 w-6"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25"
							/>
						</svg>
						Dashboard
					</a>
				</li>
				<!-- Create Idea -->
				<li>
					<a
						href="/add-idea"
						class="flex items-center gap-3 rounded-lg px-4 py-3 text-sm font-medium transition-colors hover:bg-white/10 {$page
							.url.pathname === '/add-idea'
							? 'bg-white/10 text-cyan-400'
							: 'text-slate-300'}"
					>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							fill="none"
							viewBox="0 0 24 24"
							stroke-width="1.5"
							stroke="currentColor"
							class="h-6 w-6"
						>
							<path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
						</svg>
						Create Idea
					</a>
				</li>
				<!-- Liked Ideas -->
				<li>
					<a
						href="/liked-ideas"
						class="flex items-center gap-3 rounded-lg px-4 py-3 text-sm font-medium transition-colors hover:bg-white/10 {$page
							.url.pathname === '/liked-ideas'
							? 'bg-white/10 text-cyan-400'
							: 'text-slate-300'}"
					>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							fill="none"
							viewBox="0 0 24 24"
							stroke-width="1.5"
							stroke="currentColor"
							class="h-6 w-6"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z"
							/>
						</svg>
						Liked Ideas
					</a>
				</li>
			</ul>
		</nav>
	</aside>

	<!-- Main Content -->
	<main class="ml-64 min-h-screen">
		{@render children?.()}
	</main>
</div>
