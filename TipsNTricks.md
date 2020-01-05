### Fun stuff you can do with kubernetes

Enable command completion with the following.

``` bash
echo "source (kubectl completion bash)"  >> ~/.bash_profile
```

Sort pods by creation time.

``` bash
kubectl get pods -n kube-system --sort-by=metadata.creationTimeStamp
```

Specify output type.

``` bash
kubectl get pods -n kube-system <name> --output=yaml/json/wide/
```

Show pods with ips.

``` bash
kubectl get pods -n kube-system -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.podIP}{"\n"}{end}'
```

Generate a manifest file for a namespace.

``` bash
kubectl create namespace tips -o yaml --dry-run
```

Create nginx deployment.

``` bash
kubectl run nginx --image=nginx --port=80 --replicas=2 --expose --dry-run -o yaml
```

Export pod information without cluster specific informations.

``` bash
kubectl get pod -n kube-system <podname> -o yaml --export 
```

Explain details of a kube resource.

``` bash
kubectl explain pod | more
kubectl explain pod.spec.containers.resources | more
```