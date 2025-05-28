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

### Realizar algun cambio para hacer un rollout:
```bash
kubectl rollout restart deployment auth-deployment
kubectl rollout restart deployment order-deployment
kubectl rollout restart deployment payment-deployment
```

### Verificamos los pods y servicios esten corriendo
```bash
kubectl get pods
kubectl get svc
```

### Ver contenedor con Kiali
```bash
istioctl dashboard kiali 
```

### Realizar el port forwarding para comunicar los servicios
```bash
kubectl port-forward svc/auth-service 5000:80
kubectl port-forward svc/order-service 5001:80
kubectl port-forward svc/payment-service 5002:80
```

## API GATEWAY con WSO2:

### Documentación
[Documentacion de WSO2](https://apim.docs.wso2.com/en/latest/install-and-setup/install/installing-the-product/running-the-api-m/)

### Abrir el WS02 e ingresar
Ubicacion de WSO2:
```bash
cd C:\Users\user\GitRepositories\UDLA\Integracion\wso2am-4.5.0\bin
```

### Ejecutar el API Manager de WSO2
```bash
.\api-manager.bat --start
```

Entrar a la siguiente pagina para acceder al api manager desde el navegador: [https://localhost:9443/publisher/apis](https://localhost:9443/publisher/apis)

si es que esta sin iniciar Secion, ingresar con las credenciales de `username: admin` y `password: admin`

### Entrar a la pagina de publixher de API Manager 
[https://localhost:9443/publisher](https://localhost:9443/publisher)

Luego apareceran opciones para crear un api, donde nosotros escogemos el `Start From Scratch`
Donde pondremos
* Nombre de nuestra aplicacion
* Contexto "Ejemplo: /api/weather"
* version
* Endpoint a apuntar de la aplicación (Si se creo con el Service Mesh, poner el puerto que estas haciendo forwarding)

Y en la parte de resources nosotros vamos a poner los endpoints que nosotros queremos que se transcurran
Por ejemplo en la parte de verify ponemos:
* HTTP Veb: POST
* Enter URI pattern: /verify

O

* HTTP Verb: GET
* Enter URI Pattern: /users/{userId}

Y le damos al + para que se agregue, como estamos controlando un swagger, ponemos que en eh header nos manden la authorization

Expandimos la parte del post para que nos aparezcan los `parametros` y con ello ponemos en body con el contenttype de `application/json` y que es requerido y enviamos

y le damos guardar

### Crear aplicacion
Para la aplicacion y manejo de solicitudes, se le da el siguiente contexto de dev portal, primero entramos a la aplicacion en esta url:

[https://localhost:9443/devportal/](https://localhost:9443/devportal/)

y en la parte superior izquierda le damos click en aplicaciones

Luego le damos click en `Agregar Nueva Aplicacion` donde ponemos
* Nombre de la aplicacion
* solicitudes por minuto
* Descipcion de aplicacion opcional

Le damos a guardar, en la parte izquierda aparecera lo que dice `fichas oauth2` y en esa le damos click

Bajamos toda la pagina y le damos click en `Generate keys`

### Suscripcion a aplicacion del API
Volvemos a la pantalla de APIs y seleccionamos la aplicacion que deseamos suscribir

y en la parte derecha aparecera un boton que dice `Suscripciones` damos click ahi y seleccionamos la aplicacion que nosotros escogimos y le ponemos suscribirse

