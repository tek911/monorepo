# Stress Tests

This directory contains files designed to stress-test security scanner parsers and performance.

## Purpose

Evaluate scanner robustness when handling:
- Malformed but syntactically valid code
- Extremely large files
- Unusual encodings and edge cases
- Resource-intensive patterns

## Structure

### parser-breakers/
Files designed to crash or confuse parsers:
- `deeply-nested.json` - 1000 levels of nesting
- `long-lines.py` - Single lines with 50,000+ characters
- `unicode-chaos.js` - Unusual Unicode in identifiers
- `mixed-encoding.php` - UTF-8/Latin-1 mixed encoding
- `ambiguous-syntax.java` - Valid but confusing constructs
- `huge-regex.ts` - Massive regex patterns
- `circular-imports/` - Import cycles
- `binary-with-code-ext.java` - Binary data with code extension

### scale-tests/
Large files to test performance:
- `massive-class.java` - 50,000+ line single class
- `huge-config.yaml` - 100,000+ line configuration
- `giant-json.json` - 10MB+ JSON file
- `thousand-functions.py` - 1000 functions in single file
- `many-files/` - Directory with 10,000+ small files

### encoding-edge-cases/
Encoding and filename challenges:
- Files with spaces in names
- Unicode filenames
- Special character filenames
- BOM markers (UTF-8, UTF-16)
- Mixed line endings (CRLF/LF in same file)
- Null bytes in content
- Maximum length filenames (255 characters)

## Expected Scanner Behavior

### parser-breakers/
| File | Expected Behavior |
|------|-------------------|
| deeply-nested.json | Should handle gracefully, not stack overflow |
| long-lines.py | Should scan without memory issues |
| unicode-chaos.js | Should parse correctly or skip gracefully |
| binary-with-code-ext.java | Should detect binary and skip |

### scale-tests/
| Test | Acceptable Behavior |
|------|---------------------|
| 50K line file | Complete scan < 60 seconds |
| 10MB JSON | Complete or graceful skip |
| 10K files directory | Complete scan < 5 minutes |

### encoding-edge-cases/
| Case | Expected Behavior |
|------|-------------------|
| Unicode filenames | Should process or skip with warning |
| Mixed encodings | Should detect and handle appropriately |
| BOM markers | Should not affect parsing |

## Scanner Failure Modes

Common failures to look for:
1. **Stack Overflow**: Deep nesting causes recursion issues
2. **Memory Exhaustion**: Large files cause OOM
3. **Infinite Loops**: Circular imports cause hangs
4. **Encoding Errors**: Non-UTF8 causes crashes
5. **Timeout**: Large files cause scan timeouts
6. **Silent Failures**: Files skipped without notification
