---
slug: github-pages-custom-domain-cloudflare-dns
title: "[Dominio Personalizado en GitHub Pages #1] Migración de github.io con Porkbun y Cloudflare DNS: CNAME Flattening y SSL Gratuito"
authors: [jbjihwan]
tags: [github-pages, custom-domain, porkbun, cloudflare, docusaurus, devops]
keywords: [Docusaurus GitHub Pages Custom Domain, Cloudflare DNS Porkbun CNAME setup, CNAME Flattening apex domain GitHub Pages, Cloudflare Full SSL Edge Certificate, static CNAME deployment reset bug fix]
description: "Guía de producción paso a paso para abandonar los subdominios gratuitos github.io, adquirir un dominio apex con Porkbun, delegar a Cloudflare Anycast DNS, configurar CNAME Flattening y solventar el reseteo del archivo CNAME en Docusaurus."

---

Alojarse en GitHub Pages mediante el subdominio gratuito (`username.github.io/proyecto`) es una de las soluciones más ágiles para publicar un blog de ingeniería sin incurrir en costes de servidor.

No obstante, cuando se persigue una marca profesional y se contempla la **monetización mediante Google AdSense**, surge un impedimento ineludible: **las políticas de Google AdSense prohíben estrictamente el registro de subdominios secundarios gratuitos como `*.github.io`**. Adicionalmente, para que la autoridad de dominio acumulada en los motores de búsqueda sea un activo propio, es imprescindible disponer de un **dominio apex personalizado (por ejemplo, `globaldevlog.com`)**.

En esta primera entrega de nuestra serie sobre infraestructura para blogs estáticos, explicamos la arquitectura de 3 capas con **Porkbun + Cloudflare + GitHub Pages** que utilizamos para migrar `jbjihwan.github.io/global_blog` a `https://globaldevlog.com` con cero tiempo de inactividad.

{/* truncate */}

---

![Arquitectura de Enrutamiento DNS y CDN en Producción](./images/01_dns_routing_architecture.png)

---

## 1. Filosofía de Arquitectura: Configuración Robusta en 3 Capas

El método elemental para conectar un dominio a GitHub Pages consiste en apuntar registros `A` directamente a las 4 direcciones IP fijas de GitHub (`185.199.108.153`, etc.).

Sin embargo, esta solución tradicional adolece de desventajas operativas notables:
- Ausencia de cortafuegos perimetral contra ataques DDoS o tráfico abusivo de bots.
- Lentitud en la propagación de DNS ante cualquier contingencia.
- Imposibilidad de optimizar la caché de activos estáticos (CSS, JS, imágenes).

Separamos las responsabilidades en 3 proveedores especializados:

| Capa | Proveedor | Responsabilidades Clave |
| :--- | :--- | :--- |
| **1. Registrador** | **Porkbun** | Adquisición de dominio y costes anuales de renovación más bajos del mercado, privacidad WHOIS perpetua gratuita |
| **2. Edge DNS & Seguridad** | **Cloudflare** | DNS Anycast de latencia mínima, **CNAME Flattening en el dominio apex (`@`)**, Universal SSL gratuito y protección perimetral |
| **3. Origen Estático** | **GitHub Pages** | Servidor de archivos compilados por Docusaurus, despliegue continuo mediante la rama `gh-pages`, coste de alojamiento 0 € |

---

## 2. Paso 1: Adquisición en Porkbun y Delegación de Servidores de Nombres

1. **Compra del Dominio**: Se adquiere el dominio en Porkbun con tarifas transparentes y sin recargos sorpresa de renovación.
2. **Alta en Cloudflare**: En el panel de Cloudflare, se hace clic en **Añadir sitio**, se ingresa `globaldevlog.com` y se escoge el **Plan Gratuito**.
3. **Servidores de Nombres Asignados**: Cloudflare provee dos servidores autoritativos, por ejemplo:
   ```text
   roan.ns.cloudflare.com
   sneh.ns.cloudflare.com
   ```
4. **Configuración en Porkbun**: Dentro de la consola de gestión de Porkbun (`Authoritative Nameservers`), se sustituyen las entradas por defecto por las dos proporcionadas por Cloudflare. La propagación suele completarse en 5 a 15 minutos.

---

## 3. Paso 2: CNAME Flattening y Modo Full SSL en Cloudflare

Conforme al estándar RFC 1034, el dominio apex (`@`) no admite registros CNAME convencionales debido a la convivencia con registros SOA y NS.

Cloudflare elimina este obstáculo mediante la función **CNAME Flattening**: en el momento de la consulta DNS, el edge de Cloudflare resuelve internamente el destino (`username.github.io`) y devuelve directamente las IPs, otorgando todas las ventajas de CNAME en el propio apex.

### A. Registros DNS en Cloudflare
En la sección **[DNS] > [Registros]**, se agregan dos registros con proxy activado:

| Tipo (Type) | Nombre (Name) | Destino (Target) | Estado de proxy | TTL |
| :--- | :--- | :--- | :--- | :--- |
| **CNAME** | `@` | `jbjihwan.github.io` | **Con proxy (Nube naranja activada)** | Automático |
| **CNAME** | `www` | `jbjihwan.github.io` | **Con proxy (Nube naranja activada)** | Automático |

> **Proxy Obligatorio**: Mantener la nube naranja activa asegura que todo el tráfico transite por el edge Anycast de Cloudflare, garantizando cifrado SSL gratuito, compresión Brotli y distribución ultra veloz.

### B. Modo de Cifrado SSL/TLS
En **[SSL/TLS] > [Información general]**:
- Se selecciona el modo **Full** (o **Full Strict**).
- Con ello se garantiza el cifrado seguro de extremo a extremo: entre el navegador del visitante y Cloudflare, y entre Cloudflare y el origen en GitHub Pages.

---

## 4. Paso 3: Ajuste de la Configuración en Docusaurus (`docusaurus.config.ts`)

Para trasladar las rutas relativas desde la subcarpeta (`/global_blog/`) a la raíz del nuevo dominio (`/`), se actualiza `docusaurus.config.ts`:

```typescript
const config: Config = {
  title: 'Global Dev Blog',
  tagline: 'Engineering Deep Dives in AI, Robotics, Computer Vision',

  // Dirección oficial del dominio personalizado
  url: 'https://globaldevlog.com',
  // Se define la raíz absoluta
  baseUrl: '/',

  organizationName: 'jbjihwan',
  projectName: 'global_blog',
  trailingSlash: false,
  // ...
};
```

---

## 5. Paso 4: Corrección del Fallo de Reseteo del Dominio en GitHub Pages (`static/CNAME`)

Un error habitual al enlazar un dominio propio en GitHub Pages es la **pérdida silenciosa de la configuración al desplegar**:
1. Se define `globaldevlog.com` en `Settings > Pages > Custom domain`.
2. Se ejecuta `npm run deploy` desde el equipo local.
3. El despliegue sobreescribe la rama `gh-pages` y borra la asignación, provocando errores 404 o caídas del certificado SSL.

### La Causa
El script de despliegue compila en `build/` y fuerza un push (`git push --force`) a la rama `gh-pages`. Si el archivo `CNAME` no se encuentra en la compilación, GitHub asume que el dominio ha sido retirado.

### Solución Definitiva
Se crea el archivo `static/CNAME` (sin extensión) con el dominio en texto plano:

```text
globaldevlog.com
```

Dado que Docusaurus traslada automáticamente todo el contenido de `static/` a la raíz de la compilación, el archivo `CNAME` se incorpora de forma perpetua en cada nuevo despliegue.

---

## 6. Verificación en Producción

Se compila y despliega el sitio:
```bash
npm run deploy
```

Se comprueba la cabecera HTTP y la validez del certificado:

```bash
curl -I https://globaldevlog.com
# HTTP/2 200
# server: cloudflare
# strict-transport-security: max-age=31536000

curl -I https://www.globaldevlog.com
# HTTP/2 200 (o redirección 301 al apex)
```

---

## 🔜 Próximas Entregas

Con el dominio apex plenamente operativo, los siguientes hitos son la monetización y la indexación en buscadores:
- **Parte 2**: *[Monetización de Sitios Estáticos #2] Aprobación de Google AdSense en Docusaurus: Resolución del error 404 en ads.txt e Inyección Asíncrona de Scripts*
- **Parte 3**: *[SEO Multimotor #3] Registro en Google, Naver y Bing: Trucos para la Eliminación de Sitemaps y Errores de Nivel Host*

---

### 📌 Resumen Ejecutivo de 3 a 5 Líneas
1. **Arquitectura Empresarial con Costo Cero de Servidor**: La combinación de Porkbun (registro al costo), Cloudflare (Anycast CDN y DNS global) y GitHub Pages (alojamiento estático gratuito) ofrece infraestructura de alto rendimiento sin costes operativos.
2. **Superación del Límite RFC 1034 con CNAME Flattening**: Resuelve la restricción técnica de asignar CNAMEs en el dominio raíz (`@`) mediante la técnica de aplanamiento de Cloudflare, conectando el apex directamente a GitHub Pages.
3. **Cifrado Extremo a Extremo en Modo Full (Strict)**: Establece túneles HTTPS seguros tanto entre el visitante y Cloudflare como entre Cloudflare y los servidores de origen de GitHub Pages.
4. **Persistencia Garantizada con static/CNAME**: Alojar el archivo `CNAME` en el directorio `static/` de Docusaurus evita que los despliegues automatizados eliminen la configuración del dominio personalizado.