/**
 * Ripple Sonar Core
 * Real-time ripple wave detection and analysis engine
 * 
 * Detects and classifies ripple patterns in sensor data
 */

class RippleSonar {
  constructor(config = {}) {
    this.sampleRate = config.sampleRate || 1000; // Hz
    this.bufferSize = config.bufferSize || 2048;
    this.confidenceThreshold = config.confidenceThreshold || 0.85;
    
    this.detections = [];
    this.history = [];
    this.isRunning = false;
  }

  /**
   * Analyze signal for ripple patterns
   * @param {array} signal - Input signal array
   * @returns {object} Detection results
   */
  analyze(signal) {
    if (!signal || signal.length === 0) {
      return { error: 'Invalid signal' };
    }

    const fft = this._performFFT(signal);
    const peaks = this._detectPeaks(fft);
    const ripples = this._classifyRipples(peaks);

    const result = {
      timestamp: new Date().toISOString(),
      signalLength: signal.length,
      frequencyPeaks: peaks,
      detectedRipples: ripples,
      systemEnergy: this._calculateEnergy(signal),
      coherence: this._calculateCoherence(fft),
      confidence: this._calculateConfidence(ripples),
      status: 'analyzed'
    };

    this.history.push(result);
    return result;
  }

  /**
   * Simplified FFT (Fast Fourier Transform) simulation
   */
  _performFFT(signal) {
    // In production, use a real FFT library like fft.js
    // This is a placeholder that simulates frequency domain analysis
    const fft = new Array(signal.length / 2).fill(0);
    
    for (let freq = 0; freq < fft.length; freq++) {
      let real = 0, imag = 0;
      for (let t = 0; t < signal.length; t++) {
        const angle = -2 * Math.PI * freq * t / signal.length;
        real += signal[t] * Math.cos(angle);
        imag += signal[t] * Math.sin(angle);
      }
      fft[freq] = Math.sqrt(real * real + imag * imag);
    }
    
    return fft;
  }

  /**
   * Detect frequency peaks in spectrum
   */
  _detectPeaks(spectrum) {
    const peaks = [];
    const threshold = Math.max(...spectrum) * 0.3;

    for (let i = 1; i < spectrum.length - 1; i++) {
      if (spectrum[i] > spectrum[i - 1] && 
          spectrum[i] > spectrum[i + 1] && 
          spectrum[i] > threshold) {
        peaks.push({
          frequency: (i * this.sampleRate) / spectrum.length,
          magnitude: spectrum[i],
          normalized: spectrum[i] / Math.max(...spectrum)
        });
      }
    }

    return peaks.sort((a, b) => b.magnitude - a.magnitude).slice(0, 10);
  }

  /**
   * Classify detected peaks as ripples
   */
  _classifyRipples(peaks) {
    const ripples = [];
    
    peaks.forEach((peak, index) => {
      const ripple = {
        id: `ripple-${Date.now()}-${index}`,
        frequency: peak.frequency,
        magnitude: peak.magnitude,
        normalized: peak.normalized,
        type: this._classifyByFrequency(peak.frequency),
        harmonicOrder: index + 1,
        intensity: peak.normalized * 100
      };
      ripples.push(ripple);
    });

    return ripples;
  }

  /**
   * Classify ripple by frequency
   */
  _classifyByFrequency(freq) {
    if (freq < 50) return 'subsonic';
    if (freq < 200) return 'low-frequency';
    if (freq < 2000) return 'mid-frequency';
    if (freq < 8000) return 'high-frequency';
    return 'ultrasonic';
  }

  /**
   * Calculate total signal energy
   */
  _calculateEnergy(signal) {
    return signal.reduce((sum, val) => sum + val * val, 0) / signal.length;
  }

  /**
   * Calculate spectral coherence
   */
  _calculateCoherence(spectrum) {
    const max = Math.max(...spectrum);
    const total = spectrum.reduce((a, b) => a + b, 0);
    return max / total;
  }

  /**
   * Calculate overall confidence in detection
   */
  _calculateConfidence(ripples) {
    if (ripples.length === 0) return 0;
    
    const weightedConfidence = ripples
      .slice(0, 3)
      .reduce((sum, ripple) => sum + ripple.normalized, 0) / 3;
    
    return Math.min(0.95, weightedConfidence);
  }

  /**
   * Get recent detections
   */
  getRecentDetections(count = 10) {
    return this.history.slice(-count);
  }

  /**
   * Clear history
   */
  clearHistory() {
    this.history = [];
  }

  /**
   * Get statistics
   */
  getStatistics() {
    return {
      totalAnalyses: this.history.length,
      averageConfidence: this._calculateAverageConfidence(),
      mostCommonType: this._getMostCommonType(),
      lastAnalysis: this.history[this.history.length - 1] || null
    };
  }

  _calculateAverageConfidence() {
    if (this.history.length === 0) return 0;
    return this.history.reduce((sum, h) => sum + h.confidence, 0) / this.history.length;
  }

  _getMostCommonType() {
    const types = new Map();
    this.history.forEach(h => {
      h.detectedRipples.forEach(ripple => {
        types.set(ripple.type, (types.get(ripple.type) || 0) + 1);
      });
    });
    return Array.from(types.entries()).sort((a, b) => b[1] - a[1])[0]?.[0] || 'none';
  }
}

// Export
if (typeof module !== 'undefined' && module.exports) {
  module.exports = RippleSonar;
}
