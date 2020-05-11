{{/*
Expand the number of offices.
*/}}
{{- define "smtc.noffices" }}
{{- if eq .scenarioName "traffic" }}
{{- min (len .Values.officeLocations.traffic) .Values.nOffices }}
{{- else }}
{{- min (len .Values.officeLocations.stadium) .Values.nOffices }}
{{- end }}
{{- end }}

{{/*
Expand the database name.
*/}}
{{- define "smtc.db.name" }}
{{- if gt (int .Values.nOffices) 1 }}
{{- "cloud-db" }}
{{- else }}
{{- "db" }}
{{- end }}
{{- end }}

{{/*
Expand to the office db name 
*/}}
{{- define "smtc.env.dbhost" }}
{{- if gt (int .Values.nOffices) 1 }}
              value: {{ ( .officeName ) | printf "http://%s-db-service:9200" | quote }}
{{- else }}
              value: "http://db-service:9200"
{{- end }}
{{- end }}

{{/*
Expand to either .Values.ncameras.traffic or .Values.ncameras.svcq
*/}}
{{- define "smtc.ncameras" }}
{{- if eq .scenarioName "traffic" }}
{{- .Values.ncameras.traffic }}
{{- else }}
{{- .Values.ncameras.svcq }}
{{- end }}
{{- end }}

{{/*
Expand to either .Values.nanalytics.traffic or .Values.nanalytics.svcq
*/}}
{{- define "smtc.nanalytics" }}
{{- if eq .scenarioName "traffic" }}
{{- .Values.nanalytics.traffic }}
{{- else }}
{{- .Values.nanalytics.svcq }}
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
{{- define "smtc.env.office" -}}
{{- if eq .scenarioName "traffic" }}
              value: {{ index .Values.officeLocations.traffic .officeIdx | quote }}
{{- else if eq .scenarioName "stadium" }}
              value: {{ index .Values.officeLocations.stadium .officeIdx | quote }}
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
