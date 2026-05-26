import { initTRPC } from "@trpc/server";

/**
 * Minimal tRPC bootstrap for server-side dashboard routers.
 *
 * This keeps feature routers decoupled from transport/runtime wiring while
 * preserving a single place to introduce context, auth, and protected
 * procedures later.
 */
const t = initTRPC.create();

export const router = t.router;
export const publicProcedure = t.procedure;
