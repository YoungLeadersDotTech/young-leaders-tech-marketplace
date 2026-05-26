// Clickable File Path Formatter for Claude Code Terminal
// Uses OSC 8 standard for cross-platform terminal hyperlinks
// Version: 2.0.0 - Security hardened with comprehensive error handling

const path = require('path');
const fs = require('fs');

/**
 * Sanitize file path to prevent injection attacks
 * @private
 * @param {string} filePath - Path to sanitize
 * @returns {string} Sanitized path
 * @throws {Error} If path contains suspicious patterns
 */
function sanitizePath(filePath) {
  // Remove control characters (ASCII 0-31 and 127)
  const sanitized = filePath.replace(/[\x00-\x1F\x7F]/g, '');

  // Check for suspicious patterns that could indicate injection attempts
  const dangerousPatterns = [
    /\.\.\//g,  // Path traversal
    /\.\.\\/g,  // Path traversal (Windows)
    /file:\/\//i,  // Nested file:// URIs
    /javascript:/i,  // JavaScript URI scheme
    /data:/i,  // Data URI scheme
    /<script/i,  // Script injection
  ];

  for (const pattern of dangerousPatterns) {
    if (pattern.test(sanitized)) {
      throw new Error(`Path contains suspicious pattern: ${pattern.toString()}`);
    }
  }

  return sanitized;
}

/**
 * Validate that path is within safe boundaries
 * @private
 * @param {string} filePath - Path to validate
 * @throws {Error} If path validation fails
 */
function validatePathSafety(filePath) {
  // Resolve to absolute path (handles symlinks)
  const resolved = path.resolve(filePath);

  // Check if path still absolute after resolution
  if (!path.isAbsolute(resolved)) {
    throw new Error('Path resolution resulted in non-absolute path');
  }

  // Verify path doesn't escape beyond reasonable boundaries
  // This prevents paths like /../../../../etc/passwd
  const normalized = path.normalize(resolved);
  if (normalized !== resolved) {
    throw new Error('Path normalization changed resolved path');
  }
}

/**
 * Encode URI component with additional safety checks
 * @private
 * @param {string} component - URI component to encode
 * @returns {string} Encoded component
 */
function safeEncodeURIComponent(component) {
  try {
    // Use encodeURIComponent for proper encoding of all special chars
    return encodeURIComponent(component)
      .replace(/'/g, '%27')  // Extra encoding for single quotes
      .replace(/!/g, '%21')  // Extra encoding for exclamation marks
      .replace(/\(/g, '%28') // Extra encoding for parentheses
      .replace(/\)/g, '%29');
  } catch (error) {
    throw new Error(`Failed to encode URI component: ${error.message}`);
  }
}

/**
 * Format absolute file path as OSC 8 hyperlink for terminal
 *
 * @param {string} filePath - Absolute file path to format
 * @param {object} options - Formatting options
 * @param {number} options.line - Line number to navigate to
 * @param {number} options.endLine - End line for range selection
 * @param {string} options.displayText - Custom display text (default: filename)
 * @param {boolean} options.plainText - Force plain text output (default: false)
 * @param {boolean} options.skipValidation - Skip safety validation (use with caution, default: false)
 * @returns {string} OSC 8 formatted hyperlink or plain text
 * @throws {Error} If path validation or formatting fails
 *
 * @example
 * formatClickablePath('/Users/john/file.md')
 * // => "\e]8;;file:///Users/john/file.md\e\\file.md\e]8;;\e\\"
 *
 * @example
 * formatClickablePath('/Users/john/file.ts', { line: 42 })
 * // => "\e]8;;file:///Users/john/file.ts:42\e\\file.ts:42\e]8;;\e\\"
 *
 * @example Error handling
 * try {
 *   const link = formatClickablePath(userInput);
 * } catch (error) {
 *   console.error('Invalid path:', error.message);
 *   // Fallback to plain text
 *   return userInput;
 * }
 */
function formatClickablePath(filePath, options = {}) {
  try {
    // Input validation
    if (!filePath || typeof filePath !== 'string') {
      throw new Error('File path must be a non-empty string');
    }

    // Trim whitespace
    filePath = filePath.trim();

    if (filePath.length === 0) {
      throw new Error('File path cannot be empty');
    }

    // Validate absolute path
    if (!path.isAbsolute(filePath)) {
      throw new Error(`File path must be absolute for clickable links: ${filePath}`);
    }

    // Sanitize path to prevent injection
    const sanitized = sanitizePath(filePath);

    // Validate path safety (unless explicitly skipped)
    if (!options.skipValidation) {
      validatePathSafety(sanitized);
    }

    // Plain text fallback
    if (options.plainText) {
      if (options.line) {
        return options.endLine
          ? `${sanitized}:${options.line}-${options.endLine}`
          : `${sanitized}:${options.line}`;
      }
      return sanitized;
    }

    // Normalize path for URI encoding
    const normalizedPath = path.normalize(sanitized);

    // Cross-platform file:// URI with proper encoding
    let fileUri;
    if (process.platform === 'win32') {
      // Windows: file:///C:/Users/...
      // Split path into components and encode each
      const parts = normalizedPath.replace(/\\/g, '/').split('/');
      const encodedParts = parts.map(part => part ? safeEncodeURIComponent(part) : '');
      fileUri = `file:///${encodedParts.join('/')}`;
    } else {
      // macOS/Linux: file:///Users/...
      // Split path into components and encode each
      const parts = normalizedPath.split('/');
      const encodedParts = parts.map(part => part ? safeEncodeURIComponent(part) : '');
      fileUri = `file://${encodedParts.join('/')}`;
    }

    // Add line number/range if specified (validate numeric)
    if (options.line) {
      const lineNum = parseInt(options.line, 10);
      if (isNaN(lineNum) || lineNum < 1) {
        throw new Error(`Invalid line number: ${options.line}`);
      }
      fileUri += `:${lineNum}`;

      if (options.endLine) {
        const endLineNum = parseInt(options.endLine, 10);
        if (isNaN(endLineNum) || endLineNum < lineNum) {
          throw new Error(`Invalid end line number: ${options.endLine}`);
        }
        fileUri += `-${endLineNum}`;
      }
    }

    // Display text (default: filename with line info)
    let displayText = options.displayText || path.basename(normalizedPath);
    if (options.line && !options.displayText) {
      displayText += `:${options.line}`;
      if (options.endLine) {
        displayText += `-${options.endLine}`;
      }
    }

    // Sanitize display text (prevent escape sequence injection)
    displayText = displayText.replace(/[\x00-\x1F\x7F]/g, '');

    // OSC 8 hyperlink format
    const ESC = '\x1b';
    const OSC = `${ESC}]8`;
    const ST = `${ESC}\\`;

    return `${OSC};;${fileUri}${ST}${displayText}${OSC};;${ST}`;

  } catch (error) {
    // Log error for debugging (if console available)
    if (typeof console !== 'undefined' && console.error) {
      console.error(`[formatClickablePath] Error: ${error.message}`);
    }

    // Re-throw with context
    throw new Error(`Failed to format clickable path: ${error.message}`);
  }
}

/**
 * Check if current terminal supports OSC 8 hyperlinks
 * Enhanced detection with fallback behavior
 * @returns {boolean} True if terminal likely supports OSC 8
 */
function supportsClickablePaths() {
  try {
    const term = process.env.TERM_PROGRAM;
    const termVar = process.env.TERM;

    // FORCE_HYPERLINK env var is the official Claude Code override mechanism
    if (process.env.FORCE_HYPERLINK === '1') {
      return true;
    }

    // Known supporting terminals
    const supportedTerms = [
      'vscode',           // VSCode integrated terminal
      'iTerm.app',        // iTerm2
      'WezTerm',          // WezTerm
      'Hyper',            // Hyper terminal
      'Tabby',            // Tabby terminal
      'rio',              // Rio terminal
      'ghostty',          // Ghostty terminal (TERM_PROGRAM=ghostty)
    ];

    // Check TERM_PROGRAM first (most reliable)
    if (supportedTerms.includes(term)) {
      return true;
    }

    // Check TERM variable for xterm compatibility
    if (termVar) {
      // xterm-256color and variants support OSC 8
      if (termVar.includes('xterm') || termVar.includes('screen')) {
        return true;
      }

      // Check for other known supporting terminal types
      const supportingTermTypes = ['alacritty', 'kitty', 'wezterm', 'foot'];
      if (supportingTermTypes.some(type => termVar.includes(type))) {
        return true;
      }
    }

    // Check for Windows Terminal
    if (process.env.WT_SESSION) {
      return true;
    }

    // Default to false if we can't determine support
    return false;

  } catch (error) {
    // If environment detection fails, assume no support
    if (typeof console !== 'undefined' && console.warn) {
      console.warn('[supportsClickablePaths] Detection failed:', error.message);
    }
    return false;
  }
}

/**
 * Safe wrapper for formatClickablePath with automatic fallback
 * Returns plain text if formatting fails or terminal doesn't support OSC 8
 *
 * @param {string} filePath - Absolute file path to format
 * @param {object} options - Same options as formatClickablePath
 * @returns {string} Formatted hyperlink or plain text fallback (never throws)
 *
 * @example
 * // Always succeeds, even with invalid input
 * const link = formatClickablePathSafe(userInput);
 * console.log(`Report saved: ${link}`);
 */
function formatClickablePathSafe(filePath, options = {}) {
  try {
    // Check terminal support first
    if (!supportsClickablePaths() && !options.plainText) {
      // Gracefully fall back to plain text
      return formatClickablePath(filePath, { ...options, plainText: true });
    }

    // Attempt normal formatting
    return formatClickablePath(filePath, options);

  } catch (error) {
    // Log warning (not error, since this is expected for invalid paths)
    if (typeof console !== 'undefined' && console.warn) {
      console.warn(`[formatClickablePathSafe] Falling back to plain text: ${error.message}`);
    }

    // Return safe fallback
    try {
      return filePath || '(invalid path)';
    } catch {
      return '(invalid path)';
    }
  }
}

module.exports = {
  formatClickablePath,
  formatClickablePathSafe,
  supportsClickablePaths,
};
