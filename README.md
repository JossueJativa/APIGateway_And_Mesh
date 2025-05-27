# Informacion para la prueba de Integracion Api Manager con Service Mesh

## API GATEWAY con WSO2:

### Documentación
[Documentacion de WSO2](https://apim.docs.wso2.com/en/latest/install-and-setup/install/installing-the-product/running-the-api-m/)

### Abrir el WS02 e ingresar
Ubicacion de WSO2:
```bash
> cd C:\Users\user\GitRepositories\UDLA\Integracion\wso2am-4.5.0\bin
```

Ejecutar el API Manager de WSO2
```bash
> .\api-manager.bat --start
```

Entrar a la siguiente pagina para acceder al api manager desde el navegador: [https://localhost:9443/publisher/apis](https://localhost:9443/publisher/apis)

si es que esta sin iniciar Secion, ingresar con las credenciales de `username: admin` y `password: admin`

## Service Mesh con Istio

### Documentación
[Documentacion de Istio](https://istio.io/latest/docs/setup/getting-started/)