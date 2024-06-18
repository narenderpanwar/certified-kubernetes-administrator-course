cd investindia-sws-infra && git pull && cd ../
service_name="$1"
namespace="$2"
if [ "$3" != "" ];  then
  image_tag="$3"
else
  image_tag=$(kubectl get deployment $service_name -o=jsonpath='{.spec.template.spec.containers[0].image}' -n $namespace | cut -d':' -f2)
fi
echo "$image_tag"
helm uninstall $namespace-$service_name --namespace $namespace
helm upgrade --install --namespace $namespace --kubeconfig=kube-non-prod-config $namespace-$service_name --set image.tag=$image_tag -f ./investindia-sws-infra/sws/eks/dev/app-setup-new/$service_name/values-dev.yaml ./investindia-sws-infra/sws/eks/dev/app-setup-new/$service_name
