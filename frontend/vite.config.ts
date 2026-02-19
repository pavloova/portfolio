import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// VITE_BASE_PATH="/portfolio/" for GitHub Pages, "/" for local/Vercel
const base = process.env.VITE_BASE_PATH ?? "/";

export default defineConfig({
  base,
  plugins: [react()],
  server: { port: 5173, host: true },
  build: { outDir: "dist", sourcemap: true },
});
