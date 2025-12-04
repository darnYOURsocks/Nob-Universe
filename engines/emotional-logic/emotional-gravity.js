// Emotional Gravity Engine (EGN)
// Implements CE-EGN-001 from the Codex

export function measureDistance(a, b) {
    return Math.sqrt(
        (a.x - b.x) ** 2 +
        (a.y - b.y) ** 2 +
        (a.z - b.z) ** 2
    );
}

export function computeEmotionalGravity(nodeA, nodeB) {
    // Extract variables
    const I1 = Math.max(0, Math.min(1, nodeA.intensity ?? 0));
    const I2 = Math.max(0, Math.min(1, nodeB.intensity ?? 0));

    const C1 = Math.max(0, Math.min(1, nodeA.clarity ?? 0));
    const C2 = Math.max(0, Math.min(1, nodeB.clarity ?? 0));

    const rawDistance = (typeof nodeA.distanceTo === 'function') ? nodeA.distanceTo(nodeB) : measureDistance(nodeA.position || nodeA, nodeB.position || nodeB);
    const distance = Math.max(rawDistance, 0.01);

    const G_e = 0.87; // Emotional gravitational constant

    // Force calculation
    const force = (G_e * (I1 * I2 * C1 * C2)) / (distance * distance);

    // Curvature (well depth)
    const wellDepth = force * (1 - ((C1 + C2) / 2));

    // Emotional mass approximation
    const stabilityA = nodeA.stability ?? 0.5;
    const stabilityB = nodeB.stability ?? 0.5;
    const emotionalMass = Math.max(0.01, stabilityA + stabilityB + 0.1);

    const acceleration = force / emotionalMass;

    // Direction vector
    const ax = (nodeA.position && nodeA.position.x !== undefined) ? nodeA.position.x : nodeA.x || 0;
    const ay = (nodeA.position && nodeA.position.y !== undefined) ? nodeA.position.y : nodeA.y || 0;
    const az = (nodeA.position && nodeA.position.z !== undefined) ? nodeA.position.z : nodeA.z || 0;

    const bx = (nodeB.position && nodeB.position.x !== undefined) ? nodeB.position.x : nodeB.x || 0;
    const by = (nodeB.position && nodeB.position.y !== undefined) ? nodeB.position.y : nodeB.y || 0;
    const bz = (nodeB.position && nodeB.position.z !== undefined) ? nodeB.position.z : nodeB.z || 0;

    const dx = bx - ax;
    const dy = by - ay;
    const dz = bz - az;

    const distanceNorm = Math.sqrt(dx*dx + dy*dy + dz*dz) || 0.0001;

    const direction = {
        x: dx / distanceNorm,
        y: dy / distanceNorm,
        z: dz / distanceNorm
    };

    return {
        force,
        wellDepth,
        acceleration,
        direction,
        timestamp: new Date().toISOString()
    };
}
