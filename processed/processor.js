const fs = require('fs').promises;
const path = require('path');
const { extractSections } = require('./utils');

async function processMarkdownFiles() {
    // Define the directory path relative to this script
    const directoryPath = path.join(__dirname, 'md');

    try {
        console.log(`Reading files from: ${directoryPath}`);

        // Read the directory contents
        const files = await fs.readdir(directoryPath);

        // Filter for markdown files
        var mdFiles = files.filter(file => path.extname(file).toLowerCase() === '.md');
        if (mdFiles.length === 0) {
            console.log('No markdown files found in the directory.');
            return;
        }

        console.log(`Found ${mdFiles.length} markdown files.\n`);

        // Iterate and read each file
        for (const file of mdFiles) {
            const filePath = path.join(directoryPath, file);
            try {
                const content = await fs.readFile(filePath, 'utf8');
                const sections = extractSections(content);
                // save as json
                await fs.writeFile(path.join(__dirname, 'json', 'marker', file.replace('.md', '.json')), JSON.stringify(sections));
            } catch (err) {
                console.error(`Error reading file ${file}:`, err.message);
            }
        }

    } catch (err) {
        console.error('Error accessing directory:', err.message);
    }
}

// Execute the function
processMarkdownFiles();
