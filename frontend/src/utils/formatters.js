export const gradeColors = {
  'O':  'bg-purple-100 text-purple-800',
  'A+': 'bg-emerald-100 text-emerald-800',
  'A':  'bg-green-100 text-green-800',
  'B+': 'bg-blue-100 text-blue-800',
  'B':  'bg-sky-100 text-sky-800',
  'C+': 'bg-yellow-100 text-yellow-800',
  'C':  'bg-orange-100 text-orange-800',
  'F':  'bg-red-100 text-red-800',
}

export function formatMark(value) {
  if (value == null) return '—'
  return `${Number(value).toFixed(1)}%`
}

export function formatDate(dateString) {
  if (!dateString) return '—'
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric', month: 'short', day: 'numeric',
  })
}

export function markToGrade(mark) {
  if (mark >= 90) return 'O'
  if (mark >= 80) return 'A+'
  if (mark >= 75) return 'A'
  if (mark >= 70) return 'B+'
  if (mark >= 65) return 'B'
  if (mark >= 60) return 'C+'
  if (mark >= 50) return 'C'
  return 'F'
}
