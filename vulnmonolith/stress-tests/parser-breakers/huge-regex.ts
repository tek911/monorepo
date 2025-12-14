// Huge regex patterns that may cause ReDoS or parser issues
// WARNING: These patterns are intentionally problematic

// VULNERABILITY: ReDoS - Exponential backtracking
export const emailRegexVulnerable = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;

// VULNERABILITY: ReDoS - Nested quantifiers
export const nestedQuantifiers = /^(a+)+$/;
export const nestedQuantifiers2 = /^((a+b)+c)+$/;
export const nestedQuantifiers3 = /^(([a-z])+)+$/;

// Extremely long regex pattern (stress test for parser)
export const hugePattern = new RegExp(
  "^" +
  "(?:" +
    "(?:https?|ftp):\\/\\/" +
    "(?:" +
      "(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?\\.)*" +
      "[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?" +
      "|" +
      "(?:\\d{1,3}\\.){3}\\d{1,3}" +
      "|" +
      "\\[(?:(?:(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4})|(?:(?:[0-9a-fA-F]{1,4}:){6}:[0-9a-fA-F]{1,4})|(?:(?:[0-9a-fA-F]{1,4}:){5}:(?:[0-9a-fA-F]{1,4}:)?[0-9a-fA-F]{1,4})|(?:(?:[0-9a-fA-F]{1,4}:){4}:(?:[0-9a-fA-F]{1,4}:){0,2}[0-9a-fA-F]{1,4})|(?:(?:[0-9a-fA-F]{1,4}:){3}:(?:[0-9a-fA-F]{1,4}:){0,3}[0-9a-fA-F]{1,4})|(?:(?:[0-9a-fA-F]{1,4}:){2}:(?:[0-9a-fA-F]{1,4}:){0,4}[0-9a-fA-F]{1,4})|(?:(?:[0-9a-fA-F]{1,4}:){1}:(?:[0-9a-fA-F]{1,4}:){0,5}[0-9a-fA-F]{1,4})|(?:::(?:[0-9a-fA-F]{1,4}:){0,6}[0-9a-fA-F]{1,4})|(?:(?:[0-9a-fA-F]{1,4}:){1,7}:))\\]" +
    ")" +
    "(?::\\d{1,5})?" +
    "(?:" +
      "\\/(?:[\\w\\-\\.~:/?#\\[\\]@!$&'()*+,;=%]|%[0-9a-fA-F]{2})*" +
    ")?" +
  ")" +
  "$",
  "i"
);

// VULNERABILITY: ReDoS patterns used for input validation
export const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

// ReDoS vulnerable HTML tag matching
export const htmlTagRegex = /<([a-z]+)([^<]+)*(?:>(.*)<\/\1>|\s+\/>)/gi;

// ReDoS vulnerable JSON-like matching
export const jsonLikeRegex = /^\{[\s\S]*\}$/;

// Very complex lookahead/lookbehind patterns
export const complexLookahead = /(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[^A-Za-z0-9])(?!.*\s).{12,}/;
export const complexLookbehind = /(?<=\$)\d+(?:\.\d{2})?(?=\s|$)/g;

// Deeply nested groups
export const deeplyNestedGroups = /((((((((((a+)+)+)+)+)+)+)+)+)+)+/;

// Alternation explosion
export const alternationExplosion = /(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)+/i;

// Catastrophic backtracking patterns
export const catastrophic1 = /^(a|a)+$/;
export const catastrophic2 = /^(a|aa)+$/;
export const catastrophic3 = /^(a|a?)+$/;
export const catastrophic4 = /^(a*)*$/;
export const catastrophic5 = /^(a*)+$/;

// Complex email validation (vulnerable to ReDoS)
export const complexEmailRegex = new RegExp(
  "^" +
  "(?:" +
    "[a-z0-9!#$%&'*+/=?^_`{|}~-]+" +
    "(?:\\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*" +
    "|" +
    '"(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21\\x23-\\x5b\\x5d-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])*"' +
  ")" +
  "@" +
  "(?:" +
    "(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)*[a-z0-9](?:[a-z0-9-]*[a-z0-9])?" +
    "|" +
    "\\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21-\\x5a\\x53-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])+)\\]" +
  ")" +
  "$",
  "i"
);

// Function that uses vulnerable regex
export function validateEmail(email: string): boolean {
  // VULNERABILITY: ReDoS in email validation
  return emailRegexVulnerable.test(email);
}

// VULNERABILITY: SQL injection combined with regex
export function searchWithRegex(pattern: string, table: string): string {
  // User input directly in regex and SQL
  const regex = new RegExp(pattern);
  return `SELECT * FROM ${table} WHERE content REGEXP '${pattern}'`;
}

// Configuration with secrets
const config = {
  apiKey: "sk_live_FAKEFAKEFAKEFAKE_NOTREALxx",
  jwtSecret: "jwt-secret-for-signing-tokens",
};

export default { config };
