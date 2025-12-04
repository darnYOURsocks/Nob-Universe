"""
Ripple Lab
Advanced ripple analysis laboratory
"""

import json
import numpy as np
from datetime import datetime
from scipy import signal

class RippleLab:
    """Advanced ripple analysis toolkit"""
    
    def __init__(self):
        self.experiments = []
        self.results = []
        
    def create_ripple(self, frequency=440, amplitude=1.0, duration=1.0, sample_rate=44100):
        """Create a ripple waveform"""
        t = np.linspace(0, duration, int(sample_rate * duration))
        ripple = amplitude * np.sin(2 * np.pi * frequency * t)
        
        return {
            'frequency': frequency,
            'amplitude': amplitude,
            'duration': duration,
            'sample_rate': sample_rate,
            'waveform': ripple.tolist()[:1000],  # Store only first 1000 samples
            'timestamp': datetime.now().isoformat()
        }
    
    def analyze_spectrum(self, ripple):
        """Analyze frequency spectrum"""
        waveform = np.array(ripple['waveform'])
        fft = np.fft.fft(waveform)
        freqs = np.fft.fftfreq(len(waveform), 1/ripple['sample_rate'])
        magnitude = np.abs(fft)
        
        analysis = {
            'peak_frequency': float(freqs[np.argmax(magnitude)]),
            'peak_magnitude': float(np.max(magnitude)),
            'harmonic_energy': float(np.sum(magnitude)**2 / len(magnitude)),
            'spectral_centroid': float(np.average(freqs, weights=magnitude))
        }
        
        return analysis
    
    def detect_interference(self, ripple1, ripple2):
        """Detect interference patterns between ripples"""
        w1 = np.array(ripple1['waveform'])
        w2 = np.array(ripple2['waveform'])
        
        # Pad to same length
        max_len = max(len(w1), len(w2))
        w1 = np.pad(w1, (0, max_len - len(w1)), mode='constant')
        w2 = np.pad(w2, (0, max_len - len(w2)), mode='constant')
        
        combined = w1 + w2
        constructive = np.max(combined)
        destructive = np.min(combined)
        
        interference = {
            'type': 'constructive' if constructive > (w1.max() + w2.max()) * 0.9 else 'mixed',
            'amplitude_increase': float(constructive / (w1.max() + w2.max())),
            'phase_difference': float(ripple1['frequency'] - ripple2['frequency']),
            'beat_frequency': abs(float(ripple1['frequency'] - ripple2['frequency']))
        }
        
        return interference
    
    def measure_coherence(self, ripples):
        """Measure coherence between multiple ripples"""
        if len(ripples) < 2:
            return 0.0
        
        # Simple cross-correlation based coherence
        waveforms = [np.array(r['waveform']) for r in ripples]
        max_len = max(len(w) for w in waveforms)
        
        correlations = []
        for i in range(len(waveforms)):
            for j in range(i + 1, len(waveforms)):
                w1 = np.pad(waveforms[i], (0, max_len - len(waveforms[i])), mode='constant')
                w2 = np.pad(waveforms[j], (0, max_len - len(waveforms[j])), mode='constant')
                
                # Normalize
                w1 = (w1 - np.mean(w1)) / (np.std(w1) + 1e-10)
                w2 = (w2 - np.mean(w2)) / (np.std(w2) + 1e-10)
                
                correlation = np.mean(w1 * w2)
                correlations.append(correlation)
        
        return float(np.mean(correlations)) if correlations else 0.0
    
    def resonance_analysis(self, ripple, cavity_frequency):
        """Analyze resonance in a cavity"""
        freq_ratio = ripple['frequency'] / cavity_frequency
        detuning = abs(freq_ratio - 1.0)
        
        # Q-factor (quality factor) estimation
        q_factor = 1.0 / detuning if detuning > 0.01 else 100.0
        
        resonance = {
            'frequency_ratio': float(freq_ratio),
            'detuning': float(detuning),
            'q_factor': float(min(q_factor, 1000.0)),  # Cap at 1000
            'resonance_strength': float(ripple['amplitude'] * (1.0 + 1.0/(1.0 + detuning)))
        }
        
        return resonance

def main():
    """Main execution"""
    print("=== Ripple Lab ===\n")
    
    lab = RippleLab()
    
    # Create ripples
    print("Creating ripples...")
    ripple1 = lab.create_ripple(frequency=440, amplitude=0.8)
    ripple2 = lab.create_ripple(frequency=528, amplitude=0.7)
    ripple3 = lab.create_ripple(frequency=639, amplitude=0.6)
    
    ripples = [ripple1, ripple2, ripple3]
    
    # Analyze spectrum
    print("\nSpectral Analysis:")
    for i, ripple in enumerate(ripples):
        analysis = lab.analyze_spectrum(ripple)
        print(f"Ripple {i+1}:")
        print(f"  Peak Frequency: {analysis['peak_frequency']:.1f} Hz")
        print(f"  Harmonic Energy: {analysis['harmonic_energy']:.2f}")
    
    # Detect interference
    print("\nInterference Analysis:")
    interference = lab.detect_interference(ripple1, ripple2)
    print(f"Type: {interference['type']}")
    print(f"Amplitude Increase: {interference['amplitude_increase']:.2%}")
    print(f"Beat Frequency: {interference['beat_frequency']:.1f} Hz")
    
    # Measure coherence
    print("\nCoherence Analysis:")
    coherence = lab.measure_coherence(ripples)
    print(f"System Coherence: {coherence:.2%}")
    
    # Resonance analysis
    print("\nResonance Analysis:")
    for i, ripple in enumerate(ripples):
        resonance = lab.resonance_analysis(ripple, cavity_frequency=500)
        print(f"Ripple {i+1} in 500Hz cavity:")
        print(f"  Q-Factor: {resonance['q_factor']:.1f}")
        print(f"  Resonance Strength: {resonance['resonance_strength']:.2f}")
    
    print("\n=== Lab Analysis Complete ===")

if __name__ == '__main__':
    main()
