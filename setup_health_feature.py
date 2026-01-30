#!/usr/bin/env python3
"""
Setup script to add Apple Health data feature to WorkbenchIQ
This script creates new files and patches existing files
"""

import os
import json
import re
from pathlib import Path
from typing import Optional

class HealthFeatureSetup:
    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)
        self.errors = []
        self.created_files = []
        self.patched_files = []
        
    def log(self, msg: str):
        print(f"✓ {msg}")
    
    def error(self, msg: str):
        print(f"✗ {msg}")
        self.errors.append(msg)
    
    def create_health_prompts_json(self):
        """Create prompts/health-prompts.json"""
        file_path = self.repo_root / "prompts" / "health-prompts.json"
        
        content = {
            "health_assessment": {
                "activity_analysis": {
                    "prompt": """You are a health and fitness expert analyzing Apple Health data.

Given the health metrics data in JSON format, analyze the user's activity level.

Focus on:
- Steps per day and activity classification
- Comparison to recommended daily activity
- Overall activity assessment

Return STRICT JSON:

{
  "activity_level": "Low | Moderate | High | Very High",
  "steps_per_day": "number",
  "classification": "Description of activity level",
  "recommendation": "Personalized recommendation based on current activity",
  "risk_assessment": "Low | Moderate | High"
}
"""
                },
                "cardiovascular_assessment": {
                    "prompt": """You are a cardiologist analyzing Apple Health data.

Given the health metrics including VO2 max, assess the user's cardiovascular health and fitness level.

Focus on:
- VO2 max value and fitness category
- Cardiovascular risk assessment
- Correlation with overall health

Return STRICT JSON:

{
  "vo2_max": "number",
  "fitness_category": "Poor | Fair | Good | Excellent | Superior",
  "cardio_risk": "Low | Low-Moderate | Moderate | Moderate-High | High",
  "assessment": "Clinical assessment of cardiovascular fitness",
  "recommendation": "Recommendation for cardiovascular health"
}
"""
                },
                "sleep_assessment": {
                    "prompt": """You are a sleep medicine expert analyzing Apple Health data.

Given the health metrics including average sleep hours, assess the user's sleep quality and patterns.

Focus on:
- Average sleep hours vs recommended 7-9 hours
- Sleep quality classification
- Impact on overall health

Return STRICT JSON:

{
  "avg_sleep_hours": "number",
  "sleep_quality": "Poor | Fair | Good | Excellent",
  "meets_guidelines": "boolean",
  "assessment": "Assessment of sleep quality and adequacy",
  "recommendation": "Recommendation for improving sleep"
}
"""
                },
                "overall_health_plan": {
                    "prompt": """You are a health and wellness coordinator synthesizing Apple Health data analysis.

Given the analysis of activity, cardiovascular fitness, and sleep metrics, create a comprehensive health plan.

Focus on:
- Overall health score
- Key areas of strength and concern
- Integrated recommendations
- Next steps for health improvement

Return STRICT JSON:

{
  "overall_health_score": "number between 1-100",
  "summary": "2-3 sentence executive summary of overall health status",
  "strengths": ["List of health areas that are performing well"],
  "areas_for_improvement": ["List of areas that need attention"],
  "integrated_recommendations": [
    {
      "priority": "High | Medium | Low",
      "action": "Specific actionable recommendation",
      "expected_benefit": "Expected benefit or outcome"
    }
  ],
  "next_steps": ["Specific next steps to implement"],
  "health_risk_category": "Low Risk | Moderate Risk | High Risk"
}
"""
                }
            }
        }
        
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w') as f:
                json.dump(content, f, indent=2)
            self.log(f"Created {file_path}")
            self.created_files.append(str(file_path))
        except Exception as e:
            self.error(f"Failed to create health prompts: {e}")
    
    def create_health_input_form(self):
        """Create frontend/src/components/HealthInputForm.tsx"""
        file_path = self.repo_root / "frontend" / "src" / "components" / "HealthInputForm.tsx"
        
        content = """'use client';

import { useState } from 'react';
import { AlertCircle, CheckCircle, Loader } from 'lucide-react';

interface HealthMetrics {
  steps_per_day: number;
  vo2_max: number;
  avg_sleep_hours: number;
  heart_rate_resting?: number;
  active_energy?: number;
  external_reference?: string;
}

interface HealthInputFormProps {
  onSuccess?: (result: any) => void;
  onLoading?: (loading: boolean) => void;
}

export default function HealthInputForm({ onSuccess, onLoading }: HealthInputFormProps) {
  const [formData, setFormData] = useState<HealthMetrics>({
    steps_per_day: 8500,
    vo2_max: 42,
    avg_sleep_hours: 7.5,
    heart_rate_resting: 65,
    active_energy: 500,
    external_reference: '',
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: parseFloat(value) || value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(false);

    if (onLoading) onLoading(true);

    try {
      const response = await fetch('/api/health', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to submit health data');
      }

      const result = await response.json();
      setSuccess(true);
      setFormData({
        steps_per_day: 8500,
        vo2_max: 42,
        avg_sleep_hours: 7.5,
        heart_rate_resting: 65,
        active_energy: 500,
        external_reference: '',
      });

      if (onSuccess) {
        onSuccess(result);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
      if (onLoading) onLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 max-w-2xl">
      <h2 className="text-2xl font-bold text-slate-900 mb-6 flex items-center gap-2">
        <span>❤️</span> Apple Health Data Input
      </h2>

      {error && (
        <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
          <div className="text-sm text-red-800">{error}</div>
        </div>
      )}

      {success && (
        <div className="mb-4 p-4 bg-emerald-50 border border-emerald-200 rounded-lg flex items-start gap-3">
          <CheckCircle className="w-5 h-5 text-emerald-600 flex-shrink-0 mt-0.5" />
          <div className="text-sm text-emerald-800">Health plan generated successfully!</div>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Required Fields */}
        <div className="border-b border-slate-200 pb-6">
          <h3 className="text-sm font-semibold text-slate-900 mb-4 uppercase tracking-wide">
            Required Metrics
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                Steps Per Day <span className="text-red-500">*</span>
              </label>
              <input
                type="number"
                name="steps_per_day"
                value={formData.steps_per_day}
                onChange={handleInputChange}
                required
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
                placeholder="e.g., 8500"
              />
              <p className="text-xs text-slate-500 mt-1">Daily step count</p>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                VO2 Max <span className="text-red-500">*</span>
              </label>
              <input
                type="number"
                name="vo2_max"
                value={formData.vo2_max}
                onChange={handleInputChange}
                required
                step="0.1"
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
                placeholder="e.g., 42"
              />
              <p className="text-xs text-slate-500 mt-1">mL/kg/min</p>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                Average Sleep Hours <span className="text-red-500">*</span>
              </label>
              <input
                type="number"
                name="avg_sleep_hours"
                value={formData.avg_sleep_hours}
                onChange={handleInputChange}
                required
                step="0.5"
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
                placeholder="e.g., 7.5"
              />
              <p className="text-xs text-slate-500 mt-1">Hours per night</p>
            </div>
          </div>
        </div>

        {/* Optional Fields */}
        <div className="border-b border-slate-200 pb-6">
          <h3 className="text-sm font-semibold text-slate-900 mb-4 uppercase tracking-wide">
            Optional Metrics
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                Resting Heart Rate
              </label>
              <input
                type="number"
                name="heart_rate_resting"
                value={formData.heart_rate_resting || ''}
                onChange={handleInputChange}
                step="1"
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
                placeholder="e.g., 65"
              />
              <p className="text-xs text-slate-500 mt-1">Beats per minute</p>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                Active Energy
              </label>
              <input
                type="number"
                name="active_energy"
                value={formData.active_energy || ''}
                onChange={handleInputChange}
                step="10"
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
                placeholder="e.g., 500"
              />
              <p className="text-xs text-slate-500 mt-1">Kilocalories</p>
            </div>

            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-slate-700 mb-2">
                Reference ID
              </label>
              <input
                type="text"
                name="external_reference"
                value={formData.external_reference}
                onChange={handleInputChange}
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
                placeholder="e.g., USER_12345"
              />
              <p className="text-xs text-slate-500 mt-1">Optional reference identifier</p>
            </div>
          </div>
        </div>

        {/* Submit Button */}
        <div className="flex gap-3">
          <button
            type="submit"
            disabled={loading}
            className="flex items-center justify-center gap-2 px-6 py-3 bg-emerald-600 hover:bg-emerald-700 disabled:bg-slate-300 text-white font-medium rounded-lg transition-colors"
          >
            {loading && <Loader className="w-4 h-4 animate-spin" />}
            {loading ? 'Analyzing...' : 'Analyze My Health'}
          </button>
        </div>
      </form>
    </div>
  );
}
"""
        
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w') as f:
                f.write(content)
            self.log(f"Created {file_path}")
            self.created_files.append(str(file_path))
        except Exception as e:
            self.error(f"Failed to create HealthInputForm: {e}")
    
    def create_health_analysis_panel(self):
        """Create frontend/src/components/HealthAnalysisPanel.tsx"""
        file_path = self.repo_root / "frontend" / "src" / "components" / "HealthAnalysisPanel.tsx"
        
        content = """'use client';

interface HealthAnalysisResult {
  id: string;
  llm_outputs?: {
    health_assessment?: {
      activity_analysis?: any;
      cardiovascular_assessment?: any;
      sleep_assessment?: any;
      overall_health_plan?: any;
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

  const activityAnalysis = analysis.activity_analysis;
  const cardioAnalysis = analysis.cardiovascular_assessment;
  const sleepAnalysis = analysis.sleep_assessment;
  const overallPlan = analysis.overall_health_plan;

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
"""
        
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w') as f:
                f.write(content)
            self.log(f"Created {file_path}")
            self.created_files.append(str(file_path))
        except Exception as e:
            self.error(f"Failed to create HealthAnalysisPanel: {e}")
    
    def patch_personas_py(self):
        """Add health persona to app/personas.py"""
        file_path = self.repo_root / "app" / "personas.py"
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Check if health persona already exists
            if 'HEALTH' in content and 'health_assessment' in content:
                self.log(f"Health persona already exists in {file_path}, skipping patch")
                return
            
            # Add HEALTH to PersonaType enum
            enum_pattern = r'(class PersonaType\(str, Enum\):.*?PROPERTY_CASUALTY_CLAIMS = "property_casualty_claims")'
            enum_replacement = r'\1\n    HEALTH = "health"'
            content = re.sub(enum_pattern, enum_replacement, content, flags=re.DOTALL)
            
            # Add HEALTH_FIELD_SCHEMA before UNDERWRITING_DEFAULT_PROMPTS
            health_field_schema = '''
# =============================================================================
# HEALTH PERSONA CONFIGURATION
# =============================================================================

HEALTH_FIELD_SCHEMA = {
    "name": "HealthMetricsFields",
    "fields": {
        "StepsPerDay": {
            "type": "number",
            "description": "Average daily step count from Apple Health",
            "method": "extract",
            "estimateSourceAndConfidence": True
        },
        "VO2Max": {
            "type": "number",
            "description": "VO2 max value indicating cardiovascular fitness (mL/kg/min)",
            "method": "extract",
            "estimateSourceAndConfidence": True
        },
        "AverageSleepHours": {
            "type": "number",
            "description": "Average hours of sleep per night",
            "method": "extract",
            "estimateSourceAndConfidence": True
        },
        "HeartRateResting": {
            "type": "number",
            "description": "Resting heart rate in beats per minute",
            "method": "extract",
            "estimateSourceAndConfidence": True
        },
        "ActiveEnergy": {
            "type": "number",
            "description": "Active energy burned in kilocalories",
            "method": "extract",
            "estimateSourceAndConfidence": True
        }
    }
}

HEALTH_DEFAULT_PROMPTS = {
    "health_assessment": {
        "activity_analysis": """
You are a health and fitness expert analyzing Apple Health data.

Given the health metrics data in JSON format, analyze the user's activity level.

Focus on:
- Steps per day and activity classification
- Comparison to recommended daily activity
- Overall activity assessment

Return STRICT JSON:

{
  "activity_level": "Low | Moderate | High | Very High",
  "steps_per_day": "number",
  "classification": "Description of activity level",
  "recommendation": "Personalized recommendation based on current activity",
  "risk_assessment": "Low | Moderate | High"
}
        """,
        "cardiovascular_assessment": """
You are a cardiologist analyzing Apple Health data.

Given the health metrics including VO2 max, assess the user's cardiovascular health and fitness level.

Focus on:
- VO2 max value and fitness category
- Cardiovascular risk assessment
- Correlation with overall health

Return STRICT JSON:

{
  "vo2_max": "number",
  "fitness_category": "Poor | Fair | Good | Excellent | Superior",
  "cardio_risk": "Low | Low-Moderate | Moderate | Moderate-High | High",
  "assessment": "Clinical assessment of cardiovascular fitness",
  "recommendation": "Recommendation for cardiovascular health"
}
        """,
        "sleep_assessment": """
You are a sleep medicine expert analyzing Apple Health data.

Given the health metrics including average sleep hours, assess the user's sleep quality and patterns.

Focus on:
- Average sleep hours vs recommended 7-9 hours
- Sleep quality classification
- Impact on overall health

Return STRICT JSON:

{
  "avg_sleep_hours": "number",
  "sleep_quality": "Poor | Fair | Good | Excellent",
  "meets_guidelines": "boolean",
  "assessment": "Assessment of sleep quality and adequacy",
  "recommendation": "Recommendation for improving sleep"
}
        """,
        "overall_health_plan": """
You are a health and wellness coordinator synthesizing Apple Health data analysis.

Given the analysis of activity, cardiovascular fitness, and sleep metrics, create a comprehensive health plan.

Focus on:
- Overall health score
- Key areas of strength and concern
- Integrated recommendations
- Next steps for health improvement

Return STRICT JSON:

{
  "overall_health_score": "number between 1-100",
  "summary": "2-3 sentence executive summary of overall health status",
  "strengths": ["List of health areas that are performing well"],
  "areas_for_improvement": ["List of areas that need attention"],
  "integrated_recommendations": [
    {
      "priority": "High | Medium | Low",
      "action": "Specific actionable recommendation",
      "expected_benefit": "Expected benefit or outcome"
    }
  ],
  "next_steps": ["Specific next steps to implement"],
  "health_risk_category": "Low Risk | Moderate Risk | High Risk"
}
        """
    }
}

'''
            content = content.replace('UNDERWRITING_DEFAULT_PROMPTS = {', health_field_schema + '\nUNDERWRITING_DEFAULT_PROMPTS = {')
            
            # Add health persona to PERSONA_CONFIGS
            health_config = '''    PersonaType.HEALTH: PersonaConfig(
        id="health",
        name="Health & Wellness",
        description="Apple Health data analysis for personal health assessment and wellness planning",
        icon="❤️",
        color="#10b981",  # Green
        field_schema=HEALTH_FIELD_SCHEMA,
        default_prompts=HEALTH_DEFAULT_PROMPTS,
        custom_analyzer_id="healthAnalyzer",
        enabled=True,
    ),
'''
            # Find the PERSONA_CONFIGS dict and add before closing
            pattern = r'(PERSONA_CONFIGS: Dict\[PersonaType, PersonaConfig\] = \{[^}]+PersonaType\.CLAIMS:.*?\},)'
            match = re.search(pattern, content, re.DOTALL)
            if match:
                insertion_point = match.end() - 1
                content = content[:insertion_point] + '\n' + health_config + content[insertion_point:]
            
            with open(file_path, 'w') as f:
                f.write(content)
            self.log(f"Patched {file_path} with health persona")
            self.patched_files.append(str(file_path))
        except Exception as e:
            self.error(f"Failed to patch personas.py: {e}")
    
    def patch_api_server_py(self):
        """Add health endpoint to api_server.py"""
        file_path = self.repo_root / "api_server.py"
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Check if health endpoint already exists
            if '@app.post("/api/health")' in content:
                self.log(f"Health endpoint already exists in {file_path}, skipping patch")
                return
            
            # Add HealthDataRequest model after ChatRequest
            health_request_model = '''

class HealthDataRequest(BaseModel):
    """Request model for Apple Health data submission."""
    steps_per_day: float
    vo2_max: float
    avg_sleep_hours: float
    heart_rate_resting: Optional[float] = None
    active_energy: Optional[float] = None
    external_reference: Optional[str] = None
'''
            
            # Find ChatRequest class and insert after it
            chat_request_end = content.find('class ConversationSummary')
            if chat_request_end != -1:
                content = content[:chat_request_end] + health_request_model + '\n\nclass ConversationSummary' + content[chat_request_end + len('class ConversationSummary'):]
            
            # Add health endpoint before the main() function
            health_endpoint = '''

@app.post("/api/health")
async def submit_health_data(request: HealthDataRequest):
    """Submit Apple Health data and generate personalized health plan.
    
    Args:
        request: HealthDataRequest with health metrics
        
    Returns:
        ApplicationMetadata with generated health plan
    """
    try:
        settings = load_settings()
        app_id = str(uuid.uuid4())[:8]
        
        # Convert health metrics to structured JSON markdown
        health_data = {
            "activity": {
                "steps_per_day": request.steps_per_day,
                "activity_level": (
                    "High" if request.steps_per_day > 8000 else 
                    "Moderate" if request.steps_per_day > 5000 else 
                    "Low"
                )
            },
            "cardiovascular": {
                "vo2_max": request.vo2_max,
                "cardio_risk": (
                    "Low" if request.vo2_max >= 40 else 
                    "Moderate" if request.vo2_max >= 30 else 
                    "High"
                )
            },
            "sleep": {
                "avg_sleep_hours": request.avg_sleep_hours,
                "sleep_quality": (
                    "Good" if request.avg_sleep_hours >= 7 else 
                    "Poor"
                )
            },
            "resting_heart_rate": request.heart_rate_resting,
            "active_energy": request.active_energy,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        # Create markdown representation
        document_markdown = f"""# Apple Health Data Analysis

## Health Metrics Submitted
- **Steps Per Day**: {request.steps_per_day}
- **VO2 Max**: {request.vo2_max} mL/kg/min
- **Average Sleep Hours**: {request.avg_sleep_hours} hours
- **Resting Heart Rate**: {request.heart_rate_resting or "Not provided"} bpm
- **Active Energy**: {request.active_energy or "Not provided"} kcal

## Initial Assessment
- **Activity Level**: {health_data["activity"]["activity_level"]}
- **Cardiovascular Risk**: {health_data["cardiovascular"]["cardio_risk"]}
- **Sleep Quality**: {health_data["sleep"]["sleep_quality"]}

## Data Submitted
{json.dumps(health_data, indent=2)}
"""
        
        # Create ApplicationMetadata for health persona
        app_md = new_metadata(
            settings.app.storage_root,
            app_id,
            [],  # No files for health data
            external_reference=request.external_reference,
            persona="health",
        )
        
        # Set the document markdown with health data
        app_md.document_markdown = document_markdown
        
        # Run through health assessment prompts
        app_md = await asyncio.to_thread(
            run_underwriting_prompts,
            settings,
            app_md,
            sections_to_run=["health_assessment"],
            max_workers_per_section=4,
        )
        
        logger.info("Generated health plan for application %s", app_id)
        return application_to_dict(app_md)

    except Exception as e:
        logger.error("Failed to process health data: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
'''
            
            # Insert before main()
            main_pos = content.find('def main():')
            if main_pos != -1:
                content = content[:main_pos] + health_endpoint + '\n\n# Entry point for running with uvicorn directly\ndef main():' + content[main_pos + len('def main():'):]
            
            with open(file_path, 'w') as f:
                f.write(content)
            self.log(f"Patched {file_path} with health endpoint")
            self.patched_files.append(str(file_path))
        except Exception as e:
            self.error(f"Failed to patch api_server.py: {e}")
    
    def patch_frontend_page_tsx(self):
        """Add health persona rendering to frontend/src/app/page.tsx"""
        file_path = self.repo_root / "frontend" / "src" / "app" / "page.tsx"
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Check if health persona already handled
            if "currentPersona === 'health'" in content:
                self.log(f"Health persona rendering already exists in {file_path}, skipping patch")
                return
            
            # Add imports
            if "import HealthInputForm" not in content:
                import_line = "import AutomotiveClaimsOverview from '@/components/claims/AutomotiveClaimsOverview';"
                health_imports = """import AutomotiveClaimsOverview from '@/components/claims/AutomotiveClaimsOverview';
import HealthInputForm from '@/components/HealthInputForm';
import HealthAnalysisPanel from '@/components/HealthAnalysisPanel';"""
                content = content.replace(import_line, health_imports)
            
            # Add health case to renderContent switch
            automotive_case = """        if (currentPersona === 'automotive_claims') {
          return renderAutomotiveClaimsOverview();
        }"""
            
            health_case = """        if (currentPersona === 'automotive_claims') {
          return renderAutomotiveClaimsOverview();
        }

        if (currentPersona === 'health') {
          return renderHealthInput();
        }"""
            
            content = content.replace(automotive_case, health_case)
            
            # Add render functions before return statement
            render_functions = '''
  const renderHealthInput = () => {
    if (!selectedApp) {
      return (
        <div className="flex-1">
          <HealthInputForm 
            onSuccess={handleHealthSuccess}
            onLoading={setLoading}
          />
        </div>
      );
    }

    return (
      <div className="flex-1 overflow-auto">
        <HealthAnalysisPanel result={selectedApp} />
      </div>
    );
  };

  const handleHealthSuccess = async (result: ApplicationMetadata) => {
    setSelectedApp(result);
    
    try {
      const response = await fetch(`/api/applications?persona=health`, {
        cache: 'no-store',
      });
      if (response.ok) {
        const apps = await response.json();
        setApplications(apps);
      }
    } catch (err) {
      console.error('Failed to reload applications:', err);
    }
  };

'''
            
            # Find the return statement and insert before it
            return_pos = content.rfind('  return (')
            if return_pos != -1:
                content = content[:return_pos] + render_functions + '\n  return (' + content[return_pos + len('  return ('):]
            
            with open(file_path, 'w') as f:
                f.write(content)
            self.log(f"Patched {file_path} with health persona rendering")
            self.patched_files.append(str(file_path))
        except Exception as e:
            self.error(f"Failed to patch frontend page.tsx: {e}")
    
    def run(self):
        """Execute the full setup"""
        print("🚀 Setting up Apple Health feature for WorkbenchIQ\n")
        
        # Create new files
        print("Creating new files...")
        self.create_health_prompts_json()
        self.create_health_input_form()
        self.create_health_analysis_panel()
        
        # Patch existing files
        print("\nPatching existing files...")
        self.patch_personas_py()
        self.patch_api_server_py()
        self.patch_frontend_page_tsx()
        
        # Summary
        print("\n" + "="*60)
        print("SETUP COMPLETE")
        print("="*60)
        print(f"\n✓ Created {len(self.created_files)} new files:")
        for f in self.created_files:
            print(f"  • {f}")
        
        print(f"\n✓ Patched {len(self.patched_files)} existing files:")
        for f in self.patched_files:
            print(f"  • {f}")
        
        if self.errors:
            print(f"\n⚠ {len(self.errors)} errors encountered:")
            for err in self.errors:
                print(f"  • {err}")
            return False
        
        print("\n✓ All setup steps completed successfully!")
        print("\nNext steps:")
        print("1. Test the health endpoint with: curl -X POST http://localhost:8000/api/health \\")
        print("   -H 'Content-Type: application/json' \\")
        print("   -d '{\"steps_per_day\": 9200, \"vo2_max\": 42, \"avg_sleep_hours\": 7.5}'")
        print("2. Open http://localhost:3000 and select the 'Health & Wellness' persona")
        print("3. Fill out the health form and click 'Analyze My Health'")
        return True


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        repo_root = sys.argv[1]
    else:
        repo_root = "."
    
    setup = HealthFeatureSetup(repo_root)
    success = setup.run()
    sys.exit(0 if success else 1)
