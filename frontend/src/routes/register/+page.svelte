<script lang="ts">
  import type { UserCreate } from '$lib/models/user.models';

  let newUser: UserCreate = {
    username: '',
    name: '',
    surname: '',
    email: '',
    password: '',
    is_admin: false
  };

  function handleSubmit() {
   // TODO: fetch data to API
    console.log('Dane do rejestracji:', newUser);
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
    <div class="max-w-2xl w-full mb-40">
      <h2 class="text-5xl font-bold mb-20 text-gray-800 text-center lg:text-left">Create an Account</h2>

      <form on:submit|preventDefault={handleSubmit} class="space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label for="name" class="block text-sm font-medium text-gray-700">Name</label>
            <input
              type="text"
              id="name"
              name="name"
              bind:value={newUser.name}
              class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm
                     focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              placeholder="Your name"
              required
            />
          </div>
          <div>
            <label for="surename" class="block text-sm font-medium text-gray-700">Last name</label>
            <input
              type="text"
              id="surename"
              name="surename"
              bind:value={newUser.surname}
              class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm
                     focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              placeholder="Your last name"
              required
            />
          </div>
        </div>

        <div>
          <label for="username" class="block text-sm font-medium text-gray-700">Username</label>
          <input
            type="text"
            id="username"
            name="username"
            bind:value={newUser.username}
            class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm
                   focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            placeholder="einstein9000"
            required
          />
        </div>

        <div>
          <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
          <input
            type="email"
            id="email"
            name="email"
            bind:value={newUser.email}
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
            bind:value={newUser.password}
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
            Create an Account
          </button>
        </div>
      </form>

      <p class="mt-8 text-left text-sm text-gray-600">
        Do you already have an account?
        <a href="/login" class="font-medium text-indigo-600 hover:text-indigo-500">
          Log in.
        </a>
      </p>
    </div>
  </div>
</div>