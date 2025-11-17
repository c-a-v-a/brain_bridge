import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { refresh } from '$lib/api/tokenApi'; 

export const load: PageServerLoad = async ({ cookies }) => {
    const refreshResult = await refresh(cookies);

    if (refreshResult instanceof Error) {
        return {}; 
    }

    throw redirect(302, '/'); 
};