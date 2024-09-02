import os
import time
import requests
import pytest

kubeconfig = os.getenv("KUBECONFIG")
ocp_hub_version = os.getenv("OCP_HUB_VERSION")
mch_ns = os.getenv("MCH_NAMESPACE")

@pytest.mark.parametrize("endpoint", [
    {"cmd": f"oc --kubeconfig {kubeconfig} whoami --show-console", "response": 200},
    {"cmd": f"oc --kubeconfig {kubeconfig} get managedcluster local-cluster -ojsonpath='{{.spec.managedClusterClientConfigs[0].url}}'", "response": 403},
])
def test_http_endpoint(bash, endpoint):
    if "url" in endpoint:
        url = endpoint.url
    else:
        oc_cmd = endpoint['cmd']
        url = bash.run_script_inline([oc_cmd])
    response = requests.get(url, verify=False)
    assert response.status_code == endpoint["response"], f"Endpoint {url} is not accessible. Status code: {response.status_code}"

def test_cluster_version(bash):
    oc_cmd = "oc get clusterversion version -ojsonpath='{.status.desired.version}'"
    assert bash.run_script_inline([oc_cmd]).startswith(f"{ocp_hub_version}")

@pytest.mark.parametrize("namespace", [
    "openshift-local-storage",
    f"{mch_ns}",
    "multicluster-engine",
    "openshift-gitops",
])
def test_ztp_namespaces(bash, namespace):
    oc_cmd = f"oc get ns {namespace} " + "-ojsonpath='{.metadata.name}'"
    assert bash.run_script_inline([oc_cmd]) == namespace

    count = 0
    attempts = 10
    while attempts > 0:
      oc_cmd = f"oc -n {namespace} get po --no-headers | grep -v -E 'Running|Completed' | wc -l"
      if bash.run_script_inline([oc_cmd]) == '0':
        break
      attempts -= 1
      time.sleep(60)
    assert attempts > 0, f"Not all PODs in {namespace} namespace are ready yet"
