<script lang="ts">
	import backgroundImage from '$lib/assets/dashboard-bg.png';
</script>

<div class="relative min-h-screen w-full overflow-hidden">
	<div
		class="absolute inset-[-10px] z-0 scale-110
            bg-cover bg-fixed bg-center
            blur-[40px]"
		style="background-image: url('{backgroundImage}')"
	></div>

	<div class="relative z-10 flex min-h-screen w-full items-center justify-center">
		<h1 class="text-3xl font-bold text-white">Liked Ideas</h1>
	</div>
</div>
