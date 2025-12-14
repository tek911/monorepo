import _ from 'lodash';

/**
 * VULNERABILITY: Prototype Pollution
 * CWE-1321: Improperly Controlled Modification of Object Prototype Attributes
 */

/**
 * Recursive object merge vulnerable to prototype pollution
 */
export function unsafeMerge(target: any, source: any): any {
    // VULNERABILITY: Prototype pollution via __proto__
    // Payload: { "__proto__": { "isAdmin": true } }
    for (const key in source) {
        if (typeof source[key] === 'object' && source[key] !== null) {
            if (!target[key]) {
                target[key] = {};
            }
            unsafeMerge(target[key], source[key]);
        } else {
            target[key] = source[key];
        }
    }
    return target;
}

/**
 * VULNERABILITY: Using vulnerable lodash.merge
 */
export function lodashMerge(target: any, source: any): any {
    // VULNERABILITY: lodash 4.17.15 merge is vulnerable to prototype pollution
    return _.merge(target, source);
}

/**
 * VULNERABILITY: Deep clone with prototype pollution
 */
export function deepClone(obj: any): any {
    // VULNERABILITY: Can pollute Object.prototype
    if (typeof obj !== 'object' || obj === null) {
        return obj;
    }

    const clone: any = Array.isArray(obj) ? [] : {};

    for (const key in obj) {
        // VULNERABILITY: No check for __proto__ or constructor
        clone[key] = deepClone(obj[key]);
    }

    return clone;
}

/**
 * VULNERABILITY: Object.assign with user input
 */
export function assignConfig(baseConfig: any, userConfig: any): any {
    // VULNERABILITY: User-controlled keys can include __proto__
    return Object.assign({}, baseConfig, userConfig);
}

/**
 * VULNERABILITY: JSON.parse without prototype pollution protection
 */
export function parseUserJson(jsonString: string): any {
    // VULNERABILITY: Parsed object can contain __proto__
    const parsed = JSON.parse(jsonString);

    // Then merged unsafely
    const config = {};
    unsafeMerge(config, parsed);

    return config;
}

/**
 * VULNERABILITY: Setting nested properties via string path
 */
export function setPath(obj: any, path: string, value: any): void {
    // VULNERABILITY: Path can be "__proto__.polluted"
    const keys = path.split('.');
    let current = obj;

    for (let i = 0; i < keys.length - 1; i++) {
        const key = keys[i];
        if (!current[key]) {
            current[key] = {};
        }
        current = current[key];
    }

    current[keys[keys.length - 1]] = value;
}
