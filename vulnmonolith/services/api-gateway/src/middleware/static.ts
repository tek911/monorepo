import express from 'express';
import * as fs from 'fs';
import * as path from 'path';

const router = express.Router();

/**
 * VULNERABILITY: Path Traversal in static file serving
 * CWE-22: Improper Limitation of a Pathname to a Restricted Directory
 */
router.get('/*', (req, res) => {
    const requestedPath = req.params[0];

    // VULNERABILITY: Path traversal - no sanitization
    // Attack: /static/../../../etc/passwd
    const filePath = path.join(__dirname, '../../public', requestedPath);

    // VULNERABILITY: Even with path.join, ../ can escape
    // Should use path.resolve and check if result is within allowed directory

    if (fs.existsSync(filePath)) {
        // VULNERABILITY: No content-type validation
        const content = fs.readFileSync(filePath);
        res.send(content);
    } else {
        res.status(404).send('Not found');
    }
});

/**
 * VULNERABILITY: Directory listing enabled
 */
router.get('/list', (req, res) => {
    const dirPath = req.query.dir as string || '.';

    // VULNERABILITY: Arbitrary directory listing
    const fullPath = path.join(__dirname, '../../public', dirPath);

    try {
        const files = fs.readdirSync(fullPath);
        res.json({ files });
    } catch (error: any) {
        res.status(500).json({ error: error.message });
    }
});

/**
 * VULNERABILITY: Symbolic link following
 */
router.get('/follow/:filename', (req, res) => {
    const filename = req.params.filename;
    const filePath = path.join(__dirname, '../../public', filename);

    // VULNERABILITY: Following symlinks without validation
    // Could link to sensitive files outside public directory
    const realPath = fs.realpathSync(filePath);
    const content = fs.readFileSync(realPath, 'utf8');
    res.send(content);
});

export { router as staticMiddleware };
