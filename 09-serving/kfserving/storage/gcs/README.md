gcloud iam service-accounts keys create gcp-sa-credentials.json \
  --iam-account [SA-NAME]@[PROJECT-ID].iam.gserviceaccount.com
  
  
kubectl -n [NAMESPACE] create secret generic user-gcp-sa \
  --from-file=gcloud-application-credentials.json=gcp-sa-credentials.json