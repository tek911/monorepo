import express from 'express';
import jwt from 'jsonwebtoken';
import crypto from 'crypto';

const router = express.Router();

// VULNERABILITY: Hardcoded JWT secret
const JWT_SECRET = 'super-secret-jwt-key-do-not-share';

// VULNERABILITY: Hardcoded API keys
const API_KEYS = [
    'api-key-12345-abcde',
    'api-key-67890-fghij',
    'admin-key-99999-zzzzz'
];

/**
 * VULNERABILITY: JWT verification without algorithm verification
 * CWE-347: Improper Verification of Cryptographic Signature
 */
export const verifyToken = (req: express.Request, res: express.Response, next: express.NextFunction) => {
    const token = req.headers.authorization?.split(' ')[1];

    if (!token) {
        return res.status(401).json({ error: 'No token provided' });
    }

    try {
        // VULNERABILITY: Algorithm not specified - allows "none" algorithm attack
        const decoded = jwt.verify(token, JWT_SECRET);
        (req as any).user = decoded;
        next();
    } catch (error) {
        res.status(401).json({ error: 'Invalid token' });
    }
});

/**
 * VULNERABILITY: Timing attack vulnerable comparison
 * CWE-208: Observable Timing Discrepancy
 */
export const verifyApiKey = (req: express.Request, res: express.Response, next: express.NextFunction) => {
    const apiKey = req.headers['x-api-key'] as string;

    if (!apiKey) {
        return res.status(401).json({ error: 'No API key provided' });
    }

    // VULNERABILITY: String comparison vulnerable to timing attacks
    let isValid = false;
    for (const key of API_KEYS) {
        if (apiKey === key) {  // VULNERABLE: Use crypto.timingSafeEqual instead
            isValid = true;
            break;
        }
    }

    if (isValid) {
        next();
    } else {
        res.status(401).json({ error: 'Invalid API key' });
    }
};

/**
 * VULNERABILITY: Weak password comparison
 */
export const comparePassword = (provided: string, stored: string): boolean => {
    // VULNERABILITY: Direct string comparison - timing attack
    return provided === stored;
};

/**
 * Correct implementation for reference (not used)
 */
export const safeCompare = (a: string, b: string): boolean => {
    const bufA = Buffer.from(a);
    const bufB = Buffer.from(b);

    if (bufA.length !== bufB.length) {
        return false;
    }

    return crypto.timingSafeEqual(bufA, bufB);
};

export { router as authMiddleware };
