import { createServer } from "node:http";
import { readFile } from "node:fs/promises";
import { extname, join, normalize, resolve } from "node:path";
import { dirname } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..", "src");
const port = Number(process.env.PORT || 5173);
const types = { ".html": "text/html", ".css": "text/css", ".js": "text/javascript" };

createServer(async (request, response) => {
  const urlPath = new URL(request.url, `http://127.0.0.1:${port}`).pathname;
  const requested = urlPath === "/" ? "index.html" : urlPath.slice(1);
  const filePath = normalize(join(root, requested));
  if (!filePath.startsWith(root)) {
    response.writeHead(403);
    response.end("Forbidden");
    return;
  }
  try {
    const body = await readFile(filePath);
    response.writeHead(200, { "content-type": types[extname(filePath)] || "application/octet-stream" });
    response.end(body);
  } catch {
    response.writeHead(404);
    response.end("Not found");
  }
}).listen(port, "127.0.0.1", () => {
  console.log(`Interactive resume frontend: http://127.0.0.1:${port}`);
});
