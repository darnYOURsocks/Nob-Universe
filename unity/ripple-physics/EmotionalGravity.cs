using UnityEngine;

/// <summary>
/// EmotionalGravity - Emotional field gravity simulation
/// Objects are attracted based on emotional resonance
/// </summary>
public class EmotionalGravity : MonoBehaviour
{
    [SerializeField] private float emotionalStrength = 10f;
    [SerializeField] private float attractionRadius = 20f;
    [SerializeField] private AnimationCurve falloffCurve = AnimationCurve.EaseInOut(0, 1, 1, 0);

    [System.Serializable]
    public struct EmotionalField
    {
        public Vector3 position;
        public float valence;      // -1 to 1
        public float arousal;      // 0 to 1
        public float intensity;
    }

    private EmotionalField[] fields = new EmotionalField[0];
    private Rigidbody rb;

    private void Start()
    {
        rb = GetComponent<Rigidbody>();
        if (rb == null)
            rb = gameObject.AddComponent<Rigidbody>();
    }

    private void FixedUpdate()
    {
        if (rb != null)
        {
            Vector3 emotionalForce = CalculateEmotionalForce();
            rb.AddForce(emotionalForce, ForceMode.Acceleration);
        }
    }

    private Vector3 CalculateEmotionalForce()
    {
        Vector3 totalForce = Vector3.zero;

        foreach (EmotionalField field in fields)
        {
            Vector3 toField = field.position - transform.position;
            float distance = toField.magnitude;

            if (distance < attractionRadius && distance > 0.01f)
            {
                // Falloff based on distance
                float falloff = falloffCurve.Evaluate(1f - (distance / attractionRadius));
                
                // Force magnitude based on emotional intensity
                float forceMagnitude = field.intensity * emotionalStrength * falloff;
                
                // Attraction or repulsion based on valence
                if (field.valence > 0)
                    totalForce += (toField.normalized * forceMagnitude);
                else
                    totalForce -= (toField.normalized * forceMagnitude);
            }
        }

        return totalForce;
    }

    /// <summary>
    /// Add an emotional field
    /// </summary>
    public void AddEmotionalField(Vector3 position, float valence, float arousal, float intensity)
    {
        EmotionalField newField = new EmotionalField
        {
            position = position,
            valence = Mathf.Clamp(valence, -1f, 1f),
            arousal = Mathf.Clamp01(arousal),
            intensity = intensity
        };

        System.Array.Resize(ref fields, fields.Length + 1);
        fields[fields.Length - 1] = newField;
    }

    /// <summary>
    /// Clear all emotional fields
    /// </summary>
    public void ClearEmotionalFields()
    {
        fields = new EmotionalField[0];
    }

    /// <summary>
    /// Get current emotional state
    /// </summary>
    public EmotionalField GetCombinedField()
    {
        EmotionalField combined = new EmotionalField();
        
        if (fields.Length == 0)
            return combined;

        foreach (EmotionalField field in fields)
        {
            combined.valence += field.valence;
            combined.arousal += field.arousal;
            combined.intensity += field.intensity;
        }

        combined.valence /= fields.Length;
        combined.arousal /= fields.Length;
        combined.intensity /= fields.Length;

        return combined;
    }
}
