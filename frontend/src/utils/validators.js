export function validatePredictionForm(data) {
  const errors = {}
  if (data.attendance_percentage === '' || data.attendance_percentage == null)
    errors.attendance_percentage = 'Required'
  else if (data.attendance_percentage < 0 || data.attendance_percentage > 100)
    errors.attendance_percentage = 'Must be 0–100'

  if (data.study_hours_per_week === '' || data.study_hours_per_week == null)
    errors.study_hours_per_week = 'Required'
  else if (data.study_hours_per_week < 0 || data.study_hours_per_week > 168)
    errors.study_hours_per_week = 'Must be 0–168'

  if (data.previous_gpa === '' || data.previous_gpa == null)
    errors.previous_gpa = 'Required'
  else if (data.previous_gpa < 0 || data.previous_gpa > 10)
    errors.previous_gpa = 'Must be 0–10'

  if (data.internal_mark_1 === '' || data.internal_mark_1 == null)
    errors.internal_mark_1 = 'Required'
  else if (data.internal_mark_1 < 0 || data.internal_mark_1 > 100)
    errors.internal_mark_1 = 'Must be 0–100'

  if (data.internal_mark_2 === '' || data.internal_mark_2 == null)
    errors.internal_mark_2 = 'Required'
  else if (data.internal_mark_2 < 0 || data.internal_mark_2 > 100)
    errors.internal_mark_2 = 'Must be 0–100'

  if (data.assignment_score === '' || data.assignment_score == null)
    errors.assignment_score = 'Required'
  else if (data.assignment_score < 0 || data.assignment_score > 100)
    errors.assignment_score = 'Must be 0–100'

  return errors
}
