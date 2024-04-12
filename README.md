# Using Docker

## To run the app:

```
docker-compose up --build
```

## To access the app:

http://localhost:8090

## To stop the app:

```
docker-compose down
```



# Using Kubernetes

Assuming minikube is installed:

## To start minikube:

```
minikube start
```

## To deploy the app:

```
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

## To access the app:

```
minikube service background-removal-service
```

## Scale the app:

```
kubectl scale deployment background-removal-deployment --replicas=4
```

## To stop the app:

```
kubectl delete deployment background-removal-deployment
kubectl delete service background-removal-service
```

## To stop minikube:

```
minikube stop
```

# Ansible Playbook

## To run the playbook:

```
ansible-playbook ansible/deploy_app.yml -e kubeconfig_path=~/.kube/config
```

## To stop:

```
ansible-playbook ansible/stop_app.yml -e kubeconfig_path=~/.kube/config
```

