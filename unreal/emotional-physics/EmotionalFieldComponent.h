// EmotionalFieldComponent.h
// Unreal Engine 5 Emotional Field Simulation Component

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Containers/LinkedList.h"
#include "EmotionalFieldComponent.generated.h"

/**
 * Represents an emotional state
 */
USTRUCT(BlueprintType)
struct FEmotionalState
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Emotion")
    float Valence;      // -1.0 to 1.0 (negative to positive)

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Emotion")
    float Arousal;      // 0.0 to 1.0 (calm to excited)

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Emotion")
    float Resonance;    // 0.0 to 1.0 (harmonic alignment)

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Emotion")
    float Intensity;    // Force magnitude
};

/**
 * Emotional Field Component
 * Simulates emotional forces that affect character/actor movement
 */
UCLASS(ClassGroup=(Custom), meta=(BlueprintSpawnableComponent))
class NOBS_UNIVERSE_API UEmotionalFieldComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UEmotionalFieldComponent();

    virtual void BeginPlay() override;
    virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

    // Emotional field strength
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Emotion")
    float FieldStrength;

    // Emotional state
    UPROPERTY(BlueprintReadWrite, Category = "Emotion")
    FEmotionalState CurrentEmotion;

    // Movement component to affect
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Emotion")
    class UCharacterMovementComponent* TargetMovement;

    // Add emotional field influence
    UFUNCTION(BlueprintCallable, Category = "Emotion")
    void AddEmotionalInfluence(FVector Position, FEmotionalState Emotion);

    // Clear all influences
    UFUNCTION(BlueprintCallable, Category = "Emotion")
    void ClearInfluences();

    // Get combined emotional state
    UFUNCTION(BlueprintCallable, Category = "Emotion")
    FEmotionalState GetCombinedEmotionalState() const;

    // Apply emotional force
    UFUNCTION(BlueprintCallable, Category = "Emotion")
    void ApplyEmotionalForce(FVector& OutForce);

private:
    struct FEmotionalInfluence
    {
        FVector Position;
        FEmotionalState Emotion;
    };

    TLinkedList<FEmotionalInfluence> EmotionalInfluences;

    FVector CalculateEmotionalForce();
    float CalculateFalloff(float Distance, float MaxDistance) const;
};
