// Unicode chaos - testing parser handling of unusual characters
// WARNING: Contains intentional vulnerabilities hidden in unicode

// Unicode identifiers
const π = 3.14159;
const 你好 = "hello";
const مرحبا = "marhaba";
const Δ = 0.001;
const ℝ = "real numbers";
const ∞ = Infinity;

// Zero-width characters (invisible but present)
const pass​word = "secret123"; // Zero-width space in variable name
const api_​key = "sk_live_xxxx"; // Zero-width space in variable name

// Homoglyph attack - these look like normal ASCII but aren't
const раssword = "cyrillic_p_secret"; // 'р' is Cyrillic, not Latin 'p'
const pаssword = "cyrillic_a_secret"; // 'а' is Cyrillic, not Latin 'a'

// Right-to-left override (can hide malicious code)
const normal = "user"; // Normal
const ‮malicious = "resu"; // RLO character at start

// Combining characters
const café = "coffee shop";
const café = "coffee shop"; // Same word, different encoding (e + combining acute)

// Emoji identifiers (valid in some JS engines)
const 🔑 = "api_key_value";
const 🔒 = "encrypted_secret";

// Mathematical symbols
const ∑ = (arr) => arr.reduce((a, b) => a + b, 0);
const ∏ = (arr) => arr.reduce((a, b) => a * b, 1);

// Confusing strings with special unicode
const confusingStrings = {
    // Line separator (U+2028)
    lineSep: "line1 line2",
    // Paragraph separator (U+2029)
    paraSep: "para1 para2",
    // Non-breaking space
    nbsp: "word word",
    // En space, em space, etc.
    enSpace: "word word",
    emSpace: "word word",
    // Mongolian vowel separator
    mvs: "word᠎word",
};

// SQL injection with unicode normalization bypass
const userInput = "admin'--";
const normalizedInput = "admin\u0027--"; // Unicode escape for apostrophe

// XSS with unicode
const xssPayload = "\u003cscript\u003ealert(1)\u003c/script\u003e";

// VULNERABILITY: Hidden in unicode
const config = {
    // Normal looking but with hidden characters
    database: "localhost",
    username: "admin",
    // Hidden zero-width characters make this hard to find
    pass​word: "Sup​er​Sec​ret​123", // Zero-width spaces embedded
};

// Function with unicode in name
function 计算(数字) {
    return 数字 * 2;
}

// Arrow function with unicode
const λ = x => x * x;
const ƒ = (x, y) => x + y;

// Object with unicode keys
const unicodeObj = {
    "🔐": "secret_key",
    "键": "chinese_key",
    "مفتاح": "arabic_key",
    "\u200B": "zero_width_key", // Invisible key!
};

// Template literal with unicode
const template = `
    Username: ${config.username}
    Password: ${config.pass​word}
    API Key: ${🔑}
`;

// Regular expression with unicode
const unicodeRegex = /[\u{1F600}-\u{1F64F}]/gu; // Emoji range
const rtlRegex = /[\u0600-\u06FF]/; // Arabic range

// VULNERABILITY: Eval with unicode bypass
const evalPayload = "\u0065\u0076\u0061\u006c"; // "eval" in unicode escapes
// globalThis[evalPayload]("alert(1)"); // Would execute eval

// Export with unicode
export { π, 你好, config, unicodeObj };
export default { 🔑, 🔒, λ, ƒ };
