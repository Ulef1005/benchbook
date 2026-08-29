import { execFileSync } from "node:child_process";

/** Needs fetch-depth: 0 in the workflow, or every file reports the same commit. */
export function lastUpdated(repoPath: string): { date: string; sha: string } | null {
  try {
    const out = execFileSync("git", ["log", "-1", "--format=%cs %h", "--", repoPath], {
      cwd: process.cwd(), encoding: "utf8",
    }).trim();
    if (!out) return null;
    const [date, sha] = out.split(" ");
    return { date, sha };
  } catch {
    return null; // shallow clone or not a git checkout — the strip just doesn't render
  }
}

export const GITHUB = "https://github.com/Ulef1005/benchbook";
export const editUrl = (repoPath: string) => `${GITHUB}/blob/main/${repoPath}`;
