# Emotional Physics - Unreal Engine Integration

## Overview

EmotionalFieldComponent for Unreal Engine 5 simulates emotional forces that affect character movement and behavior.

## Features

- **Emotional State Tracking**: Valence (positive/negative), Arousal (calm/excited), Resonance
- **Dynamic Force Application**: Characters respond to emotional fields
- **Real-time Influence System**: Add/remove emotional influences at runtime
- **Blueprint Compatible**: Full blueprint support for designers

## Installation

1. Copy `EmotionalFieldComponent.h` and `EmotionalFieldComponent.cpp` to your project's `Source/YourProject/` directory
2. Rebuild the Visual Studio project
3. Open Unreal Engine and enable the plugin

## Usage

### In C++

```cpp
// Add component to character
ACharacter* MyCharacter = ...;
UEmotionalFieldComponent* EmotionComponent = NewObject<UEmotionalFieldComponent>(MyCharacter);
MyCharacter->AddOwnedComponent(EmotionComponent);
EmotionComponent->RegisterComponent();

// Add emotional influence
FEmotionalState JoyfulState;
JoyfulState.Valence = 0.8f;    // Positive
JoyfulState.Arousal = 0.7f;    // Excited
JoyfulState.Resonance = 0.9f;  // High alignment
JoyfulState.Intensity = 10.0f; // Force strength

EmotionComponent->AddEmotionalInfluence(InfluenceLocation, JoyfulState);
```

### In Blueprint

1. Add EmotionalFieldComponent to Character Blueprint
2. Call "Add Emotional Influence" with:
   - **Position**: World location of emotional source
   - **Valence**: -1.0 (negative) to 1.0 (positive)
   - **Arousal**: 0.0 (calm) to 1.0 (excited)
   - **Resonance**: 0.0 to 1.0 (harmonic alignment)
   - **Intensity**: Force magnitude

## Parameters

- **Field Strength**: Multiplier for all emotional forces (default: 10.0)
- **Valence Range**: -1.0 to 1.0
  - Negative values: Repulsion
  - Positive values: Attraction
- **Arousal Range**: 0.0 to 1.0
  - Low: Calm, sustained forces
  - High: Excited, reactive forces

## Example Emotions

### Joy
- Valence: 0.8
- Arousal: 0.7
- Effect: Attracts, energizing

### Tension
- Valence: -0.5
- Arousal: 0.9
- Effect: Repels, destabilizing

### Harmony
- Valence: 0.9
- Arousal: 0.4
- Effect: Attracts smoothly, stabilizing

## Performance

- Efficient linked list for dynamic influence management
- Falloff calculation prevents distant influences
- Configurable tick rate for optimization
