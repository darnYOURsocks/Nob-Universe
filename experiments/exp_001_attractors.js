const path = require("path");
const AFMCore = require("../engines/afm/afm-core");

const metadata = {
  id: "exp_001_attractors",
  name: "Attractor Field Mapping",
  description: "Maps field strength and trajectories across clustered attractors",
  tags: ["afm", "attractors", "trajectory"],
};

function run() {
  const afm = new AFMCore({ dimensions: 3, resolution: 50, fieldStrength: 1.2 });

  afm.addAttractor("alpha", [0, 0, 0], 1.2, "core");
  afm.addAttractor("beta", [2, 2, 0], 0.8, "peripheral");
  afm.addAttractor("gamma", [-1.5, 2.5, 0], 1.1, "peripheral");
  afm.addAttractor("delta", [-2, -1, 0], 0.9, "edge");

  const samplePoint = [0.5, 0.5, 0];
  const nearest = afm.findNearestAttractor(samplePoint);
  const trajectory = afm.traceTrajectory([1.5, -0.5, 0], 40, 0.08);
  const bifurcations = afm.detectBifurcationPoints();
  const heatmap = afm.generateHeatmap({ max: 2.5 }, 12);

  return {
    metadata,
    statistics: afm.getStatistics(),
    nearest,
    trajectoryPreview: trajectory.slice(0, 5),
    bifurcationCount: bifurcations.length,
    heatmapSample: heatmap.slice(0, 3).map(row => row.slice(0, 3)),
    generatedAt: new Date().toISOString(),
  };
}

module.exports = {
  metadata,
  run,
  file: path.basename(__filename),
};
