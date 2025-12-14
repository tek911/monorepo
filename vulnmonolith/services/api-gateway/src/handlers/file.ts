import express from 'express';
import { exec, execSync } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';

const router = express.Router();

/**
 * VULNERABILITY: Command Injection
 * User input is directly passed to shell command
 * CWE-78: Improper Neutralization of Special Elements used in an OS Command
 */
router.post('/process', (req, res) => {
    const { filename, operation } = req.body;

    // VULNERABILITY: Command injection via filename
    const command = `convert ${filename} -resize 50% output_${filename}`;

    exec(command, (error, stdout, stderr) => {
        if (error) {
            return res.status(500).json({ error: error.message });
        }
        res.json({ output: stdout });
    });
});

/**
 * VULNERABILITY: Command injection in file operations
 */
router.get('/info', (req, res) => {
    const filename = req.query.file as string;

    // VULNERABILITY: Direct command injection
    const command = `file ${filename} && stat ${filename}`;

    exec(command, (error, stdout) => {
        if (error) {
            return res.status(500).json({ error: error.message });
        }
        res.json({ info: stdout });
    });
});

/**
 * VULNERABILITY: Path traversal
 * CWE-22: Improper Limitation of a Pathname to a Restricted Directory
 */
router.get('/read', (req, res) => {
    const filename = req.query.file as string;

    // VULNERABILITY: No path validation - allows traversal like ../../etc/passwd
    const filePath = path.join('/var/uploads/', filename);

    try {
        const content = fs.readFileSync(filePath, 'utf8');
        res.json({ content });
    } catch (error: any) {
        res.status(500).json({ error: error.message });
    }
});

/**
 * VULNERABILITY: Arbitrary file write via path traversal
 */
router.post('/write', (req, res) => {
    const { filename, content } = req.body;

    // VULNERABILITY: No validation on filename
    const filePath = `/var/uploads/${filename}`;

    try {
        fs.writeFileSync(filePath, content);
        res.json({ success: true });
    } catch (error: any) {
        res.status(500).json({ error: error.message });
    }
});

/**
 * VULNERABILITY: Command injection via execSync
 */
router.post('/archive', (req, res) => {
    const { files, archiveName } = req.body;

    // VULNERABILITY: User input in command
    const command = `tar -czf ${archiveName}.tar.gz ${files.join(' ')}`;

    try {
        execSync(command);
        res.json({ archive: `${archiveName}.tar.gz` });
    } catch (error: any) {
        res.status(500).json({ error: error.message });
    }
});

/**
 * VULNERABILITY: Shell injection via template strings
 */
router.delete('/remove', (req, res) => {
    const filename = req.query.file as string;

    // VULNERABILITY: Backtick injection possible
    exec(`rm -f ${filename}`, (error) => {
        if (error) {
            return res.status(500).json({ error: 'Failed to delete' });
        }
        res.json({ deleted: filename });
    });
});

export { router as fileHandler };
