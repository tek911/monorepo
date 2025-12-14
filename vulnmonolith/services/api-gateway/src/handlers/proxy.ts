import express from 'express';
import axios from 'axios';
import * as http from 'http';

const router = express.Router();

/**
 * VULNERABILITY: Open Proxy
 * Allows proxying requests to any destination
 */
router.all('/forward', async (req, res) => {
    const targetUrl = req.query.target as string || req.body.target;
    const method = req.method.toLowerCase();

    try {
        // VULNERABILITY: Open proxy to any URL
        const response = await axios({
            method,
            url: targetUrl,
            data: req.body.data,
            headers: {
                ...req.headers,
                host: new URL(targetUrl).host
            }
        });

        res.status(response.status).json(response.data);
    } catch (error: any) {
        res.status(500).json({ error: error.message });
    }
});

/**
 * VULNERABILITY: HTTP Header Injection
 * CWE-113: Improper Neutralization of CRLF Sequences in HTTP Headers
 */
router.get('/header-proxy', (req, res) => {
    const customHeader = req.query.header as string;

    // VULNERABILITY: CRLF injection in headers
    res.setHeader('X-Custom-Header', customHeader);
    res.json({ success: true });
});

/**
 * VULNERABILITY: Response splitting via header injection
 */
router.get('/redirect', (req, res) => {
    const location = req.query.url as string;

    // VULNERABILITY: Open redirect + header injection
    res.redirect(location);
});

/**
 * VULNERABILITY: HTTP Request Smuggling potential
 */
router.post('/smuggle', (req, res) => {
    const { target, rawRequest } = req.body;

    // VULNERABILITY: Forwarding raw HTTP requests
    const options = {
        hostname: new URL(target).hostname,
        port: 80,
        path: '/',
        method: 'POST',
        headers: {
            'Content-Length': rawRequest.length
        }
    };

    const proxyReq = http.request(options, (proxyRes) => {
        let data = '';
        proxyRes.on('data', (chunk) => { data += chunk; });
        proxyRes.on('end', () => {
            res.json({ response: data });
        });
    });

    proxyReq.write(rawRequest);
    proxyReq.end();
});

export { router as proxyHandler };
