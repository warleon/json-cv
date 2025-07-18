import { promises as fs } from "fs";
import * as theme_onepage_plus from "jsonresume-theme-onepage-plus";
import * as theme_even from "jsonresume-theme-even";
import * as theme_elegant from "jsonresume-theme-elegant";
import puppeteer from "puppeteer";
import { render } from "resumed";
import path from "path";

// Get all JSON files from the resumes directory
const resumesDir = "resumes";
const outputDir = "output";
const files = await fs.readdir(resumesDir);
const resumeFiles = files.filter(file => path.extname(file) === '.json');

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
    
    const theme = theme_elegant;
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
      width: "210mm", // Custom width equivalent to A4 width (8.27 inches)
      height: `${await page.evaluate(() => document.body.scrollHeight)}px`, // Set height based on content
      preferCSSPageSize: true, // Allow CSS to control the page size
    });
    
    await page.close();
    console.log(`✓ Generated: ${outputPath}`);
  } catch (error) {
    console.error(`✗ Error processing ${resumeFile}:`, error.message);
  }
}

await browser.close();
console.log('\nAll resumes processed!');
