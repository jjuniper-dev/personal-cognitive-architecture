import { Octokit } from "@octokit/rest";

/**
 * GitHub Connector for Obsidian Vault Integration
 *
 * Provides read-only access to the Obsidian vault stored in GitHub
 * as a synchronization and backup source for the cognitive architecture dashboard.
 *
 * Canonical authority remains the local-first Obsidian vault.
 */

export interface VaultNote {
  path: string;
  name: string;
  content: string;
  frontmatter: Record<string, unknown>;
  lastModified: string;
  type: "concept" | "daily" | "project" | "research" | "output" | "reference" | "template";
}

export interface VaultFolder {
  name: string;
  path: string;
  description: string;
  noteCount: number;
}

export interface VaultMetadata {
  totalNotes: number;
  totalFolders: number;
  lastSync: string;
  folders: VaultFolder[];
}

export class GitHubVaultConnector {
  private octokit: Octokit;
  private owner: string;
  private repo: string;
  private branch = "main";

  constructor(githubToken: string, owner: string = "jjuniper-dev", repo: string = "Obsidian") {
    this.octokit = new Octokit({ auth: githubToken });
    this.owner = owner;
    this.repo = repo;
  }

  async getVaultStructure(): Promise<VaultFolder[]> {
    try {
      const { data } = await this.octokit.repos.getContent({
        owner: this.owner,
        repo: this.repo,
        path: "",
        ref: this.branch,
      });

      if (!Array.isArray(data)) {
        return [];
      }

      const folders: VaultFolder[] = [];
      const folderMap: Record<string, number> = {};

      const allFiles = await this.getAllMarkdownFiles();
      allFiles.forEach((file) => {
        const folderPath = file.path.split("/")[0];
        folderMap[folderPath] = (folderMap[folderPath] || 0) + 1;
      });

      const folderDescriptions: Record<string, string> = {
        "00_Inbox": "Temporary ingestion zone for new captures",
        "01_Daily": "Daily cognitive snapshots and reflections",
        "02_Projects": "Active execution-oriented work",
        "03_Research": "Exploration and investigation space",
        "04_Concepts": "Stable knowledge primitives and frameworks",
        "05_Themes": "Cross-cutting domains and recurring patterns",
        "06_People": "Relationship and context layer",
        "07_Outputs": "Finalized artifacts and publications",
        "08_Media": "Non-text supporting material",
        "20_MOCs": "Maps of Content for navigation",
        "30_Templates": "Reusable cognitive structures",
        "40_References": "External source preservation",
        "_system": "Machine-operated infrastructure",
        "90_Archive": "Archived and historical content",
      };

      for (const item of data) {
        if (item.type === "dir" && !item.name.startsWith(".")) {
          folders.push({
            name: item.name,
            path: item.path,
            description: folderDescriptions[item.name] || "Vault folder",
            noteCount: folderMap[item.name] || 0,
          });
        }
      }

      return folders.sort((a, b) => {
        const aNum = parseInt(a.name.split("_")[0]) || 999;
        const bNum = parseInt(b.name.split("_")[0]) || 999;
        return aNum - bNum;
      });
    } catch (error) {
      console.error("[GitHub Connector] Failed to get vault structure:", error);
      return [];
    }
  }

  private async getAllMarkdownFiles(path: string = ""): Promise<Array<{ path: string }>> {
    try {
      const { data } = await this.octokit.repos.getContent({
        owner: this.owner,
        repo: this.repo,
        path: path || "",
        ref: this.branch,
      });

      if (!Array.isArray(data)) {
        return [];
      }

      let files: Array<{ path: string }> = [];

      for (const item of data) {
        if (item.type === "file" && (item as any).name.endsWith(".md")) {
          files.push({ path: (item as any).path });
        } else if (item.type === "dir" && !(item as any).name.startsWith(".") && (item as any).name !== "_system") {
          const subFiles = await this.getAllMarkdownFiles((item as any).path);
          files = files.concat(subFiles);
        }
      }

      return files;
    } catch (error) {
      console.error("[GitHub Connector] Failed to get markdown files:", error);
      return [];
    }
  }

  async getNote(path: string): Promise<VaultNote | null> {
    try {
      const { data } = await this.octokit.repos.getContent({
        owner: this.owner,
        repo: this.repo,
        path,
        ref: this.branch,
      });

      if (typeof data === "string" || Array.isArray(data)) {
        return null;
      }

      const fileData = data as any;

      if (fileData.type !== "file" || !fileData.download_url) {
        return null;
      }

      const response = await fetch(fileData.download_url);

      if (!response.ok) {
        console.error(`[GitHub Connector] Failed to download note ${path}: ${response.status}`);
        return null;
      }

      const content = await response.text();

      const { frontmatter, body } = this.parseFrontmatter(content);
      const type = this.inferNoteType(path);

      return {
        path: fileData.path,
        name: fileData.name,
        content: body,
        frontmatter: frontmatter || {},
        lastModified: new Date().toISOString(),
        type,
      };
    } catch (error) {
      console.error("[GitHub Connector] Failed to get note:", error);
      return null;
    }
  }

  async listNotesInFolder(folderPath: string): Promise<VaultNote[]> {
    try {
      const { data } = await this.octokit.repos.getContent({
        owner: this.owner,
        repo: this.repo,
        path: folderPath,
        ref: this.branch,
      });

      if (!Array.isArray(data)) {
        return [];
      }

      const notes: VaultNote[] = [];

      for (const item of data) {
        if (item.type === "file" && (item as any).name.endsWith(".md")) {
          const note = await this.getNote((item as any).path);
          if (note) {
            notes.push(note);
          }
        }
      }

      return notes;
    } catch (error) {
      console.error("[GitHub Connector] Failed to list notes:", error);
      return [];
    }
  }

  async getVaultMetadata(): Promise<VaultMetadata> {
    try {
      const folders = await this.getVaultStructure();
      const totalNotes = folders.reduce((sum, f) => sum + f.noteCount, 0);

      return {
        totalNotes,
        totalFolders: folders.length,
        lastSync: new Date().toISOString(),
        folders,
      };
    } catch (error) {
      console.error("[GitHub Connector] Failed to get vault metadata:", error);
      return {
        totalNotes: 0,
        totalFolders: 0,
        lastSync: new Date().toISOString(),
        folders: [],
      };
    }
  }

  async searchNotes(query: string): Promise<VaultNote[]> {
    try {
      const allFiles = await this.getAllMarkdownFiles();
      const results: VaultNote[] = [];

      for (const file of allFiles) {
        const note = await this.getNote(file.path);
        if (note) {
          const contentMatch = note.content.toLowerCase().includes(query.toLowerCase());
          const frontmatterMatch = JSON.stringify(note.frontmatter)
            .toLowerCase()
            .includes(query.toLowerCase());
          const pathMatch = note.path.toLowerCase().includes(query.toLowerCase());

          if (contentMatch || frontmatterMatch || pathMatch) {
            results.push(note);
          }
        }
      }

      return results;
    } catch (error) {
      console.error("[GitHub Connector] Failed to search notes:", error);
      return [];
    }
  }

  private parseFrontmatter(content: string): {
    frontmatter: Record<string, unknown> | null;
    body: string;
  } {
    const frontmatterRegex = /^---\n([\s\S]*?)\n---\n([\s\S]*)$/;
    const match = content.match(frontmatterRegex);

    if (!match) {
      return { frontmatter: null, body: content };
    }

    const [, frontmatterStr, body] = match;
    const frontmatter: Record<string, unknown> = {};

    frontmatterStr.split("\n").forEach((line) => {
      const colonIndex = line.indexOf(":");
      if (colonIndex > 0) {
        const key = line.substring(0, colonIndex).trim();
        const value = line.substring(colonIndex + 1).trim();
        frontmatter[key] = value.replace(/^["']|["']$/g, "");
      }
    });

    return { frontmatter, body };
  }

  private inferNoteType(
    path: string
  ): "concept" | "daily" | "project" | "research" | "output" | "reference" | "template" {
    if (path.includes("00_Inbox")) return "reference";
    if (path.includes("01_Daily")) return "daily";
    if (path.includes("02_Projects")) return "project";
    if (path.includes("03_Research")) return "research";
    if (path.includes("04_Concepts")) return "concept";
    if (path.includes("07_Outputs")) return "output";
    if (path.includes("30_Templates")) return "template";
    return "reference";
  }
}
