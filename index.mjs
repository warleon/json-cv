import { promises as fs } from "fs";
import * as theme_onepage_plus from "jsonresume-theme-onepage-plus";
import * as theme_even from "jsonresume-theme-even";
import * as theme_elegant from "jsonresume-theme-elegant";
import * as theme_html from "@warleon/jsonresume-theme-html";
import * as theme_compact from "@warleon/jsonresume-theme-compact"

import puppeteer from "puppeteer";
import { render } from "resumed";
import path from "path";

// Get all JSON files from the resumes directory
const resumesDir = "resumes";
const outputDir = "output";

// Optional CLI arg: name of a specific resume to build (with or without .json extension)
const requestedResume = process.argv[2];

const files = await fs.readdir(resumesDir);
let resumeFiles = files.filter(file => path.extname(file) === '.json');

if (requestedResume) {
  const requestedFile = requestedResume.endsWith('.json') ? requestedResume : `${requestedResume}.json`;
  if (!resumeFiles.includes(requestedFile)) {
    console.error(`✗ Resume not found: ${requestedFile}`);
    process.exit(1);
  }
  resumeFiles = [requestedFile];
}

console.log(`Found ${resumeFiles.length} resume files to process:`);
resumeFiles.forEach(file => console.log(`  - ${file}`));

// Launch browser once for all PDFs
const browser = await puppeteer.launch();

// Process each resume file
for (const resumeFile of resumeFiles) {
  console.log(`\nProcessing ${resumeFile}...`);
  
  try {
    // Read and parse the resume JSON
    const resumePath = path.join(resumesDir, resumeFile);
    const resume = JSON.parse(await fs.readFile(resumePath, "utf-8"));
    
    const theme = theme_compact;
    // Render the resume to HTML
    const html = await render(resume, theme);
    
    // Create PDF
    const page = await browser.newPage();
    await page.setContent(html, { waitUntil: "networkidle0" });
    
    // Generate output filename (replace .json with .pdf)
    const outputFileName = path.basename(resumeFile, '.json') + '.pdf';
    const outputPath = path.join(outputDir, outputFileName);
    
    await page.pdf({
      path: outputPath,
      printBackground: true,
      //width: "210mm", // Custom width equivalent to A4 width (8.27 inches)
      //height: `${await page.evaluate(() => document.body.scrollHeight)}px`, // Set height based on content
      //preferCSSPageSize: true, // Allow CSS to control the page size
      format: "A4",
      margin: {
        top: "5mm",
        right: "5mm",
        bottom: "5mm",
        left: "5mm"
      }
    });
    
    await page.close();
    console.log(`✓ Generated: ${outputPath}`);
  } catch (error) {
    console.error(`✗ Error processing ${resumeFile}:`, error.message);
  }
}

await browser.close();
console.log('\nAll resumes processed!');
