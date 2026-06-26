import { gradeColors, formatMark } from '../../utils/formatters'
import { Target, Cpu } from 'lucide-react'

export default function PredictionResult({ result }) {
  if (!result) return null
  const { predicted_mark, predicted_grade, confidence_score, model_version } = result

  return (
    <div className="rounded-2xl border-2 border-primary-100 bg-primary-50 p-6 text-center space-y-4">
      <p className="text-sm font-medium text-primary-600 uppercase tracking-wider">Prediction Result</p>

      <div className="flex items-center justify-center gap-6">
        <div>
          <p className="text-5xl font-bold text-gray-900">{formatMark(predicted_mark)}</p>
          <p className="text-sm text-gray-500 mt-1">Predicted Final Mark</p>
        </div>
        <div className={`px-5 py-3 rounded-xl text-2xl font-bold ${gradeColors[predicted_grade] || 'bg-gray-100 text-gray-700'}`}>
          {predicted_grade}
        </div>
      </div>

      <div className="flex justify-center gap-6 text-sm text-gray-500 pt-2">
        {confidence_score != null && (
          <div className="flex items-center gap-1.5">
            <Target className="w-4 h-4" />
            <span>Confidence: {(confidence_score * 100).toFixed(1)}%</span>
          </div>
        )}
        {model_version && (
          <div className="flex items-center gap-1.5">
            <Cpu className="w-4 h-4" />
            <span>{model_version}</span>
          </div>
        )}
      </div>
    </div>
  )
}
