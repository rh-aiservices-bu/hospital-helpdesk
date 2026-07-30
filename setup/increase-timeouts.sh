#!/usr/bin/env bash
# Increases the model serving and AI stack timeouts for CPU inference.
# Run this from the OpenShift web terminal if the Playground times out on CPU.
#
# What this does:
#   1. Sets the InferenceService predictor timeout to 700s
#   2. Sets the Llama Stack ConfigMap read timeout to 600s
#   3. Restarts the Llama Stack deployment to pick up the new timeout

set -e

NAMESPACE="hospital-helpdesk"

echo "==> Increasing InferenceService predictor timeout to 700s..."
IS_NAME=$(oc get inferenceservice -n "$NAMESPACE" -o jsonpath='{.items[0].metadata.name}')
oc patch inferenceservice -n "$NAMESPACE" "$IS_NAME" \
  --type=json \
  -p '[{"op":"replace","path":"/spec/predictor/timeout","value":700}]'
echo "    Done (InferenceService: $IS_NAME)"

echo "==> Increasing Llama Stack read timeout to 600s..."
python3 -c "
import subprocess, json, re
cm = json.loads(subprocess.run(
    ['oc','get','configmap','llama-stack-config','-n','$NAMESPACE','-o','json'],
    capture_output=True, text=True).stdout)
cm['data']['config.yaml'] = re.sub(r'read:\s*\d+', 'read: 600', cm['data']['config.yaml'])
subprocess.run([
    'oc','patch','configmap','llama-stack-config','-n','$NAMESPACE',
    '--type=merge','-p', json.dumps({'data': {'config.yaml': cm['data']['config.yaml']}})
])
"
echo "    Done"

echo "==> Restarting Llama Stack to apply new timeout..."
oc rollout restart deployment/lsd-genai-playground -n "$NAMESPACE"
oc rollout status deployment/lsd-genai-playground -n "$NAMESPACE"
echo "    Done"

echo ""
echo "Timeouts updated. The model now has up to 10 minutes to respond."
