import express from 'express';
import * as ejs from 'ejs';
import * as pug from 'pug';
import Handlebars from 'handlebars';
import { marked } from 'marked';

const router = express.Router();

/**
 * VULNERABILITY: Server-Side Template Injection (SSTI) via EJS
 * CWE-94: Improper Control of Generation of Code
 */
router.post('/render/ejs', (req, res) => {
    const { template, data } = req.body;

    try {
        // VULNERABILITY: SSTI - user-controlled template
        // Payload: <%= process.mainModule.require('child_process').execSync('id') %>
        const result = ejs.render(template, data);
        res.json({ rendered: result });
    } catch (error: any) {
        res.status(500).json({ error: error.message });
    }
});

/**
 * VULNERABILITY: SSTI via Pug
 */
router.post('/render/pug', (req, res) => {
    const { template, data } = req.body;

    try {
        // VULNERABILITY: SSTI via Pug
        const compiledFunction = pug.compile(template);
        const result = compiledFunction(data);
        res.json({ rendered: result });
    } catch (error: any) {
        res.status(500).json({ error: error.message });
    }
});

/**
 * VULNERABILITY: Prototype pollution via Handlebars
 */
router.post('/render/handlebars', (req, res) => {
    const { template, context } = req.body;

    try {
        // VULNERABILITY: Handlebars with prototype pollution
        const compiled = Handlebars.compile(template);
        const result = compiled(context);
        res.json({ rendered: result });
    } catch (error: any) {
        res.status(500).json({ error: error.message });
    }
});

/**
 * VULNERABILITY: XSS via Markdown rendering
 */
router.post('/render/markdown', (req, res) => {
    const { content } = req.body;

    try {
        // VULNERABILITY: Markdown to HTML without sanitization
        // Payload: <script>alert(1)</script> or [link](javascript:alert(1))
        const html = marked(content);
        res.json({ html });
    } catch (error: any) {
        res.status(500).json({ error: error.message });
    }
});

/**
 * VULNERABILITY: Dynamic template path
 */
router.get('/load', (req, res) => {
    const templateName = req.query.name as string;

    try {
        // VULNERABILITY: Path traversal in template loading
        const templatePath = `./templates/${templateName}.ejs`;
        const result = ejs.renderFile(templatePath, { user: 'guest' });
        res.json({ rendered: result });
    } catch (error: any) {
        res.status(500).json({ error: error.message });
    }
});

export { router as templateHandler };
