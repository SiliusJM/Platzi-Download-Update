<div align="center">
  <img src ="https://github.com/OscarDogar/Platzi-Download/assets/60854050/5a57dd93-1138-40d1-9231-c3c029c98bb5"/>
  <h1>Platzi-Download</h1>
</div>

> **Proyecto original por [@OscarDogar](https://github.com/OscarDogar/Platzi-Download)** — Esta es una versión actualizada mantenida por [@SiliusJM](https://github.com/SiliusJM/Platzi-Download-Update) con correcciones de compatibilidad para el estado actual de Platzi (2024–2025).
>
> ⚠️ El autor original tiene planeada una **Nueva Versión** ([#109](https://github.com/OscarDogar/Platzi-Download/issues/109)) que eliminará Selenium/ChromeDriver y migrará a Docker. Esta actualización es un parche de compatibilidad mientras tanto.

Permite descargar videos de Platzi muchos más rápido. Permite descargar tanto los videos, las lecturas, los subtítulos (si están disponibles) y los recursos de cada una de las clases.

---

## 📄 Requirements

- Es **NECESARIO** tener una cuenta de suscripción a Platzi.
- Tener **Google Chrome** instalado.
- Tener instalado **FFmpeg** (ver instrucciones de instalación más abajo).
- ~~Descargar chromedriver.exe manualmente~~ → **Ya no es necesario** (ver sección de actualizaciones).
- Tener **Python 3.10+** instalado (incluido Python 3.13).
- Instalar las dependencias con `pip install -r requirements.txt`.
- Configurar el archivo `.env` que se genera al ejecutar el programa por primera vez:
  1. `EMAIL` = `"tuemail@email.com"`
  2. `PWD` = `"tucontraseña"`
  3. `WORDS_TO_REMOVE` *(opcional)* = `word1, word2, word3`

---

## 🔧 Instalación de FFmpeg (paso a paso)

FFmpeg es necesario para unir los segmentos de video descargados. **No es un `.exe` suelto**, es un conjunto de herramientas que se instala en el sistema.

### Opción A — Instalación manual (recomendada)

1. Ve a [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html) y haz clic en el logo de Windows.
2. Descarga la build desde **gyan.dev** → `ffmpeg-release-essentials.zip` (o desde [https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/)).
3. Extrae el `.zip`. Obtendrás una carpeta como `ffmpeg-7.x.x-essentials_build`.
4. Renombra esa carpeta a `ffmpeg` y muévela a `C:\` → resultado: `C:\ffmpeg\`.
5. Dentro deberías tener la ruta `C:\ffmpeg\bin\ffmpeg.exe`.
6. Agrega `C:\ffmpeg\bin` al **PATH** del sistema:
   - Abre el menú inicio → busca **"Variables de entorno"** → **"Editar las variables de entorno del sistema"**.
   - Haz clic en **Variables de entorno...** → en la sección *Variables del sistema* selecciona `Path` → **Editar**.
   - Haz clic en **Nuevo** → escribe `C:\ffmpeg\bin` → **Aceptar** en todas las ventanas.
7. Abre una nueva terminal (cmd o PowerShell) y verifica con:
   ```
   ffmpeg -version
   ```
   Si muestra la versión, está correctamente instalado.

### Opción B — Via Winget (Windows 10/11)

```powershell
winget install Gyan.FFmpeg
```

Winget lo instala y agrega al PATH automáticamente.

### Opción C — Via Chocolatey

```powershell
choco install ffmpeg
```

> [!IMPORTANT]
> El programa verifica al iniciar si FFmpeg está instalado. Si no lo detecta, mostrará el mensaje `Please install ffmpeg` y se cerrará. Asegúrate de que `ffmpeg` esté en el PATH antes de ejecutar.

---

## 📥 Instalación del proyecto

```bash
# 1. Clonar el repositorio
git clone https://github.com/SiliusJM/Platzi-Download-Update.git
cd Platzi-Download-Update

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar el programa (genera el .env automáticamente)
python main.py
```

Al ejecutar por primera vez se crea el archivo `.env`. **Cierra el programa, edita el `.env`** con tu email y contraseña de Platzi, y vuelve a ejecutar.

---

## 📋 Cómo ejecutar el proyecto (paso a paso)

### Antes de la primera ejecución

1. Asegúrate de tener **FFmpeg** instalado y en el PATH (ver sección anterior).
2. Asegúrate de tener **Google Chrome** instalado.
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Ejecuta `python main.py` una vez para que genere el archivo `.env`.
5. Abre el `.env` (está en la misma carpeta del proyecto) y configura:
   ```env
   EMAIL="tuemail@platzi.com"
   PWD="tucontraseña"
   WORDS_TO_REMOVE=
   ```

### Ejecución normal

1. Ejecuta:
   ```bash
   python main.py
   ```
2. Se abrirá Chrome automáticamente. **No lo cierres**.
3. Ingresa la URL de la clase desde donde quieres empezar. Debe ser la URL de una clase específica, por ejemplo:
   ```
   https://platzi.com/cursos/nombre-curso/clase-nombre/
   ```
   No funciona con la URL del curso general (sin clase específica).
4. Elige la opción:
   - `1` → Descargar solo esa clase.
   - `2` → Descargar esa clase y todas las siguientes.
5. Espera el mensaje `Finding videos...`.
6. Si aparece un **captcha**, resuélvelo manualmente en la ventana de Chrome. El programa espera hasta 2 minutos.
7. Los archivos se guardan en `./videos/<nombre-del-curso>/`.

---

## ⚠️ Possible failures

* Si hay caídas o desconexiones de internet es posible que se pierda la conexión y no siga descargando o pasando los videos.
* Si se queda quieto y no avanza de una clase.
* Si después de un tiempo no se completa el captcha falla.
* `not found` en los subtítulos: no cumplió con algunas validaciones para poder descargarlo.
* `All retries failed.`: al descargar un video no se pudo obtener alguna de las partes, se salta y sigue al siguiente.
* Si al momento de estar buscando los videos se da click en otra parte que redireccione a una página distinta, genera un problema.
* En algunos casos, debido a que el servidor puede presentar problemas no se podrá descargar el video por lo que se salta y se pasa al siguiente video.

---

## 🔄 Actualizaciones (SiliusJM)

Esta fork aplica correcciones de compatibilidad sobre la versión original de OscarDogar (última release: junio 2024).

### ❌ Problema 1 — ChromeDriver manual ya no funciona

**Descripción:** El proyecto original requería descargar manualmente `chromedriver.exe`, colocarlo en `C:/chromedriver.exe` y mantenerlo sincronizado con la versión instalada de Chrome. Esto causaba errores frecuentes del tipo:
```
This version of ChromeDriver only supports Chrome version XX
```
o simplemente que Chrome no arrancara si la versión no coincidía.

**Solución aplicada:** Se reemplazó el uso directo de `webdriver.Chrome(service=Service(...))` por `undetected_chromedriver` (`uc`). Esta librería:
- **Descarga y gestiona ChromeDriver automáticamente**, sin necesidad de colocarlo en ninguna ruta manual.
- Detecta la versión mayor de Chrome instalada leyendo el registro de Windows (`HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon`) y descarga el driver compatible.
- Evita la detección de bots por parte de Platzi (de ahí el nombre *undetected*).

**Qué ya NO debes hacer:**
- ~~Descargar `chromedriver.exe` desde chromedriver.chromium.org~~
- ~~Colocarlo en `C:/chromedriver.exe`~~
- ~~Actualizarlo cada vez que Chrome se actualiza~~

**Qué sí necesitas:**
- Tener Google Chrome instalado normalmente.
- La librería `undetected-chromedriver==3.5.4` (ya está en `requirements.txt`).

---

### ❌ Problema 2 — Nuevo formato de URL de Platzi no era reconocido

**Descripción:** Platzi migró sus URLs de `/clases/` al formato `/cursos/<curso>/<clase>/`. El programa aceptaba cualquier URL y luego fallaba al no encontrar el contenido esperado.

**Solución aplicada:** Se agregó validación en la entrada de URL: ahora se verifica que la URL sea de una clase específica (contiene `/clases/` o `/cursos/` con al menos 6 barras). Si se ingresa la URL del curso general, el programa muestra un mensaje de error con un ejemplo del formato correcto.

---

### ❌ Problema 3 — Nuevo reproductor de video (estructura DASH/MPD, Platzi 2024+)

**Descripción:** Platzi actualizó su reproductor. El video ya no siempre estaba en `serverC.hls` dentro del script de la página; en las clases nuevas aparece como una URL `.mpd` (DASH) bajo la clave `"dash"`.

**Solución aplicada:** `getVideoAndSubInfo` ahora detecta ambas estructuras:
1. Estructura antigua: `serverC → hls` (URL `.m3u8` directa).
2. Estructura nueva: busca `"dash":"https://mdstrm.com/video/....mpd"` y construye la URL `.m3u8` equivalente a partir del ID del video.

---

### ❌ Problema 4 — Popup de "completar perfil" bloqueaba la navegación

**Descripción:** Platzi muestra un modal de "Completa tu perfil" que interceptaba los clics en el botón de siguiente clase, lanzando errores de elemento interceptado.

**Solución aplicada:** Se agregó detección y cierre automático del popup buscando el texto `"Omitir por ahora"` antes de intentar navegar a la siguiente clase.

---

### ❌ Problema 5 — Número de clase incorrecto / nombre repetido

**Descripción:** El contador de clases tomaba como base el número extraído del HTML (`MaterialHeading-tag`), que a veces no aparecía o tenía formato distinto. Esto causaba que varias clases se guardaran con el mismo número o con `1.` como prefijo.

**Solución aplicada:** Se implementó `getClassPositionFromSidebar`: al iniciar, el programa abre el modal *"Ver clases"* de Platzi, lee todos los enlaces de clase del curso en orden DOM, y determina la posición real de la clase de inicio. A partir de ahí lleva un contador propio (`classCounter`) independiente del HTML. Se mantienen también dos patrones de fallback en `getClassNumber` para los casos donde el sidebar no esté disponible.

> [!NOTE]
> En algunos cursos el nombre de la clase puede quedar repetido o con ligeras variaciones dependiendo de cómo Platzi renderice el DOM en ese momento. Este comportamiento aún puede ocurrir en cursos con estructura atípica.

---

### ❌ Problema 6 — Nombre del curso extraído incorrectamente

**Descripción:** El selector CSS `BadgeWithText_BadgeWithText` para obtener el nombre del curso dejó de funcionar de forma confiable tras cambios en el frontend de Platzi.

**Solución aplicada:** El nombre del curso ahora se extrae principalmente del **título de la página** (`driver.title`), que sigue el formato estable `"Nombre Clase | Nombre Curso | Platzi"`. Los selectores CSS y el slug de URL quedan como fallback en ese orden.

---

### ❌ Problema 7 — `requirements.txt` incompatible con Python 3.13

**Descripción:** El `requirements.txt` original era una exportación de `pip freeze` que incluía todas las dependencias transitivas y herramientas de build con versiones exactas (`==`) antiguas. Al instalar en Python 3.13 fallaba inmediatamente con:
```
ERROR: Failed to build 'pillow' when getting requirements to build wheel
KeyError: '__version__'
```
Los paquetes problemáticos eran `pillow==10.2.0` (no compila en Python 3.13) y `cffi==1.15.1`. Además el archivo incluía paquetes que nunca se usan en el proyecto: `Django`, `pyinstaller`, `pefile`, `pywin32-ctypes`, `sqlparse`, `altgraph`, etc.

**Solución aplicada:** Se reescribió el `requirements.txt` con **únicamente las 6 dependencias reales** del proyecto usando versiones mínimas (`>=`) en lugar de pins exactos, lo que permite que pip resuelva versiones compatibles con cualquier Python 3.10+:

```
pillow>=10.4.0
pyfiglet>=1.0.2
python-dotenv>=1.0.0
requests>=2.30.0
selenium>=4.18.0
undetected-chromedriver>=3.5.4
```

---

### ❌ Problema 8 — `ModuleNotFoundError: No module named 'distutils'` en Python 3.13

**Descripción:** Al ejecutar `python main.py` después de instalar las dependencias con Python 3.13, el programa falla inmediatamente al importar `undetected_chromedriver`:
```
File "...\undetected_chromedriver\patcher.py", line 4, in <module>
    from distutils.version import LooseVersion
ModuleNotFoundError: No module named 'distutils'
```
El módulo `distutils` fue eliminado definitivamente de la librería estándar en Python 3.13 (se deprecó en 3.10 y se removió en 3.12/3.13). `undetected-chromedriver 3.5.5` aún lo usa internamente en su archivo `patcher.py`.

**Solución aplicada:** Se agregó `setuptools>=70.0.0` al `requirements.txt`. `setuptools` incluye una capa de compatibilidad (`distutils-precedence.pth`) que restaura `distutils` como módulo importable en Python 3.13, lo que permite que `undetected-chromedriver` funcione sin modificar su código fuente.

---

## 💕 Sponsor

- Si el proyecto original te ha sido útil, apoya a su creador original:

[Sponsor OscarDogar <img src="https://github-production-user-asset-6210df.s3.amazonaws.com/60854050/263421335-c7468ed6-7853-42c6-9de9-05be51da1ca2.png" width="20"/>](https://github.com/sponsors/OscarDogar)

## ⭐ Star this project

- Repositorio original: [OscarDogar/Platzi-Download](https://github.com/OscarDogar/Platzi-Download)
- Esta fork: [SiliusJM/Platzi-Download-Update](https://github.com/SiliusJM/Platzi-Download-Update)

---

## ✅ Result

Una vez completado todo el proceso quedarán los cursos dentro de la carpeta llamada `videos` y dentro estarán otras carpetas con el nombre de cada uno de los cursos. Dentro de esas carpetas estarán los videos, una carpeta de `lectures`, una carpeta con los subtítulos y otra con los recursos.

Este sería el resultado dentro de la carpeta *Taller de Inglés Básico sobre Elementos de Trabajo*:

![image](https://github.com/OscarDogar/Platzi-Download/assets/60854050/d2aa50e8-a7c3-4bb6-8833-7b258e96181c)


## ➕ Additional

> [!TIP]
> Si deseas ver los comentarios de las clases deberás iniciar sesión, pero puede ser con una cuenta sin suscripción. Puedes utilizar la extensión [Tampermonkey](https://chromewebstore.google.com/detail/tampermonkey/dhdgffkkebhmkfjojejmpbldmpobfkfo) con el siguiente script:

### [View Platzi Comments](https://gist.githubusercontent.com/OscarDogar/717448f4db972aa01b4cf8b88baab4e2/raw/1641227fb3cd2e104002a9e50353648efd7ff250/ViewPlatziComments.js)

- Para agregar el script a Tampermonkey simplemente es ir a las configuraciones, luego a utilities y después agregar la url en la parte de abajo.

   ![image](https://github.com/OscarDogar/Platzi-Download/assets/60854050/9a6d2d7b-3b00-4632-b6c8-25f57dfd8a7d)

- Luego aparecerá otra ventana para instalar el script en Tampermonkey. Al final en la pestaña de installed userscripts deberá aparecer el script:

   ![image](https://github.com/OscarDogar/Platzi-Download/assets/60854050/c3496eaf-dc8f-41a7-8f15-3cb96bf1d801)


## 💡 Ejemplo

Como se puede ver en esta [clase](https://platzi.com/new-home/clases/2069-negocios-data-science/33434-como-crear-empresas-y-culturas-data-driven/), se alcanzan a leer los primeros comentarios de la parte de arriba, pero mientras más se va bajando menos se podrán ver los comentarios [Imagen izquierda]. Ya una vez con el script se podrán ver todos los comentarios sin necesidad de tener una cuenta de pago [Imagen derecha].

<img width="400" src ="https://github.com/OscarDogar/Platzi-Download/assets/60854050/c42d199e-9230-4334-aaf1-10a0d809ef7c"/>
<img width="400" src ="https://github.com/OscarDogar/Platzi-Download/assets/60854050/78322f45-5f97-4f7b-b4c7-96d2155aaefc"/>












