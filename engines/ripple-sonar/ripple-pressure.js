// Ripple Pressure Engine (RPN)
// Computes pressure = (A * S) / dt with nonlinear soft cap

export function computeRipplePressure(A, S, dt) {
    if (dt <= 0) dt = 0.0001;

    // base pressure calculation
    const rawPressure = (A * S) / dt;

    // nonlinear soften (Codex v1.1 pattern)
    const pressure = Math.pow(rawPressure, 0.85);

    // stability: inverse relationship
    const stability = 1 / (1 + pressure);

    // prediction: normalized spike likelihood
    const prediction = Math.min(pressure / 10, 1);

    return {
        pressure,
        stability,
        prediction,
        timestamp: new Date().toISOString()
    };
}

// Append results to DB (note: in static file environments this POST will not persist)
export async function logRipplePressure(A, S, dt) {
    const newEntry = computeRipplePressure(A, S, dt);

    const db = await fetch("../../databases/rfc-db.json").then(r => r.json());

    if (!Array.isArray(db.pressure_nodes)) db.pressure_nodes = [];

    db.pressure_nodes.push({
        id: "RPN-" + String(db.pressure_nodes.length + 1).padStart(3, "0"),
        input: { A, S, dt },
        output: newEntry
    });

    // Attempt to POST updated DB back to server (works only with a supporting backend)
    try {
        await fetch("../../databases/rfc-db.json", {
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(db, null, 2)
        });
    } catch (e) {
        // In static file hosting this will fail — caller should handle persistence
        console.warn('logRipplePressure: persistence not available in static hosting', e);
    }

    return newEntry;
}
