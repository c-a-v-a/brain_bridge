// src/routes/dashboard/+page.server.ts

import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
// Import universal functions
import { refresh, logout } from '$lib/api/tokenApi'; 

export const load: PageServerLoad = async ({ cookies }) => {
    // 1. Attempt to refresh tokens using the universal 'refresh' function.
    // We pass the SvelteKit 'cookies' object so 'refresh' uses the server-side logic
    // for reading and writing cookies.
    const refreshResult = await refresh(cookies);

    if (refreshResult instanceof Error) {
        // 2. Failure: Refresh failed (token missing or expired/invalid).
        
        // Ensure all tokens are deleted (important for safety)
        logout(cookies); 

        // Redirect the user to the login page
        throw redirect(302, '/login'); 
    }

    // 3. Success: Refresh succeeded. The new token pair has already been
    // saved in the cookies by the 'refresh' function itself.
    
    // Allow access to the dashboard
    return {
        status: 'authenticated',
        message: 'Session successfully renewed.'
        // You can fetch protected dashboard data here if needed
    };
};