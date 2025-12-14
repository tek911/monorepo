import express from 'express';
import axios from 'axios';
import fetch from 'node-fetch';
import { URL } from 'url';

const router = express.Router();

/**
 * VULNERABILITY: Server-Side Request Forgery (SSRF)
 * CWE-918: Server-Side Request Forgery
 * User-controlled URL is fetched without validation
 */
router.get('/fetch', async (req, res) => {
    const url = req.query.url as string;

    try {
        // VULNERABILITY: SSRF - no URL validation
        // Attacker can access internal services: http://169.254.169.254/latest/meta-data/
        const response = await axios.get(url);
        res.json({ data: response.data });
    } catch (error: any) {
        res.status(500).json({ error: error.message });
    }
});

/**
 * VULNERABILITY: SSRF with POST method
 */
router.post('/webhook', async (req, res) => {
    const { url, payload } = req.body;

    try {
        // VULNERABILITY: SSRF via POST
        const response = await axios.post(url, payload);
        res.json({ response: response.data });
    } catch (error: any) {
        res.status(500).json({ error: error.message });
    }
});

/**
 * VULNERABILITY: SSRF via node-fetch
 */
router.get('/image', async (req, res) => {
    const imageUrl = req.query.src as string;

    try {
        // VULNERABILITY: SSRF - fetching arbitrary URLs
        const response = await fetch(imageUrl);
        const buffer = await response.buffer();

        res.set('Content-Type', response.headers.get('content-type') || 'image/png');
        res.send(buffer);
    } catch (error: any) {
        res.status(500).json({ error: error.message });
    }
});

/**
 * VULNERABILITY: Bypass attempt with URL validation that's insufficient
 */
router.get('/safe-fetch', async (req, res) => {
    const url = req.query.url as string;

    try {
        const parsed = new URL(url);

        // VULNERABILITY: Insufficient validation
        // Can be bypassed with: http://localhost@evil.com, http://127.0.0.1.nip.io
        if (parsed.hostname === 'localhost' || parsed.hostname === '127.0.0.1') {
            return res.status(400).json({ error: 'Invalid URL' });
        }

        const response = await axios.get(url);
        res.json({ data: response.data });
    } catch (error: any) {
        res.status(500).json({ error: error.message });
    }
});

/**
 * VULNERABILITY: SSRF via redirect following
 */
router.get('/follow', async (req, res) => {
    const url = req.query.url as string;

    try {
        // VULNERABILITY: Following redirects can lead to internal resources
        const response = await axios.get(url, {
            maxRedirects: 10 // Follows redirects to potentially internal URLs
        });
        res.json({ data: response.data });
    } catch (error: any) {
        res.status(500).json({ error: error.message });
    }
});

/**
 * VULNERABILITY: DNS rebinding vulnerable
 */
router.get('/dns-check', async (req, res) => {
    const url = req.query.url as string;

    try {
        const parsed = new URL(url);

        // First DNS lookup (might resolve to safe IP)
        // Second lookup during fetch (might resolve to internal IP)
        // VULNERABILITY: DNS rebinding attack possible

        const response = await axios.get(url, { timeout: 5000 });
        res.json({ data: response.data });
    } catch (error: any) {
        res.status(500).json({ error: error.message });
    }
});

export { router as previewHandler };
