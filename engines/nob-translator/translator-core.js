/**
 * NOB Translator Core
 * n(z) Cross-Domain Translation Engine
 * 
 * Translates patterns and concepts between different semantic domains
 */

class NOBTranslator {
  constructor(codexPath = '../codex/codex-index.json') {
    this.codexPath = codexPath;
    this.translations = new Map();
    this.domains = new Set();
    this.initialize();
  }

  initialize() {
    console.log('NOB Translator initialized');
    this.domains.add('harmonic');
    this.domains.add('emotional');
    this.domains.add('conceptual');
    this.domains.add('mathematical');
    this.domains.add('symbolic');
  }

  /**
   * Translate a concept from one domain to another
   * @param {string} concept - The concept to translate
   * @param {string} fromDomain - Source domain
   * @param {string} toDomain - Target domain
   * @returns {object} Translation result with confidence score
   */
  translate(concept, fromDomain, toDomain) {
    if (!this.domains.has(fromDomain) || !this.domains.has(toDomain)) {
      throw new Error(`Invalid domain. Valid domains: ${Array.from(this.domains).join(', ')}`);
    }

    const translationKey = `${concept}:${fromDomain}→${toDomain}`;
    
    if (this.translations.has(translationKey)) {
      return this.translations.get(translationKey);
    }

    const result = this._performTranslation(concept, fromDomain, toDomain);
    this.translations.set(translationKey, result);
    return result;
  }

  /**
   * Core translation algorithm
   */
  _performTranslation(concept, fromDomain, toDomain) {
    const baseConfidence = 0.85;
    
    const mappings = {
      'harmonic→emotional': {
        'frequency': 'resonance',
        'amplitude': 'intensity',
        'phase': 'synchronization',
        'decay': 'dissipation'
      },
      'emotional→symbolic': {
        'joy': '⟡',
        'harmony': '◈',
        'tension': '✕',
        'growth': '↗'
      },
      'conceptual→mathematical': {
        'pattern': 'function',
        'relationship': 'operator',
        'hierarchy': 'tree',
        'network': 'graph'
      }
    };

    const key = `${fromDomain}→${toDomain}`;
    const mapping = mappings[key] || {};
    
    return {
      original: concept,
      translated: mapping[concept] || `[${concept} in ${toDomain}]`,
      fromDomain: fromDomain,
      toDomain: toDomain,
      confidence: baseConfidence,
      timestamp: new Date().toISOString()
    };
  }

  /**
   * Batch translate multiple concepts
   */
  batchTranslate(concepts, fromDomain, toDomain) {
    return concepts.map(concept => 
      this.translate(concept, fromDomain, toDomain)
    );
  }

  /**
   * Get available domains
   */
  getAvailableDomains() {
    return Array.from(this.domains);
  }

  /**
   * Add custom domain
   */
  addDomain(domainName) {
    this.domains.add(domainName);
  }
}

// Export for Node.js/ES modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = NOBTranslator;
}
