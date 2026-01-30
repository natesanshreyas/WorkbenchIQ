'use client';

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
