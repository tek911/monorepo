/**
 * XSS Test Vectors
 * INTENTIONAL vulnerabilities for testing security controls.
 * These should be excluded from security scan results.
 */

// XSS test payloads for security testing
const XSS_PAYLOADS = [
  '<script>alert("XSS")</script>',
  '<img src=x onerror=alert("XSS")>',
  '<svg onload=alert("XSS")>',
  '"><script>alert("XSS")</script>',
  "javascript:alert('XSS')",
  '<body onload=alert("XSS")>',
  '<iframe src="javascript:alert(\'XSS\')">',
  '<input onfocus=alert("XSS") autofocus>',
  "'-alert('XSS')-'",
  '{{constructor.constructor("alert(1)")()}}',
];

// DOM XSS test payloads
const DOM_XSS_PAYLOADS = [
  '#<script>alert(1)</script>',
  '?name=<script>alert(1)</script>',
  'javascript:alert(document.domain)',
];

/**
 * INTENTIONALLY VULNERABLE: Renders user input without sanitization.
 * Used to test XSS prevention middleware.
 */
function vulnerableRender(userInput) {
  // INTENTIONAL XSS VULNERABILITY
  document.getElementById('output').innerHTML = userInput;
}

/**
 * INTENTIONALLY VULNERABLE: Creates elements from user input.
 */
function vulnerableElementCreation(tagName, content) {
  // INTENTIONAL DOM manipulation vulnerability
  const element = document.createElement(tagName);
  element.innerHTML = content;
  return element;
}

/**
 * INTENTIONALLY VULNERABLE: Evaluates user input.
 */
function vulnerableEval(userCode) {
  // INTENTIONAL code execution vulnerability
  return eval(userCode);
}

/**
 * Test helper to inject XSS payloads.
 * WARNING: Only use in isolated test environments.
 */
class XSSTestHelper {
  static injectPayload(payload) {
    // INTENTIONAL - for testing CSP and sanitization
    const script = document.createElement('script');
    script.textContent = payload;
    document.body.appendChild(script);
  }

  static testDOMXSS(payload) {
    // INTENTIONAL - tests DOM-based XSS
    location.hash = payload;
    return document.location.hash;
  }
}

module.exports = {
  XSS_PAYLOADS,
  DOM_XSS_PAYLOADS,
  vulnerableRender,
  vulnerableElementCreation,
  vulnerableEval,
  XSSTestHelper,
};
