using UnityEngine;

/// <summary>
/// RipplePhysics - Core ripple physics engine for Unity
/// Simulates ripple propagation and wave interference
/// </summary>
public class RipplePhysics : MonoBehaviour
{
    [System.Serializable]
    public struct RippleSource
    {
        public Vector3 position;
        public float amplitude;
        public float frequency;
        public float dampening;
    }

    [SerializeField] private RippleSource[] rippleSources = new RippleSource[1];
    [SerializeField] private float gridSize = 10f;
    [SerializeField] private int gridResolution = 32;
    [SerializeField] private float timeScale = 1f;
    
    private float[,] heightMap;
    private float[,] velocityMap;
    private Mesh rippleMesh;
    private Vector3[] vertices;
    private float elapsedTime = 0f;

    private void Start()
    {
        InitializeMesh();
        InitializeRippleSources();
    }

    private void InitializeMesh()
    {
        // Create grid mesh
        vertices = new Vector3[gridResolution * gridResolution];
        int[] triangles = new int[(gridResolution - 1) * (gridResolution - 1) * 6];
        
        int triIndex = 0;
        for (int y = 0; y < gridResolution; y++)
        {
            for (int x = 0; x < gridResolution; x++)
            {
                int index = y * gridResolution + x;
                vertices[index] = new Vector3(
                    (x - gridResolution / 2) * gridSize / gridResolution,
                    0,
                    (y - gridResolution / 2) * gridSize / gridResolution
                );

                if (x < gridResolution - 1 && y < gridResolution - 1)
                {
                    int v0 = index;
                    int v1 = index + 1;
                    int v2 = index + gridResolution;
                    int v3 = index + gridResolution + 1;

                    triangles[triIndex++] = v0; triangles[triIndex++] = v2; triangles[triIndex++] = v1;
                    triangles[triIndex++] = v1; triangles[triIndex++] = v2; triangles[triIndex++] = v3;
                }
            }
        }

        rippleMesh = new Mesh();
        rippleMesh.vertices = vertices;
        rippleMesh.triangles = triangles;
        rippleMesh.RecalculateNormals();

        GetComponent<MeshFilter>().mesh = rippleMesh;
    }

    private void InitializeRippleSources()
    {
        if (rippleSources.Length == 0)
        {
            rippleSources = new RippleSource[1]
            {
                new RippleSource
                {
                    position = Vector3.zero,
                    amplitude = 0.5f,
                    frequency = 2f,
                    dampening = 0.98f
                }
            };
        }
    }

    private void Update()
    {
        elapsedTime += Time.deltaTime * timeScale;
        UpdateRipples();
        rippleMesh.vertices = vertices;
        rippleMesh.RecalculateNormals();
    }

    private void UpdateRipples()
    {
        for (int i = 0; i < vertices.Length; i++)
        {
            Vector3 vertex = vertices[i];
            vertex.y = 0;

            foreach (RippleSource source in rippleSources)
            {
                float distance = Vector3.Distance(vertex, source.position);
                float wave = source.amplitude * Mathf.Sin(distance * source.frequency - elapsedTime * source.frequency);
                wave *= Mathf.Exp(-distance * source.dampening);
                
                vertex.y += wave;
            }

            vertices[i] = vertex;
        }
    }

    /// <summary>
    /// Add a ripple source at runtime
    /// </summary>
    public void AddRippleSource(Vector3 position, float amplitude, float frequency)
    {
        RippleSource newSource = new RippleSource
        {
            position = position,
            amplitude = amplitude,
            frequency = frequency,
            dampening = 0.98f
        };

        System.Array.Resize(ref rippleSources, rippleSources.Length + 1);
        rippleSources[rippleSources.Length - 1] = newSource;
    }

    /// <summary>
    /// Get height at world position
    /// </summary>
    public float GetHeightAt(Vector3 worldPosition)
    {
        float height = 0f;
        foreach (RippleSource source in rippleSources)
        {
            float distance = Vector3.Distance(worldPosition, source.position);
            float wave = source.amplitude * Mathf.Sin(distance * source.frequency - elapsedTime * source.frequency);
            wave *= Mathf.Exp(-distance * source.dampening);
            height += wave;
        }
        return height;
    }
}
