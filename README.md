# Informacion para la prueba de Integracion Api Manager con Service Mesh

## Service Mesh con Istio

### Documentación
[Documentacion de Istio](https://istio.io/latest/docs/setup/getting-started/)

### Abrir el Istio para ingresar
Ubicacion de Istio:
```bash
cd C:\Program Files\istio-1.26.0\bin
```

### Construir los contenedores
Vamos a la parte de las carpetas para poner las siguientes builds de la parte de docker
```bash
docker build -t auth-service ./auth
docker build -t order-service ./order
docker build -t payment-service ./payment
```

### Creacion de kind para soporte de ingress
---
```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  extraPortMappings:
  - containerPort: 80
    hostPort: 8080
```
---

### Subir las imagenes del docker al kind
```bash
kind load docker-image auth-service --name istio-mesh
kind load docker-image order-service --name istio-mesh
kind load docker-image payment-service --name istio-mesh
```

### Aplicar los manifiestos YAML en la parte del kubectl:
```bash
kubectl apply -f proxi/auth-service.yml
kubectl apply -f proxi/order-service.yml
kubectl apply -f proxi/payment-service.yml
```

### Eliminar los manifiestos YAML en la parte del kubectl:
```bash
kubectl delete -f proxi/auth-service.yml
kubectl delete -f proxi/order-service.yml
kubectl delete -f proxi/payment-service.yml
```

### Verificamos los pods y servicios esten corriendo
```bash
kubectl get pods
kubectl get svc
kubectl get gateway
kubectl get virtualservice
```

### Realizar el port forwarding para comunicar los servicios
```bash
kubectl port-forward svc/auth-service 5000:5000
kubectl port-forward svc/order-service 5001:5001
kubectl port-forward svc/payment-service 5002:5002
```

## API GATEWAY con WSO2:

### Documentación
[Documentacion de WSO2](https://apim.docs.wso2.com/en/latest/install-and-setup/install/installing-the-product/running-the-api-m/)

### Abrir el WS02 e ingresar
Ubicacion de WSO2:
```bash
cd C:\Users\user\GitRepositories\UDLA\Integracion\wso2am-4.5.0\bin
```

Ejecutar el API Manager de WSO2
```bash
.\api-manager.bat --start
```

Entrar a la siguiente pagina para acceder al api manager desde el navegador: [https://localhost:9443/publisher/apis](https://localhost:9443/publisher/apis)

si es que esta sin iniciar Secion, ingresar con las credenciales de `username: admin` y `password: admin`