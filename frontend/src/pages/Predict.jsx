import { useState, useCallback } from 'react'
import { usePrediction } from '../hooks/usePrediction'
import PredictionForm from '../components/predictions/PredictionForm'
import PredictionResult from '../components/predictions/PredictionResult'
import { Clock } from 'lucide-react'
import { formatMark, formatDate, gradeColors } from '../utils/formatters'

export default function Predict() {
  const [result, setResult] = useState(null)
  const { predictMutation, historyQuery } = usePrediction()

  const handlePredict = useCallback((data) => {
    predictMutation.mutate(data, { onSuccess: (res) => setResult(res) })
  }, [predictMutation])

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Left: Form */}
      <div className="card space-y-6">
        <div>
          <h2 className="font-semibold text-gray-900">Enter Student Data</h2>
          <p className="text-sm text-gray-500 mt-1">Fill in the academic metrics to predict the final mark.</p>
        </div>
        <PredictionForm onSubmit={handlePredict} isLoading={predictMutation.isPending} />
        {predictMutation.isError && (
          <p className="text-sm text-red-600 bg-red-50 rounded-lg px-3 py-2">{predictMutation.error?.message}</p>
        )}
        {result && <PredictionResult result={result} />}
      </div>

      {/* Right: History */}
      <div className="card space-y-4">
        <div className="flex items-center gap-2">
          <Clock className="w-4 h-4 text-gray-400" />
          <h2 className="font-semibold text-gray-900">Recent Predictions</h2>
        </div>
        {historyQuery.isLoading ? (
          <p className="text-sm text-gray-400">Loading…</p>
        ) : historyQuery.data?.items?.length === 0 ? (
          <p className="text-sm text-gray-400 py-4 text-center">No predictions yet</p>
        ) : (
          <div className="space-y-2 max-h-[500px] overflow-y-auto pr-1">
            {historyQuery.data?.items?.slice(0, 15).map((p) => (
              <div key={p.id} className="flex items-center justify-between px-3 py-2 bg-gray-50 rounded-lg">
                <div>
                  <span className="text-sm font-semibold text-gray-900">{formatMark(p.predicted_mark)}</span>
                  <span className="text-xs text-gray-400 ml-2">{formatDate(p.created_at)}</span>
                </div>
                <span className={`badge ${gradeColors[p.predicted_grade] || 'bg-gray-100 text-gray-600'}`}>
                  {p.predicted_grade}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
