/**
 * VULNERABILITY: ReDoS (Regular Expression Denial of Service)
 * CWE-1333: Inefficient Regular Expression Complexity
 */

/**
 * VULNERABLE: Email regex with catastrophic backtracking
 */
export function validateEmail(email: string): boolean {
    // VULNERABILITY: ReDoS - exponential backtracking
    // Attack input: "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa!"
    const emailRegex = /^([a-zA-Z0-9]+)+@[a-zA-Z0-9]+\.[a-zA-Z]+$/;
    return emailRegex.test(email);
}

/**
 * VULNERABLE: Another ReDoS pattern
 */
export function validateEmailExtended(email: string): boolean {
    // VULNERABILITY: Nested quantifiers cause exponential time
    const regex = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    return regex.test(email);
}

/**
 * VULNERABLE: URL validation with ReDoS
 */
export function validateUrl(url: string): boolean {
    // VULNERABILITY: ReDoS in URL validation
    const urlRegex = /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/;
    return urlRegex.test(url);
}

/**
 * VULNERABLE: Complex regex for parsing
 */
export function parseComplexInput(input: string): boolean {
    // VULNERABILITY: Multiple nested groups
    const regex = /^((ab)*)+$/;
    return regex.test(input);
}

/**
 * VULNERABLE: HTML tag matching with ReDoS
 */
export function extractTags(html: string): string[] | null {
    // VULNERABILITY: Backtracking on malformed HTML
    const tagRegex = /<([a-z]+)([^<]+)*(?:>(.*)<\/\1>|\s+\/>)/gi;
    return html.match(tagRegex);
}

/**
 * VULNERABLE: JSON-like validation
 */
export function validateJsonLike(input: string): boolean {
    // VULNERABILITY: Catastrophic backtracking
    const regex = /^\{[\s\S]*\}$/;
    return regex.test(input);
}

/**
 * VULNERABLE: Path validation
 */
export function validatePath(path: string): boolean {
    // VULNERABILITY: ReDoS on deeply nested paths
    const pathRegex = /^([\/\w\-\.]+)*$/;
    return pathRegex.test(path);
}

/**
 * Safe alternative (for reference)
 */
export function validateEmailSafe(email: string): boolean {
    // Simple, linear-time email validation
    const parts = email.split('@');
    if (parts.length !== 2) return false;
    if (parts[0].length === 0 || parts[1].length === 0) return false;
    if (!parts[1].includes('.')) return false;
    return true;
}
