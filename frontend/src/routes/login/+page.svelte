<script lang="ts">

  let userLog = {
    usernameEmail: '',
    password: '',
  };

  function handleSubmit() {
   // TODO: fetch data to API
    console.log('Dane do rejestracji:', userLog);
    alert('Formularz wysłany! Sprawdź konsolę.');
  }
</script>

<div class="min-h-screen bg-gray-100 flex flex-col lg:flex-row">
  <div class="w-full lg:w-1/3 flex justify-center p-8 text-white
              bg-linear-to-br from-teal-700 via-violet-800 to-teal-700">
    <div class="absolute inset-0 z-0 backdrop-filter backdrop-blur-3xl"></div>
    <div class="relative z-10 max-w-md lg:mt-20 text-left lg:text-left">
      <h1 class="text-4xl lg:text-5xl font-extrabold leading-tight mb-4 opacity-90">
        The bridge between ideas.
      </h1>
      <p class="text-2xl lg:text-3xl font-semibold opacity-80">
        Brings people together.
      </p>
    </div>
  </div>

  <div class="w-full lg:w-2/3 flex z-10 items-center justify-center p-8 bg-white lg:rounded-l-4xl">
    <div class="max-w-2xl w-full mb-52">
      <h2 class="text-5xl font-bold mb-20 text-gray-800 text-center lg:text-left">Log in</h2>

      <form on:submit|preventDefault={handleSubmit} class="space-y-6">
        <div>
          <label for="username" class="block text-sm font-medium text-gray-700">Email or username</label>
          <input
            type="text"
            id="username"
            name="username"
            bind:value={userLog.usernameEmail}
            class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm
                   focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            placeholder="your.email@example.com"
            required
          />
        </div>

        <div>
          <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
          <input
            type="password"
            id="password"
            name="password"
            bind:value={userLog.password}
            class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm
                   focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            placeholder="Minimum 8 characters"
            required
          />
        </div>

        <div>
          <button
            type="submit"
            class="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg
                   shadow-sm text-lg font-medium text-white bg-teal-950 hover:bg-cyan-800
                   focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            Log in
          </button>
        </div>
      </form>

      <p class="mt-8 text-left text-sm text-gray-600">
        Don't have an account yet?
        <a href="/register" class="font-medium text-indigo-600 hover:text-indigo-500">
          Sign up
        </a>
      </p>
    </div>
  </div>
</div>