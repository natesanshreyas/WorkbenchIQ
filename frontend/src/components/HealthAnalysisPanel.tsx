'use client';

interface HealthAnalysisResult {
  id: string;
  llm_outputs?: {
      health_assessment?: {
      activity_analysis?: any;
      cardiovascular_assessment?: any;
      sleep_assessment?: any;
      overall_health_plan?: any;
      underwriting_decision?: any;
    };
  };
  document_markdown?: string;
}

interface HealthAnalysisPanelProps {
  result: HealthAnalysisResult;
}

export default function HealthAnalysisPanel({ result }: HealthAnalysisPanelProps) {
  const analysis = result.llm_outputs?.health_assessment;

  if (!analysis) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <p className="text-slate-600">No analysis available</p>
      </div>
    );
  }

const activityAnalysis = analysis.activity_analysis?.parsed;
const cardioAnalysis = analysis.cardiovascular_assessment?.parsed;
const sleepAnalysis = analysis.sleep_assessment?.parsed;
const overallPlan = analysis.overall_health_plan?.parsed;
const underwritingDecision = analysis.underwriting_decision?.parsed;

  const getRiskColor = (risk: string) => {
    if (!risk) return 'bg-slate-100 text-slate-700';
    const lower = risk.toLowerCase();
    if (lower.includes('low')) return 'bg-emerald-100 text-emerald-700';
    if (lower.includes('moderate')) return 'bg-amber-100 text-amber-700';
    return 'bg-red-100 text-red-700';
  };

  const getPriorityColor = (priority: string) => {
    if (!priority) return 'text-slate-600';
    const lower = priority.toLowerCase();
    if (lower.includes('high')) return 'text-red-600 font-semibold';
    if (lower.includes('medium')) return 'text-amber-600 font-semibold';
    return 'text-emerald-600 font-semibold';
  };

  return (
    <div className="space-y-6 p-6">
            {/* Underwriting Decision */}
      {underwritingDecision && (
        <div className="bg-gradient-to-r from-purple-50 to-indigo-50 rounded-lg shadow-lg p-6 border-2 border-purple-300">
          <h2 className="text-2xl font-bold text-purple-900 mb-4">Underwriting Decision</h2>
          
          <div className="grid grid-cols-3 gap-4 mb-6">
            <div className="bg-white rounded-lg p-4 shadow">
              <div className="text-sm text-slate-600 mb-1">Decision</div>
              <div className="text-xl font-bold text-purple-700">{underwritingDecision.underwriting_decision}</div>
            </div>
            <div className="bg-white rounded-lg p-4 shadow">
              <div className="text-sm text-slate-600 mb-1">Risk Classification</div>
              <div className="text-xl font-bold text-indigo-700">{underwritingDecision.risk_classification}</div>
            </div>
            <div className="bg-white rounded-lg p-4 shadow">
              <div className="text-sm text-slate-600 mb-1">Premium Adjustment</div>
              <div className="text-xl font-bold text-emerald-700">{underwritingDecision.premium_adjustment}</div>
            </div>
          </div>

          <div className="bg-white rounded-lg p-4 mb-4">
            <h3 className="font-semibold text-slate-900 mb-2">Decision Rationale</h3>
            <p className="text-slate-700">{underwritingDecision.decision_rationale}</p>
          </div>

          {underwritingDecision.risk_factors && underwritingDecision.risk_factors.length > 0 && (
            <div className="bg-white rounded-lg p-4">
              <h3 className="font-semibold text-slate-900 mb-3">Risk Factors</h3>
              <div className="space-y-2">
                {underwritingDecision.risk_factors.map((factor: any, idx: number) => (
                  <div key={idx} className="flex items-start gap-3 p-3 bg-slate-50 rounded">
                    <span className={`px-2 py-1 rounded text-xs font-medium ${
                      factor.assessment === 'Positive' ? 'bg-emerald-100 text-emerald-700' :
                      factor.assessment === 'Negative' ? 'bg-red-100 text-red-700' :
                      'bg-slate-100 text-slate-700'
                    }`}>
                      {factor.assessment}
                    </span>
                    <div className="flex-1">
                      <div className="font-medium text-slate-900">{factor.factor}</div>
                      <div className="text-sm text-slate-600">{factor.impact}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
      {/* Overall Health Score */}
      {overallPlan && (
        <div className="bg-gradient-to-r from-emerald-50 to-teal-50 rounded-lg shadow-md p-6 border border-emerald-200">
          <div className="flex items-start justify-between">
            <div>
              <h2 className="text-2xl font-bold text-emerald-900 mb-2">Overall Health Assessment</h2>
              <p className="text-emerald-800 text-lg max-w-3xl">{overallPlan.summary}</p>
            </div>
            <div className="text-right">
              <div className="text-5xl font-bold text-emerald-600">{overallPlan.overall_health_score}</div>
              <div className="text-sm text-emerald-700 font-medium">Health Score</div>
            </div>
          </div>

          <div className="mt-6 grid grid-cols-2 gap-4">
            <div>
              <h3 className="font-semibold text-emerald-900 mb-2">Risk Category</h3>
              <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${getRiskColor(overallPlan.health_risk_category)}`}>
                {overallPlan.health_risk_category}
              </span>
            </div>
          </div>
        </div>
      )}

      {/* Activity Analysis */}
      {activityAnalysis && (
        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-blue-500">
          <h3 className="flex items-center gap-2 text-lg font-bold text-slate-900 mb-4">
            <span>🚶</span> Activity Analysis
          </h3>
          <div className="space-y-3">
            <div className="flex justify-between items-start">
              <span className="font-medium text-slate-700">Activity Level</span>
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${getRiskColor(activityAnalysis.activity_level)}`}>
                {activityAnalysis.activity_level}
              </span>
            </div>
            <div className="flex justify-between items-start">
              <span className="font-medium text-slate-700">Steps Per Day</span>
              <span className="text-slate-900 font-semibold">{activityAnalysis.steps_per_day?.toLocaleString()}</span>
            </div>
            <div className="mt-4 p-3 bg-blue-50 rounded border border-blue-200">
              <p className="text-sm text-slate-700">{activityAnalysis.recommendation}</p>
            </div>
          </div>
        </div>
      )}

      {/* Cardiovascular Assessment */}
      {cardioAnalysis && (
        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-red-500">
          <h3 className="flex items-center gap-2 text-lg font-bold text-slate-900 mb-4">
            <span>❤️</span> Cardiovascular Health
          </h3>
          <div className="space-y-3">
            <div className="flex justify-between items-start">
              <span className="font-medium text-slate-700">Fitness Category</span>
              <span className="text-slate-900 font-semibold">{cardioAnalysis.fitness_category}</span>
            </div>
            <div className="flex justify-between items-start">
              <span className="font-medium text-slate-700">VO2 Max</span>
              <span className="text-slate-900 font-semibold">{cardioAnalysis.vo2_max} mL/kg/min</span>
            </div>
            <div className="flex justify-between items-start">
              <span className="font-medium text-slate-700">Cardiovascular Risk</span>
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${getRiskColor(cardioAnalysis.cardio_risk)}`}>
                {cardioAnalysis.cardio_risk}
              </span>
            </div>
            <div className="mt-4 p-3 bg-red-50 rounded border border-red-200">
              <p className="text-sm text-slate-700">{cardioAnalysis.recommendation}</p>
            </div>
          </div>
        </div>
      )}

      {/* Sleep Assessment */}
      {sleepAnalysis && (
        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-indigo-500">
          <h3 className="flex items-center gap-2 text-lg font-bold text-slate-900 mb-4">
            <span>😴</span> Sleep Quality
          </h3>
          <div className="space-y-3">
            <div className="flex justify-between items-start">
              <span className="font-medium text-slate-700">Sleep Quality</span>
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${getRiskColor(sleepAnalysis.sleep_quality)}`}>
                {sleepAnalysis.sleep_quality}
              </span>
            </div>
            <div className="flex justify-between items-start">
              <span className="font-medium text-slate-700">Average Hours</span>
              <span className="text-slate-900 font-semibold">{sleepAnalysis.avg_sleep_hours} hours/night</span>
            </div>
            <div className="flex justify-between items-start">
              <span className="font-medium text-slate-700">Meets Guidelines</span>
              <span className="flex items-center gap-2">
                {sleepAnalysis.meets_guidelines ? (
                  <span className="text-emerald-600 font-semibold">✓ Yes</span>
                ) : (
                  <span className="text-amber-600 font-semibold">⚠ No</span>
                )}
              </span>
            </div>
            <div className="mt-4 p-3 bg-indigo-50 rounded border border-indigo-200">
              <p className="text-sm text-slate-700">{sleepAnalysis.recommendation}</p>
            </div>
          </div>
        </div>
      )}

      {/* Recommendations */}
      {overallPlan?.integrated_recommendations && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="flex items-center gap-2 text-lg font-bold text-slate-900 mb-4">
            📈 Personalized Recommendations
          </h3>
          <div className="space-y-3">
            {overallPlan.integrated_recommendations.map((rec: any, idx: number) => (
              <div key={idx} className="p-4 bg-slate-50 rounded-lg border border-slate-200">
                <div className="flex items-start justify-between mb-2">
                  <h4 className={`font-semibold ${getPriorityColor(rec.priority)}`}>
                    {rec.action}
                  </h4>
                  <span className="text-xs font-medium px-2 py-1 bg-slate-200 text-slate-700 rounded">
                    {rec.priority} Priority
                  </span>
                </div>
                <p className="text-sm text-slate-700">Expected benefit: {rec.expected_benefit}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Next Steps */}
      {overallPlan?.next_steps && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-bold text-slate-900 mb-4">Next Steps</h3>
          <ul className="space-y-2">
            {overallPlan.next_steps.map((step: string, idx: number) => (
              <li key={idx} className="flex items-start gap-3">
                <span className="inline-flex items-center justify-center w-6 h-6 rounded-full bg-emerald-100 text-emerald-700 font-semibold text-sm flex-shrink-0 mt-0.5">
                  {idx + 1}
                </span>
                <span className="text-slate-700">{step}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
