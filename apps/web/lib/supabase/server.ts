import { createServerClient } from "@supabase/ssr";
import { cookies } from "next/headers";
import { redirect } from "next/navigation";

import { supabasePublishableKey, supabaseUrl } from "@/lib/supabase/config";

export function createSupabaseServerClient() {
  const cookieStore = cookies();
  type CookieToSet = {
    name: string;
    value: string;
    options?: any;
  };

  return createServerClient(supabaseUrl, supabasePublishableKey, {
    cookies: {
      getAll() {
        return cookieStore.getAll();
      },
      setAll(cookiesToSet: CookieToSet[]) {
        try {
          cookiesToSet.forEach((cookie) => {
            cookieStore.set(cookie.name, cookie.value, cookie.options);
          });
        } catch {
          // Server Components cannot always mutate cookies; middleware refresh handles persistence.
        }
      },
    },
  });
}

export async function getAuthenticatedUser() {
  const supabase = createSupabaseServerClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();

  return user;
}

export async function requireAuthenticatedUser() {
  const user = await getAuthenticatedUser();

  if (!user) {
    redirect("/login");
  }

  return user;
}
