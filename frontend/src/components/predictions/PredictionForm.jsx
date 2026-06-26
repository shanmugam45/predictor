import { useState, useCallback, memo } from 'react'
import { validatePredictionForm } from '../../utils/validators'
import { Brain } from 'lucide-react'

const DEFAULTS = {
  attendance_percentage: '',
  study_hours_per_week: '',
  previous_gpa: '',
  internal_mark_1: '',
  internal_mark_2: '',
  assignment_score: '',
  lab_score: '',
  participation_score: '',
}

const Field = memo(({ label, name, min, max, step = '0.1', required, value, error, onChange, onKeyDown, onPaste }) => (
  <div>
    <label className="label">{label}{required && ' *'}</label>
    <input
      name={name}
      type="text"
      inputMode="decimal"
      autoComplete="off"
      spellCheck="false"
      className={`input-field ${error ? 'border-red-400' : ''}`}
      value={value}
      onChange={onChange}
      onKeyDown={onKeyDown}
      onPaste={onPaste}
      placeholder={`${min}–${max}`}
    />
    {error && <p className="text-xs text-red-500 mt-1">{error}</p>}
  </div>
))

const PredictionForm = memo(function PredictionForm({ onSubmit, isLoading }) {
  const [form, setForm] = useState(DEFAULTS)
  const [errors, setErrors] = useState({})

  const sanitizeNumericInput = useCallback((value) => {
    const cleaned = value.replace(/[^0-9.]/g, '')
    return cleaned.replace(/(\..*)\./g, '$1')
  }, [])

  const handleFieldChange = useCallback(
    (e) => {
      const { name, value } = e.target
      setForm((prev) => ({ ...prev, [name]: sanitizeNumericInput(value) }))
    },
    [sanitizeNumericInput],
  )

  const handleFieldPaste = useCallback(
    (e) => {
      e.preventDefault()
      const { name } = e.target
      const pasted = e.clipboardData.getData('text')
      setForm((prev) => ({ ...prev, [name]: sanitizeNumericInput(pasted) }))
    },
    [sanitizeNumericInput],
  )

  const numericKeyDown = useCallback((e) => {
    if (e.ctrlKey || e.metaKey || e.altKey) return
    const allowed = [
      'Backspace', 'Tab', 'Enter', 'Escape',
      'ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown',
      'Delete', 'Home', 'End', '.',
    ]
    if (allowed.includes(e.key)) return
    if (/^[0-9]$/.test(e.key)) return
    e.preventDefault()
  }, [])

  const handleSubmit = (e) => {
    e.preventDefault()
    const errs = validatePredictionForm(form)
    if (Object.keys(errs).length) { setErrors(errs); return }
    setErrors({})

    const converted = Object.fromEntries(
      Object.entries(form).map(([k, v]) => [k, v === '' ? null : Number(v)])
    )
    const payload = {
      attendance_percentage: converted.attendance_percentage,
      study_hours_per_week: converted.study_hours_per_week,
      previous_gpa: converted.previous_gpa,
      internal_mark_1: converted.internal_mark_1,
      internal_mark_2: converted.internal_mark_2,
      assignment_score: converted.assignment_score,
      lab_score: converted.lab_score,
      participation_score: converted.participation_score,
    }

    if (onSubmit) {
      onSubmit(payload)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      <div className="grid grid-cols-2 gap-4">
        <Field
          label="Attendance (%)"
          name="attendance_percentage"
          min={0}
          max={100}
          required
          value={form.attendance_percentage}
          error={errors.attendance_percentage}
          onChange={handleFieldChange}
          onKeyDown={numericKeyDown}
          onPaste={handleFieldPaste}
        />
        <Field
          label="Study Hours/Week"
          name="study_hours_per_week"
          min={0}
          max={168}
          step="0.5"
          required
          value={form.study_hours_per_week}
          error={errors.study_hours_per_week}
          onChange={handleFieldChange}
          onKeyDown={numericKeyDown}
          onPaste={handleFieldPaste}
        />
        <Field
          label="Previous GPA (0–10)"
          name="previous_gpa"
          min={0}
          max={10}
          step="0.01"
          required
          value={form.previous_gpa}
          error={errors.previous_gpa}
          onChange={handleFieldChange}
          onKeyDown={numericKeyDown}
          onPaste={handleFieldPaste}
        />
        <Field
          label="Internal Mark 1"
          name="internal_mark_1"
          min={0}
          max={100}
          required
          value={form.internal_mark_1}
          error={errors.internal_mark_1}
          onChange={handleFieldChange}
          onKeyDown={numericKeyDown}
          onPaste={handleFieldPaste}
        />
        <Field
          label="Internal Mark 2"
          name="internal_mark_2"
          min={0}
          max={100}
          required
          value={form.internal_mark_2}
          error={errors.internal_mark_2}
          onChange={handleFieldChange}
          onKeyDown={numericKeyDown}
          onPaste={handleFieldPaste}
        />
        <Field
          label="Assignment Score"
          name="assignment_score"
          min={0}
          max={100}
          required
          value={form.assignment_score}
          error={errors.assignment_score}
          onChange={handleFieldChange}
          onKeyDown={numericKeyDown}
          onPaste={handleFieldPaste}
        />
        <Field
          label="Lab Score (optional)"
          name="lab_score"
          min={0}
          max={100}
          value={form.lab_score}
          error={errors.lab_score}
          onChange={handleFieldChange}
          onKeyDown={numericKeyDown}
          onPaste={handleFieldPaste}
        />
        <Field
          label="Participation Score (optional)"
          name="participation_score"
          min={0}
          max={100}
          value={form.participation_score}
          error={errors.participation_score}
          onChange={handleFieldChange}
          onKeyDown={numericKeyDown}
          onPaste={handleFieldPaste}
        />
      </div>
      <button type="submit" className="btn-primary w-full justify-center gap-2" disabled={isLoading}>
        <Brain className="w-4 h-4" />
        {isLoading ? 'Predicting…' : 'Predict Final Mark'}
      </button>
    </form>
  )
})

export default PredictionForm
