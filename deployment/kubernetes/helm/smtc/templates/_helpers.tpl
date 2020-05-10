{{/*
Expand the number of offices.
*/}}
{{- define "smtc.nOffices" }}
{{- if eq .scenarioName "stadium" }}
{{- 1 }}
{{- else }}
{{- .nOffices }}
{{- end }}
{{- end }}

{{/*
Expand the database name.
*/}}
{{- define "smtc.db.name" -}}
{{- if gt (int .Values.nOffices) 1 }}
{{- "cloud-db" }}
{{- else }}
{{- "db" }}
{{- end }}
{{- end }}

{{/*
Expand the analytics replicas.
*/}}
{{- define "smtc.analytics" -}}
{{- (split "," (toString .Values.nAnalytics))._0 }}
{{- end }}

{{/*
Expand the analytics replicas.
*/}}
{{- define "smtc.analytics2" -}}
{{- $a0 := (split "," (toString .Values.nAnalytics))._0 }}
{{- $a1 := (split "," (toString .Values.nAnalytics))._1 }}
{{- $a2 := (split "," (toString .Values.nAnalytics))._2 }}
{{- if $a1 }}
{{- $a1 }}
{{- else }}
{{- $a0 }}
{{- end }}
{{- end }}

{{/*
Expand the analytics replicas.
*/}}
{{- define "smtc.analytics3" -}}
{{- $a0 := (split "," (toString .Values.nAnalytics))._0 }}
{{- $a1 := (split "," (toString .Values.nAnalytics))._1 }}
{{- $a2 := (split "," (toString .Values.nAnalytics))._2 }}
{{- if $a2 }}
{{- $a2 }}
{{- else if $a1 }}
{{- $a1 }}
{{- else }}
{{- $a0 }}
{{- end }}
{{- end }}

{{/*
Expand the camera replicas.
*/}}
{{- define "smtc.cameras" -}}
{{- int (split "," (toString .Values.nCameras))._0 }}
{{- end }}

{{/*
Expand the camera replicas.
*/}}
{{- define "smtc.cameras2" -}}
{{- $a0 := (split "," (toString .Values.nCameras))._0 }}
{{- $a1 := (split "," (toString .Values.nCameras))._1 }}
{{- $a2 := (split "," (toString .Values.nCameras))._2 }}
{{- if $a1 }}
{{- int $a1 }}
{{- else }}
{{- int $a0 }}
{{- end }}
{{- end }}

{{/*
Expand the camera replicas.
*/}}
{{- define "smtc.cameras3" -}}
{{- $a0 := (split "," (toString .Values.nCameras))._0 }}
{{- $a1 := (split "," (toString .Values.nCameras))._1 }}
{{- $a2 := (split "," (toString .Values.nCameras))._2 }}
{{- if $a2 }}
{{- int $a2 }}
{{- else if $a1 }}
{{- int $a1 }}
{{- else }}
{{- int $a0 }}
{{- end }}
{{- end }}

{{/*
Expand the platform suffix.
*/}}
{{- define "smtc.platform.suffix" -}}
{{ lower .Values.platform }}
{{- end }}

{{/*
Expand the platform volume mounts.
*/}}
{{- define "smtc.platform.mounts" -}}
{{- if eq "vcac-a" ( include "smtc.platform.suffix" . ) }}
            - mountPath: /var/tmp
              name: var-tmp
#          resources:
#            limits:
#              vpu.intel.com/hddl: 1
#              gpu.intel.com/i915: 1
          securityContext:
            privileged: true
{{- end }}
{{- end }}

{{/*
Expand the platform volumes.
*/}}
{{- define "smtc.platform.volumes" -}}
{{- if eq "vcac-a" ( include "smtc.platform.suffix" . ) }}
          - name: "var-tmp"
            hostPath:
              path: /var/tmp
              type: Directory
{{- end }}
{{- end }}

{{/*
Office location
*/}}
{{- define "smtc.office.location" -}}
{{- if eq .scenarioName "traffic" }}
              value: {{ index .locations.traffic .officeIdx | quote }}
{{- else if eq .scenarioName "stadium" }}
              value: {{ index .locations.stadium .officeIdx | quote }}
{{- end }}
{{- end }}

{{/*
Expand the platform nodeSelector.
*/}}
{{- define "smtc.platform.node-selector" -}}
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
              - matchExpressions:
                - key: "vcac-zone"
                  {{- if eq "vcac-a" ( include "smtc.platform.suffix" . ) }}
                  operator: In
                  {{- else }}
                  operator: NotIn
                  {{- end }}
                  values:
                    - "yes"
{{- end }}

{{/*
Expand Linux user id, if provided.
*/}}
{{- define "smtc.user.id" -}}
{{- if $.Values.userID }}
{{- .Values.userID }}
{{- else }}
{{- 0 }}
{{- end }}
{{- end }}

{{/*
Expand Linux user group, if provided.
*/}}
{{- define "smtc.user.group" -}}
{{- if $.Values.userID }}
{{- .Values.groupID }}
{{- else }}
{{- 0 }}
{{- end }}
{{- end }}
