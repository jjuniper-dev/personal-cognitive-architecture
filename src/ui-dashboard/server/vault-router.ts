import { z } from "zod";
import { publicProcedure, router } from "./_core/trpc";
import { GitHubVaultConnector } from "./github-connector";

const SAFE_PATH_REGEX = /^[a-zA-Z0-9_\-/.]+$/;

const validatePath = (path: string) => {
  if (
    path.includes("..") ||
    path.startsWith("/") ||
    !SAFE_PATH_REGEX.test(path)
  ) {
    throw new Error("Invalid vault path");
  }
};

const getVaultConnector = () => {
  const token = process.env.GITHUB_TOKEN;

  if (!token) {
    throw new Error("GITHUB_TOKEN environment variable not set");
  }

  return new GitHubVaultConnector(
    token,
    process.env.GITHUB_VAULT_OWNER || "jjuniper-dev",
    process.env.GITHUB_VAULT_REPO || "Obsidian"
  );
};

export const vaultRouter = router({
  structure: publicProcedure.query(async () => {
    const connector = getVaultConnector();
    return connector.getVaultStructure();
  }),

  metadata: publicProcedure.query(async () => {
    const connector = getVaultConnector();
    return connector.getVaultMetadata();
  }),

  listNotes: publicProcedure
    .input(z.object({ folderPath: z.string().min(1).max(200) }))
    .query(async ({ input }) => {
      validatePath(input.folderPath);

      const connector = getVaultConnector();
      return connector.listNotesInFolder(input.folderPath);
    }),

  getNote: publicProcedure
    .input(z.object({ path: z.string().min(1).max(500) }))
    .query(async ({ input }) => {
      validatePath(input.path);

      const connector = getVaultConnector();
      return connector.getNote(input.path);
    }),

  search: publicProcedure
    .input(z.object({ query: z.string().min(1).max(200) }))
    .query(async ({ input }) => {
      const connector = getVaultConnector();
      return connector.searchNotes(input.query);
    }),

  getCanonicalNotes: publicProcedure.query(async () => {
    const connector = getVaultConnector();
    return connector.listNotesInFolder("04_Concepts");
  }),

  getInboxNotes: publicProcedure.query(async () => {
    const connector = getVaultConnector();
    return connector.listNotesInFolder("00_Inbox");
  }),

  getDailyNotes: publicProcedure.query(async () => {
    const connector = getVaultConnector();
    return connector.listNotesInFolder("01_Daily");
  }),

  getResearchNotes: publicProcedure.query(async () => {
    const connector = getVaultConnector();
    return connector.listNotesInFolder("03_Research");
  }),

  getProjectNotes: publicProcedure.query(async () => {
    const connector = getVaultConnector();
    return connector.listNotesInFolder("02_Projects");
  }),
});
