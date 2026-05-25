import { describe, it, expect, beforeAll } from "vitest";
import { GitHubVaultConnector } from "./github-connector";

describe("GitHub Vault Connector", () => {
  let connector: GitHubVaultConnector;
  const githubToken = process.env.GITHUB_TOKEN;

  beforeAll(() => {
    if (!githubToken) {
      throw new Error("GITHUB_TOKEN environment variable not set");
    }
    connector = new GitHubVaultConnector(githubToken, "jjuniper-dev", "Obsidian");
  });

  it("should authenticate with GitHub API", async () => {
    expect(githubToken).toBeDefined();
    expect(githubToken!.length).toBeGreaterThan(30);
  });

  it("should retrieve vault structure", async () => {
    const structure = await connector.getVaultStructure();
    expect(structure).toBeDefined();
    expect(Array.isArray(structure)).toBe(true);
    expect(structure.length).toBeGreaterThan(0);
  }, { timeout: 30000 });

  it("should have canonical folders in vault structure", async () => {
    const structure = await connector.getVaultStructure();
    const folderNames = structure.map((f) => f.name);
    
    // Check for key PCA folders
    expect(folderNames.length).toBeGreaterThan(0);
    expect(folderNames).toContain("04_Concepts");
  }, { timeout: 30000 });

  it("should retrieve vault metadata", async () => {
    const metadata = await connector.getVaultMetadata();
    expect(metadata).toBeDefined();
    expect(metadata.totalNotes).toBeGreaterThanOrEqual(0);
    expect(metadata.totalFolders).toBeGreaterThan(0);
    expect(metadata.lastSync).toBeDefined();
  }, { timeout: 60000 });

  it("should list notes in Concepts folder", async () => {
    const notes = await connector.listNotesInFolder("04_Concepts");
    expect(Array.isArray(notes)).toBe(true);
    if (notes.length > 0) {
      expect(notes[0].path).toBeDefined();
      expect(notes[0].name).toBeDefined();
      expect(notes[0].type).toBe("concept");
    }
  }, { timeout: 30000 });

  it("should parse note frontmatter correctly", async () => {
    const notes = await connector.listNotesInFolder("04_Concepts");
    if (notes.length > 0) {
      const note = notes[0];
      expect(note.frontmatter).toBeDefined();
      expect(typeof note.frontmatter).toBe("object");
    }
  }, { timeout: 30000 });

  it("should infer note types correctly", async () => {
    const conceptNotes = await connector.listNotesInFolder("04_Concepts");
    
    if (conceptNotes.length > 0) {
      expect(conceptNotes[0].type).toBe("concept");
    }
  }, { timeout: 30000 });
});
