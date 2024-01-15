import time

import yaml
from kubernetes import client, config, utils
from kubernetes.client.rest import ApiException


config.load_kube_config()
v1 = client.CoreV1Api()


name = "pool1"
namespace = "datalayer"


def delete_pod():
    try:
        api_response = v1.delete_namespaced_pod(name, namespace)
        print(api_response)
    except ApiException as e:
        print("Exception when calling delete_namespaced_pod: %s\n" % e)


def create_pod():
    specs = yaml.safe_load(f"""
apiVersion: v1
kind: Pod
metadata:
  name: {name}
  namespace: {namespace}
  labels:
    app: jupyterpool
spec:
  hostname: {name}
  subdomain: jupyterpool
  containers:
  - name: jupyterpool
    image: datalayer/jupyterpool:0.0.7
#    imagePullPolicy: Always
    ports:
    - containerPort: 2300
      protocol: TCP
""")
    api_response = v1.create_namespaced_pod(body=specs, namespace=namespace)
    while True:
        try:
            api_response = v1.read_namespaced_pod(name=name, namespace=namespace)
            if api_response.status.phase != 'Pending':
                break
            time.sleep(1)
        except ApiException as e:
            print(e)
            time.sleep(1)
    print(f'Pod {name} in {namespace} created.')
    print(api_response)
    return name


def list_pods():
    print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        print(f"{i.status.pod_ip}\t{i.metadata.name}\t{i.metadata.namespace}")


def main():
    delete_pod()
    time.sleep(1)
    create_pod()
    time.sleep(1)
#    list_pods()


if __name__ == '__main__':
    main()
