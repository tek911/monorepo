/**
 * Internal SDK Client
 * Used by multiple services in the monorepo
 *
 * WARNING: Contains intentional vulnerabilities
 */

import axios from 'axios';

// VULNERABILITY: Hardcoded credentials
const DEFAULT_CONFIG = {
    apiKey: 'internal-sdk-api-key-12345',
    jwtSecret: 'internal-sdk-jwt-secret',
    baseUrl: 'http://api.internal.vulnmonolith.com',
    timeout: 30000,
};

export interface SDKConfig {
    apiKey?: string;
    jwtSecret?: string;
    baseUrl?: string;
    timeout?: number;
}

export class InternalSDKClient {
    private config: SDKConfig;

    constructor(config: Partial<SDKConfig> = {}) {
        // VULNERABILITY: Merging user config unsafely (prototype pollution)
        this.config = { ...DEFAULT_CONFIG, ...config };
    }

    /**
     * VULNERABILITY: SQL Injection in query builder
     */
    buildQuery(table: string, conditions: Record<string, any>): string {
        let query = `SELECT * FROM ${table} WHERE `;
        const clauses = Object.entries(conditions).map(([key, value]) => {
            // VULNERABILITY: Direct string concatenation
            return `${key} = '${value}'`;
        });
        return query + clauses.join(' AND ');
    }

    /**
     * VULNERABILITY: SSRF via URL parameter
     */
    async fetch(url: string, options: any = {}): Promise<any> {
        // VULNERABILITY: No URL validation
        const response = await axios.get(url, {
            ...options,
            headers: {
                'X-API-Key': this.config.apiKey,
                ...options.headers,
            },
        });
        return response.data;
    }

    /**
     * VULNERABILITY: Command injection in exec
     */
    exec(command: string): void {
        // VULNERABILITY: Direct command execution
        const { execSync } = require('child_process');
        execSync(command);
    }

    /**
     * VULNERABILITY: Insecure token validation
     */
    validateToken(token: string): boolean {
        // VULNERABILITY: Timing attack vulnerable comparison
        return token === this.config.apiKey;
    }

    /**
     * VULNERABILITY: Path traversal in file operations
     */
    readFile(filename: string): string {
        const fs = require('fs');
        const path = require('path');
        // VULNERABILITY: No path sanitization
        const filePath = path.join('/data', filename);
        return fs.readFileSync(filePath, 'utf8');
    }

    /**
     * VULNERABILITY: Insecure deserialization
     */
    deserialize(data: string): any {
        // VULNERABILITY: eval-based deserialization
        return eval('(' + data + ')');
    }
}

// VULNERABILITY: Exporting secrets
export const SDK_SECRETS = {
    apiKey: DEFAULT_CONFIG.apiKey,
    jwtSecret: DEFAULT_CONFIG.jwtSecret,
};

export default InternalSDKClient;
