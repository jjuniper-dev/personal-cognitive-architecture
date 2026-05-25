import { z } from "zod";
import { publicProcedure, router } from "./_core/trpc";
import { GitHubVaultConnector } from "./github-connector";

/**
 * Vault Router
 * 
 * Provides tRPC procedures for accessing the Obsidian vault via GitHub
 * as a backup source for the cognitive architecture dashboard.
 */

// Initialize GitHub connector (requires GITHUB_TOKEN env var)
const getVaultConnector = () => {
  const token = process.env.GITHUB_TOKEN;
  if (!token) {
    throw new Error("GITHUB_TOKEN environment variable not set");
  }
  return new GitHubVaultConnector(token, "jjuniper-dev", "Obsidian");
};

export const vaultRouter = router({
  /**
   * Get vault structure and folder listing
   */
  structure: publicProcedure.query(async () => {
    try {
      const connector = getVaultConnector();
      const folders = await connector.getVaultStructure();
      return {
        success: true,
        data: folders,
      };
    } catch (error) {
      console.error("[Vault Router] Failed to get structure:", error);
      return {
        success: false,
        error: "Failed to retrieve vault structure",
        data: [],
      };
    }
  }),

  /**
   * Get vault metadata and statistics
   */
  metadata: publicProcedure.query(async () => {
    try {
      const connector = getVaultConnector();
      const metadata = await connector.getVaultMetadata();
      return {
        success: true,
        data: metadata,
      };
    } catch (error) {
      console.error("[Vault Router] Failed to get metadata:", error);
      return {
        success: false,
        error: "Failed to retrieve vault metadata",
        data: null,
      };
    }
  }),

  /**
   * List notes in a specific folder
   */
  listNotes: publicProcedure
    .input(z.object({ folderPath: z.string() }))
    .query(async ({ input }) => {
      try {
        const connector = getVaultConnector();
        const notes = await connector.listNotesInFolder(input.folderPath);
        return {
          success: true,
          data: notes,
        };
      } catch (error) {
        console.error("[Vault Router] Failed to list notes:", error);
        return {
          success: false,
          error: "Failed to retrieve notes",
          data: [],
        };
      }
    }),

  /**
   * Get a specific note by path
   */
  getNote: publicProcedure
    .input(z.object({ path: z.string() }))
    .query(async ({ input }) => {
      try {
        const connector = getVaultConnector();
        const note = await connector.getNote(input.path);
        return {
          success: true,
          data: note,
        };
      } catch (error) {
        console.error("[Vault Router] Failed to get note:", error);
        return {
          success: false,
          error: "Failed to retrieve note",
          data: null,
        };
      }
    }),

  /**
   * Search notes by query
   */
  search: publicProcedure
    .input(z.object({ query: z.string() }))
    .query(async ({ input }) => {
      try {
        const connector = getVaultConnector();
        const results = await connector.searchNotes(input.query);
        return {
          success: true,
          data: results,
        };
      } catch (error) {
        console.error("[Vault Router] Failed to search notes:", error);
        return {
          success: false,
          error: "Failed to search notes",
          data: [],
        };
      }
    }),

  /**
   * Get canonical notes (from 04_Concepts folder)
   */
  getCanonicalNotes: publicProcedure.query(async () => {
    try {
      const connector = getVaultConnector();
      const notes = await connector.listNotesInFolder("04_Concepts");
      return {
        success: true,
        data: notes,
      };
    } catch (error) {
      console.error("[Vault Router] Failed to get canonical notes:", error);
      return {
        success: false,
        error: "Failed to retrieve canonical notes",
        data: [],
      };
    }
  }),

  /**
   * Get inbox notes (from 00_Inbox folder)
   */
  getInboxNotes: publicProcedure.query(async () => {
    try {
      const connector = getVaultConnector();
      const notes = await connector.listNotesInFolder("00_Inbox");
      return {
        success: true,
        data: notes,
      };
    } catch (error) {
      console.error("[Vault Router] Failed to get inbox notes:", error);
      return {
        success: false,
        error: "Failed to retrieve inbox notes",
        data: [],
      };
    }
  }),

  /**
   * Get daily notes (from 01_Daily folder)
   */
  getDailyNotes: publicProcedure.query(async () => {
    try {
      const connector = getVaultConnector();
      const notes = await connector.listNotesInFolder("01_Daily");
      return {
        success: true,
        data: notes,
      };
    } catch (error) {
      console.error("[Vault Router] Failed to get daily notes:", error);
      return {
        success: false,
        error: "Failed to retrieve daily notes",
        data: [],
      };
    }
  }),

  /**
   * Get research notes (from 03_Research folder)
   */
  getResearchNotes: publicProcedure.query(async () => {
    try {
      const connector = getVaultConnector();
      const notes = await connector.listNotesInFolder("03_Research");
      return {
        success: true,
        data: notes,
      };
    } catch (error) {
      console.error("[Vault Router] Failed to get research notes:", error);
      return {
        success: false,
        error: "Failed to retrieve research notes",
        data: [],
      };
    }
  }),

  /**
   * Get project notes (from 02_Projects folder)
   */
  getProjectNotes: publicProcedure.query(async () => {
    try {
      const connector = getVaultConnector();
      const notes = await connector.listNotesInFolder("02_Projects");
      return {
        success: true,
        data: notes,
      };
    } catch (error) {
      console.error("[Vault Router] Failed to get project notes:", error);
      return {
        success: false,
        error: "Failed to retrieve project notes",
        data: [],
      };
    }
  }),
});
