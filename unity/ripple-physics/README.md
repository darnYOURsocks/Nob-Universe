# Ripple Physics - Unity Integration Guide

## Overview

RipplePhysics simulates realistic water/ripple propagation in Unity using a simple wave equation approach.

## Components

### RipplePhysics.cs
- **Main ripple simulation engine**
- Creates a deformable mesh based on ripple sources
- Supports multiple simultaneous ripple sources
- Real-time wave propagation and dampening

### EmotionalGravity.cs
- **Gravity based on emotional resonance**
- Objects attract/repel based on emotional fields
- Valence-based (positive/negative) attraction
- Arousal-based force intensity

## Usage

### Basic Setup

1. Create a GameObject with a Mesh Filter and Mesh Renderer
2. Add the `RipplePhysics` component
3. Adjust parameters:
   - Grid Size: Physical size of ripple surface
   - Grid Resolution: Detail level (higher = more detail but slower)
   - Time Scale: Speed of ripple simulation

### Adding Ripples at Runtime

```csharp
RipplePhysics ripples = GetComponent<RipplePhysics>();
ripples.AddRippleSource(new Vector3(0, 0, 5), amplitude: 0.5f, frequency: 2f);
```

### Emotional Gravity

1. Add `EmotionalGravity` to objects that should respond to emotional fields
2. Call `AddEmotionalField()` to add emotional influences:

```csharp
EmotionalGravity gravity = GetComponent<EmotionalGravity>();
gravity.AddEmotionalField(position, valence: 0.8f, arousal: 0.5f, intensity: 10f);
```

## Parameters

### RipplePhysics
- **Amplitude**: Wave height (0-1)
- **Frequency**: Wave speed
- **Dampening**: How quickly ripples fade (0.98 = 2% loss per frame)

### EmotionalGravity
- **Valence**: -1 (repel) to 1 (attract)
- **Arousal**: 0 (calm) to 1 (excited)
- **Intensity**: Force magnitude

## Performance Notes

- Lower grid resolution = better performance
- Fewer ripple sources = better performance
- Use FixedUpdate for physics consistency
