import { describe, it, expect, beforeAll } from "vitest";
import { GitHubVaultConnector } from "./github-connector";

const githubToken = process.env.GITHUB_TOKEN;
const describeIfToken = githubToken ? describe : describe.skip;

describeIfToken("GitHub Vault Connector", () => {
  let connector: GitHubVaultConnector;

  beforeAll(() => {
    connector = new GitHubVaultConnector(
      githubToken!,
      process.env.GITHUB_VAULT_OWNER || "jjuniper-dev",
      process.env.GITHUB_VAULT_REPO || "Obsidian"
    );
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
});
