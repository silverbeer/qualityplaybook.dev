{{/*
Expand the name of the chart.
*/}}
{{- define "qualityplaybook.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "qualityplaybook.labels" -}}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Frontend labels
*/}}
{{- define "qualityplaybook.frontend.labels" -}}
{{ include "qualityplaybook.labels" . }}
app: qualityplaybook-frontend
app.kubernetes.io/name: qualityplaybook-frontend
app.kubernetes.io/component: frontend
{{- end }}

{{/*
Backend labels
*/}}
{{- define "qualityplaybook.backend.labels" -}}
{{ include "qualityplaybook.labels" . }}
app: qualityplaybook-backend
app.kubernetes.io/name: qualityplaybook-backend
app.kubernetes.io/component: backend
{{- end }}
