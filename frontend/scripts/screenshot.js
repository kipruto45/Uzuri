const puppeteer = require("puppeteer");
const fs = require("fs");
const path = require("path");

const PORTS = [5173, 5174];
let BASE = "http://localhost:5173";
const ROUTES = [
  "/",
  "/attachments",
  "/clearance",
  "/calendar",
  "/accessibility",
  "/ai-support",
];
const OUT_DIR = path.join(__dirname, "..", "screenshots");

async function waitForServer(urls, timeout = 30000) {
  const start = Date.now();
  while (Date.now() - start < timeout) {
    for (const url of urls) {
      try {
        const res = await fetch(url, { method: "HEAD" });
        if (res && res.ok) {
          BASE = url;
          return;
        }
      } catch (e) {}
    }
    await new Promise((r) => setTimeout(r, 500));
  }
  throw new Error("Server did not become ready in time: " + urls.join(", "));
}

(async () => {
  if (!fs.existsSync(OUT_DIR)) fs.mkdirSync(OUT_DIR, { recursive: true });

  const urls = PORTS.map((p) => `http://localhost:${p}`);
  console.log("Waiting for dev server on", urls.join(", "));
  try {
    await waitForServer(urls);
  } catch (e) {
    console.warn("Server did not respond to HEAD; continuing anyway");
  }

  const browser = await puppeteer.launch({
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });
  try {
    for (const route of ROUTES) {
      const url = BASE + route;
      const slug =
        route === "/"
          ? "dashboard"
          : route.replace(/\//g, "").replace(/[^a-z0-9_-]/gi, "_");
      const page = await browser.newPage();

      // Desktop
      await page.setViewport({ width: 1366, height: 768 });
      console.log("Navigating to", url);
      await page
        .goto(url, { waitUntil: "networkidle2", timeout: 30000 })
        .catch(() => {});
      await page.waitForTimeout(1000);
      const desktopPath = path.join(OUT_DIR, `${slug}-desktop.png`);
      await page.screenshot({ path: desktopPath, fullPage: true });
      console.log("Saved", desktopPath);

      // Mobile
      await page.setViewport({ width: 375, height: 812, isMobile: true });
      await page
        .reload({ waitUntil: "networkidle2", timeout: 30000 })
        .catch(() => {});
      await page.waitForTimeout(1000);
      const mobilePath = path.join(OUT_DIR, `${slug}-mobile.png`);
      await page.screenshot({ path: mobilePath, fullPage: true });
      console.log("Saved", mobilePath);

      await page.close();
    }
  } finally {
    await browser.close();
  }
  console.log("Screenshots complete");
})().catch((err) => {
  console.error(err);
  process.exit(1);
});
