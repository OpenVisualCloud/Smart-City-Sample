{{/*
Expand the number of offices.
*/}}
{{- define "smtc.noffices" }}
{{- if eq .scenarioName "traffic" }}
{{- min (len .Values.officeLocations.traffic) .Values.noffices }}
{{- else if eq .scenarioName "stadium" }}
{{- min (len .Values.officeLocations.stadium) .Values.noffices }}
{{- end }}
{{- end }}

{{/*
Expand the database name.
*/}}
{{- define "smtc.db.name" }}
{{- if gt (int .Values.noffices) 1 }}
{{- "cloud-db" }}
{{- else }}
{{- "db" }}
{{- end }}
{{- end }}

{{/*
Expand to the office db name 
*/}}
{{- define "smtc.env.dbhost" }}
{{- if gt (int .Values.noffices) 1 }}
{{- printf "http://%s-db-service:9200" .officeName }}
{{- else }}
{{- "http://db-service:9200" }}
{{- end }}
{{- end }}

{{/*
Expand to either .Values.ncameras.traffic or .Values.ncameras.svcq
*/}}
{{- define "smtc.ncameras" }}
{{- if eq .scenarioName "traffic" }}
{{- .Values.ncameras.traffic }}
{{- else if eq .scenarioName "stadium" }}
{{- .Values.ncameras.svcq }}
{{- end }}
{{- end }}

{{/*
Expand to either .Values.nanalytics.traffic or .Values.nanalytics.svcq
*/}}
{{- define "smtc.nanalytics" }}
{{- if eq .scenarioName "traffic" }}
{{- .Values.nanalytics.traffic }}
{{- else if eq .scenarioName "stadium" }}
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
{{- index .Values.officeLocations.traffic .officeIdx }}
{{- else if eq .scenarioName "stadium" }}
{{- index .Values.officeLocations.stadium .officeIdx }}
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
                  operator: NotIn
                  values:
                    - "yes"
{{- end }}

{{/*
Expand the platform accel-selector.
*/}}
{{- define "smtc.platform.accel-selector" -}}
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
Expand the platform device name.
*/}}
{{- define "smtc.platform.device" }}
{{- if eq "vcac-a" ( include "smtc.platform.suffix" . ) }}
{{- "hddl" }}
{{- else }}
{{- "cpu" }}
{{- end }}
{{- end }}

{{/*
Extract the hostname from connector.host
*/}}
{{- define "smtc.connector.cloud.hostname" }}
{{- regexReplaceAll ".*@" .Values.connector.cloudHost "" }}
{{- end }}

{{/*
Connector DBHost
*/}}
{{- define "smtc.connector.dbhost" }}
{{- if (len .Values.connector.cloudHost) }}
{{- printf "localhost:%d" (int .Values.connector.cloudQueryPort) }}
{{- else }}
{{- "cloud-db-service:9200" }}
{{- end }}
{{- end }}
