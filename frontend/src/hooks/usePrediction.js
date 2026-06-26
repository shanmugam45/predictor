import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { predictionService } from '../services/predictionService'
import toast from 'react-hot-toast'

export function usePrediction() {
  const qc = useQueryClient()

  const predictMutation = useMutation({
    mutationFn: predictionService.predict,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['predictions'] }),
    onError: (e) => toast.error(e.message),
  })

  const batchMutation = useMutation({
    mutationFn: predictionService.predictBatch,
    onSuccess: () => { toast.success('Batch prediction complete'); qc.invalidateQueries({ queryKey: ['predictions'] }) },
    onError: (e) => toast.error(e.message),
  })

  const historyQuery = useQuery({
    queryKey: ['predictions'],
    queryFn: () => predictionService.list({}),
  })

  return { predictMutation, batchMutation, historyQuery }
}
