/**
 * Emotional Logic Engine
 * Maps ripple patterns to emotional states and generates affective reasoning
 * 
 * Interprets patterns through emotional dimensions: valence, arousal, resonance
 */

class EmotionalLogicEngine {
  constructor(config = {}) {
    this.emotions = new Map();
    this.stateHistory = [];
    this.resonanceThreshold = config.resonanceThreshold || 0.7;
    this.learningMode = config.learningMode !== false;
    
    this._initializeEmotions();
  }

  _initializeEmotions() {
    const emotionDefinitions = [
      { name: 'Joy', valence: 0.9, arousal: 0.7, color: '#FFD700' },
      { name: 'Curiosity', valence: 0.6, arousal: 0.8, color: '#87CEEB' },
      { name: 'Harmony', valence: 0.8, arousal: 0.4, color: '#90EE90' },
      { name: 'Tension', valence: 0.3, arousal: 0.9, color: '#FF6B6B' },
      { name: 'Resolution', valence: 0.85, arousal: 0.3, color: '#98FB98' },
      { name: 'Growth', valence: 0.75, arousal: 0.6, color: '#FFB6C1' },
      { name: 'Integration', valence: 0.8, arousal: 0.5, color: '#DDA0DD' }
    ];

    emotionDefinitions.forEach(emotion => {
      this.emotions.set(emotion.name, {
        ...emotion,
        resonance: 0,
        intensity: 0,
        lastActivation: null
      });
    });
  }

  /**
   * Interpret a ripple pattern as emotional state
   */
  interpretPattern(pattern) {
    if (!pattern.frequency || !pattern.magnitude) {
      return { error: 'Invalid pattern' };
    }

    const valence = this._frequencyToValence(pattern.frequency);
    const arousal = this._magnitudeToArousal(pattern.magnitude);
    const resonance = this._calculateResonance(pattern);

    const emotionalState = {
      timestamp: new Date().toISOString(),
      valence,
      arousal,
      resonance,
      dominantEmotion: this._findDominantEmotion(valence, arousal),
      secondaryEmotions: this._findSecondaryEmotions(valence, arousal),
      intensity: Math.sqrt(arousal * arousal + valence * valence),
      confidence: resonance,
      interpretation: this._generateInterpretation(valence, arousal, resonance)
    };

    this.stateHistory.push(emotionalState);
    
    if (this.learningMode) {
      this._updateEmotionalModel(emotionalState);
    }

    return emotionalState;
  }

  /**
   * Process batch of patterns
   */
  processBatch(patterns) {
    return patterns.map(pattern => this.interpretPattern(pattern));
  }

  /**
   * Detect emotional transitions
   */
  detectTransitions() {
    const transitions = [];
    
    if (this.stateHistory.length < 2) return transitions;

    for (let i = 1; i < this.stateHistory.length; i++) {
      const prev = this.stateHistory[i - 1];
      const curr = this.stateHistory[i];

      const change = {
        from: prev.dominantEmotion,
        to: curr.dominantEmotion,
        valenceChange: curr.valence - prev.valence,
        arousalChange: curr.arousal - prev.arousal,
        resonanceChange: curr.resonance - prev.resonance
      };

      if (change.from !== change.to) {
        transitions.push(change);
      }
    }

    return transitions;
  }

  /**
   * Predict emotional trajectory
   */
  predictTrajectory(steps = 5) {
    if (this.stateHistory.length === 0) {
      return [];
    }

    const current = this.stateHistory[this.stateHistory.length - 1];
    const trajectory = [current];

    for (let i = 0; i < steps; i++) {
      const trend = this._calculateTrend();
      const next = {
        valence: Math.max(0, Math.min(1, current.valence + trend.valenceVelocity)),
        arousal: Math.max(0, Math.min(1, current.arousal + trend.arousalVelocity)),
        resonance: Math.max(0, Math.min(1, current.resonance + trend.resonanceVelocity)),
        dominantEmotion: null,
        timestamp: new Date().toISOString()
      };

      next.dominantEmotion = this._findDominantEmotion(next.valence, next.arousal);
      trajectory.push(next);
    }

    return trajectory;
  }

  /**
   * Get current emotional state
   */
  getCurrentState() {
    if (this.stateHistory.length === 0) {
      return null;
    }
    return this.stateHistory[this.stateHistory.length - 1];
  }

  /**
   * Get emotional statistics
   */
  getStatistics() {
    if (this.stateHistory.length === 0) {
      return null;
    }

    const avgValence = this.stateHistory.reduce((sum, s) => sum + s.valence, 0) / this.stateHistory.length;
    const avgArousal = this.stateHistory.reduce((sum, s) => sum + s.arousal, 0) / this.stateHistory.length;
    const avgResonance = this.stateHistory.reduce((sum, s) => sum + s.resonance, 0) / this.stateHistory.length;

    return {
      averageValence: avgValence,
      averageArousal: avgArousal,
      averageResonance: avgResonance,
      totalStates: this.stateHistory.length,
      emotionalRange: this._calculateRange()
    };
  }

  // Private methods

  _frequencyToValence(frequency) {
    // Map frequency to valence: lower freq = lower valence, higher = higher
    return Math.min(1, frequency / 1000);
  }

  _magnitudeToArousal(magnitude) {
    // Map magnitude to arousal
    return Math.min(1, magnitude);
  }

  _calculateResonance(pattern) {
    // Check how well pattern aligns with known emotional patterns
    let maxAlignment = 0;
    
    this.emotions.forEach(emotion => {
      // Simple alignment based on frequency match
      const freqMatch = 1 - Math.abs(pattern.frequency - 500) / 500;
      maxAlignment = Math.max(maxAlignment, freqMatch);
    });

    return Math.max(this.resonanceThreshold, maxAlignment);
  }

  _findDominantEmotion(valence, arousal) {
    let dominant = null;
    let minDistance = Infinity;

    this.emotions.forEach((emotion, name) => {
      const distance = Math.sqrt(
        Math.pow(valence - emotion.valence, 2) + 
        Math.pow(arousal - emotion.arousal, 2)
      );

      if (distance < minDistance) {
        minDistance = distance;
        dominant = name;
      }
    });

    return dominant;
  }

  _findSecondaryEmotions(valence, arousal, topN = 2) {
    const emotions = [];

    this.emotions.forEach((emotion, name) => {
      const distance = Math.sqrt(
        Math.pow(valence - emotion.valence, 2) + 
        Math.pow(arousal - emotion.arousal, 2)
      );
      emotions.push({ name, distance });
    });

    return emotions.sort((a, b) => a.distance - b.distance).slice(1, topN + 1).map(e => e.name);
  }

  _generateInterpretation(valence, arousal, resonance) {
    let interpretation = '';
    
    if (valence > 0.7) interpretation += 'positive ';
    else if (valence < 0.3) interpretation += 'negative ';
    else interpretation += 'neutral ';

    if (arousal > 0.7) interpretation += 'and energetic';
    else if (arousal < 0.3) interpretation += 'and calm';
    else interpretation += 'and balanced';

    if (resonance < 0.7) interpretation += ' (uncertain match)';

    return interpretation;
  }

  _updateEmotionalModel(state) {
    // Update emotion models based on new state
    const emotion = this.emotions.get(state.dominantEmotion);
    if (emotion) {
      emotion.lastActivation = state.timestamp;
      emotion.resonance = state.resonance;
      emotion.intensity = state.intensity;
    }
  }

  _calculateTrend() {
    if (this.stateHistory.length < 2) {
      return { valenceVelocity: 0, arousalVelocity: 0, resonanceVelocity: 0 };
    }

    const recent = this.stateHistory.slice(-5);
    const valenceVelocity = (recent[recent.length - 1].valence - recent[0].valence) / recent.length;
    const arousalVelocity = (recent[recent.length - 1].arousal - recent[0].arousal) / recent.length;
    const resonanceVelocity = (recent[recent.length - 1].resonance - recent[0].resonance) / recent.length;

    return { valenceVelocity, arousalVelocity, resonanceVelocity };
  }

  _calculateRange() {
    const valences = this.stateHistory.map(s => s.valence);
    const arousals = this.stateHistory.map(s => s.arousal);

    return {
      valenceRange: [Math.min(...valences), Math.max(...valences)],
      arousalRange: [Math.min(...arousals), Math.max(...arousals)]
    };
  }
}

// Export
if (typeof module !== 'undefined' && module.exports) {
  module.exports = EmotionalLogicEngine;
}
