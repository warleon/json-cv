import { promises as fs } from "fs";
import * as theme from "jsonresume-theme-onepage-plus";
import puppeteer from "puppeteer";
import { render } from "resumed";

const resume = JSON.parse(await fs.readFile("resume.json", "utf-8"));
const html = await render(resume, theme);

const browser = await puppeteer.launch();
const page = await browser.newPage();

await page.setContent(html, { waitUntil: "networkidle0" });
await page.pdf({
  path: "resume.pdf",
  printBackground: true,
  width: "210mm", // Custom width equivalent to A4 width (8.27 inches)
  height: `${await page.evaluate(() => document.body.scrollHeight)}px`, // Set height based on content
  preferCSSPageSize: true, // Allow CSS to control the page size
});
await browser.close();
