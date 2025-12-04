/**
 * Attractor Field Mapping (AFM) Core
 * Maps and visualizes attractor states in pattern space
 * 
 * Used for detecting stable pattern configurations and bifurcation points
 */

class AFMCore {
  constructor(config = {}) {
    this.dimensions = config.dimensions || 3;
    this.resolution = config.resolution || 100;
    this.attractors = new Map();
    this.fieldStrength = config.fieldStrength || 1.0;
  }

  /**
   * Add an attractor point
   */
  addAttractor(id, position, strength = 1.0, type = 'standard') {
    this.attractors.set(id, {
      id,
      position,
      strength,
      type,
      created: new Date().toISOString(),
      visited: 0
    });
  }

  /**
   * Calculate field strength at a point
   */
  getFieldStrengthAt(point) {
    let totalForce = 0;
    
    this.attractors.forEach(attractor => {
      const distance = this._euclideanDistance(point, attractor.position);
      if (distance > 0.001) {
        const force = (attractor.strength * this.fieldStrength) / (distance * distance);
        totalForce += force;
      }
    });

    return totalForce;
  }

  /**
   * Calculate field vector at a point
   */
  getFieldVectorAt(point) {
    const vector = new Array(this.dimensions).fill(0);
    
    this.attractors.forEach(attractor => {
      const distance = this._euclideanDistance(point, attractor.position);
      if (distance > 0.001) {
        const magnitude = (attractor.strength * this.fieldStrength) / (distance * distance);
        
        for (let i = 0; i < this.dimensions; i++) {
          const direction = attractor.position[i] - point[i];
          vector[i] += magnitude * direction / distance;
        }
      }
    });

    return vector;
  }

  /**
   * Trace a trajectory from starting point
   */
  traceTrajectory(startPoint, steps = 100, stepSize = 0.01) {
    const trajectory = [startPoint];
    let current = [...startPoint];

    for (let i = 0; i < steps; i++) {
      const vector = this.getFieldVectorAt(current);
      const magnitude = Math.sqrt(vector.reduce((sum, v) => sum + v * v, 0));
      
      if (magnitude < 0.001) break; // Converged to attractor

      for (let j = 0; j < this.dimensions; j++) {
        current[j] += (vector[j] / magnitude) * stepSize;
      }
      
      trajectory.push([...current]);
    }

    return trajectory;
  }

  /**
   * Find nearest attractor to a point
   */
  findNearestAttractor(point) {
    let nearest = null;
    let minDistance = Infinity;

    this.attractors.forEach(attractor => {
      const distance = this._euclideanDistance(point, attractor.position);
      if (distance < minDistance) {
        minDistance = distance;
        nearest = { ...attractor, distance };
      }
    });

    return nearest;
  }

  /**
   * Detect bifurcation points (where field behavior changes)
   */
  detectBifurcationPoints() {
    const bifurcations = [];
    
    // Sample the field and look for discontinuities
    const samples = this._generateSamplePoints(10);
    
    for (let i = 0; i < samples.length - 1; i++) {
      const field1 = this.getFieldStrengthAt(samples[i]);
      const field2 = this.getFieldStrengthAt(samples[i + 1]);
      
      const change = Math.abs(field2 - field1);
      if (change > this.fieldStrength * 2) {
        bifurcations.push({
          point: samples[i],
          change: change,
          type: 'high-gradient'
        });
      }
    }

    return bifurcations;
  }

  /**
   * Get all attractors
   */
  getAttractors() {
    return Array.from(this.attractors.values());
  }

  /**
   * Clear all attractors
   */
  clearAttractors() {
    this.attractors.clear();
  }

  /**
   * Generate field heatmap
   */
  generateHeatmap(bounds, resolution = 50) {
    const heatmap = [];
    const step = bounds.max / resolution;

    for (let x = 0; x <= bounds.max; x += step) {
      const row = [];
      for (let y = 0; y <= bounds.max; y += step) {
        const strength = this.getFieldStrengthAt([x, y, 0]);
        row.push(strength);
      }
      heatmap.push(row);
    }

    return heatmap;
  }

  // Private methods

  _euclideanDistance(p1, p2) {
    return Math.sqrt(
      p1.reduce((sum, val, i) => sum + Math.pow(val - p2[i], 2), 0)
    );
  }

  _generateSamplePoints(count) {
    const samples = [];
    for (let i = 0; i < count; i++) {
      const point = new Array(this.dimensions).fill(0).map(() => Math.random() * 10);
      samples.push(point);
    }
    return samples;
  }

  /**
   * Get statistics
   */
  getStatistics() {
    return {
      totalAttractors: this.attractors.size,
      dimensions: this.dimensions,
      fieldStrength: this.fieldStrength,
      attractors: this.getAttractors()
    };
  }
}

// Export
if (typeof module !== 'undefined' && module.exports) {
  module.exports = AFMCore;
}
