// EmotionalFieldComponent.cpp
// Unreal Engine 5 Implementation

#include "EmotionalFieldComponent.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "GameFramework/Character.h"

UEmotionalFieldComponent::UEmotionalFieldComponent()
    : FieldStrength(10.0f)
{
    PrimaryComponentTick.TickInterval = 0.016f;
    PrimaryComponentTick.bCanEverTick = true;
}

void UEmotionalFieldComponent::BeginPlay()
{
    Super::BeginPlay();

    if (!TargetMovement)
    {
        AActor* Owner = GetOwner();
        if (ACharacter* Character = Cast<ACharacter>(Owner))
        {
            TargetMovement = Character->GetCharacterMovement();
        }
    }

    // Initialize emotional state
    CurrentEmotion.Valence = 0.0f;
    CurrentEmotion.Arousal = 0.5f;
    CurrentEmotion.Resonance = 0.8f;
    CurrentEmotion.Intensity = 1.0f;
}

void UEmotionalFieldComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
    Super::TickComponent(DeltaTime, TickType, ThisTickFunction);

    if (TargetMovement)
    {
        FVector EmotionalForce = CalculateEmotionalForce();
        TargetMovement->AddForce(EmotionalForce);
    }
}

void UEmotionalFieldComponent::AddEmotionalInfluence(FVector Position, FEmotionalState Emotion)
{
    FEmotionalInfluence NewInfluence;
    NewInfluence.Position = Position;
    NewInfluence.Emotion = Emotion;

    EmotionalInfluences.AddHead(NewInfluence);
}

void UEmotionalFieldComponent::ClearInfluences()
{
    EmotionalInfluences.Unlink();
}

FEmotionalState UEmotionalFieldComponent::GetCombinedEmotionalState() const
{
    FEmotionalState Combined;
    Combined.Valence = 0.0f;
    Combined.Arousal = 0.0f;
    Combined.Resonance = 0.0f;
    Combined.Intensity = 0.0f;

    int32 Count = 0;

    for (auto It = EmotionalInfluences.GetHead(); It; It = It->Next())
    {
        const FEmotionalInfluence& Influence = **It;
        Combined.Valence += Influence.Emotion.Valence;
        Combined.Arousal += Influence.Emotion.Arousal;
        Combined.Resonance += Influence.Emotion.Resonance;
        Combined.Intensity += Influence.Emotion.Intensity;
        Count++;
    }

    if (Count > 0)
    {
        Combined.Valence /= Count;
        Combined.Arousal /= Count;
        Combined.Resonance /= Count;
        Combined.Intensity /= Count;
    }

    return Combined;
}

void UEmotionalFieldComponent::ApplyEmotionalForce(FVector& OutForce)
{
    OutForce = CalculateEmotionalForce();
}

FVector UEmotionalFieldComponent::CalculateEmotionalForce()
{
    FVector TotalForce = FVector::ZeroVector;
    const float MaxDistance = 50.0f;

    if (!GetOwner())
        return TotalForce;

    FVector OwnerLocation = GetOwner()->GetActorLocation();

    for (auto It = EmotionalInfluences.GetHead(); It; It = It->Next())
    {
        const FEmotionalInfluence& Influence = **It;
        FVector ToInfluence = Influence.Emotion.Position - OwnerLocation;
        float Distance = ToInfluence.Length();

        if (Distance < MaxDistance && Distance > 0.01f)
        {
            float Falloff = CalculateFalloff(Distance, MaxDistance);
            float ForceMagnitude = Influence.Emotion.Intensity * FieldStrength * Falloff;

            // Attraction if positive valence, repulsion if negative
            if (Influence.Emotion.Valence > 0.0f)
            {
                TotalForce += (ToInfluence.GetSafeNormal() * ForceMagnitude * Influence.Emotion.Valence);
            }
            else
            {
                TotalForce -= (ToInfluence.GetSafeNormal() * ForceMagnitude * FMath::Abs(Influence.Emotion.Valence));
            }
        }
    }

    return TotalForce;
}

float UEmotionalFieldComponent::CalculateFalloff(float Distance, float MaxDistance) const
{
    if (Distance >= MaxDistance)
        return 0.0f;

    float NormalizedDistance = Distance / MaxDistance;
    return FMath::Cos(NormalizedDistance * PI * 0.5f);
}
