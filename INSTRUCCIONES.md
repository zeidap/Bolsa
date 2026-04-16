# 📈 Cartera 1738 – Instrucciones de publicación en GitHub

Seguí estos pasos **una sola vez**. Después todo funciona automáticamente.

---

## PASO 1 — Crear cuenta en GitHub (5 min)

1. Entrá a **https://github.com**
2. Hacé clic en **"Sign up"** (arriba a la derecha)
3. Ingresá tu email, una contraseña y elegí un nombre de usuario (ej: `patriciozeida`)
4. Verificá tu cuenta con el email que te manden
5. Elegí el plan **Free** (no necesitás pagar nada)

---

## PASO 2 — Crear el repositorio (2 min)

1. Una vez logueado, hacé clic en **"New"** (botón verde, arriba a la izquierda)
2. Completá el formulario:
   - **Repository name:** `cartera-1738`
   - **Description:** `Dashboard de cartera de acciones` *(opcional)*
   - Dejá seleccionado **Public** *(necesario para GitHub Pages gratis)*
   - **NO** marques ninguna de las opciones de inicialización (README, .gitignore)
3. Hacé clic en **"Create repository"**

---

## PASO 3 — Subir los archivos (5 min)

Una vez creado el repositorio, vas a ver una pantalla vacía con instrucciones.
La forma más fácil para empezar es **subir los archivos directo desde el navegador**:

1. En la pantalla del repo, buscá el link que dice **"uploading an existing file"** y hacelo clic
2. Arrastrá **toda la carpeta `cartera-app`** a la zona de carga
   - O hacé clic en "choose your files" y seleccioná todos los archivos
3. Asegurate de que estén subidos estos archivos y carpetas:
   ```
   index.html
   data/prices.json
   scripts/fetch_prices.py
   .github/workflows/update-prices.yml
   ```
4. En la sección "Commit changes" abajo, dejá el mensaje por defecto y hacé clic en **"Commit changes"**

> ⚠️ **Importante:** la carpeta `.github` empieza con un punto. Algunos sistemas operativos la ocultan.
> Si no podés verla, en Mac abrí Finder y presioná **Cmd + Shift + .** para mostrar archivos ocultos.

---

## PASO 4 — Activar GitHub Pages (2 min)

1. En tu repositorio, hacé clic en **Settings** (engranaje, arriba)
2. En el menú izquierdo, hacé clic en **Pages**
3. En la sección "Build and deployment":
   - **Source:** seleccioná `Deploy from a branch`
   - **Branch:** seleccioná `main` y la carpeta `/ (root)`
4. Hacé clic en **Save**
5. Esperá 1-2 minutos y actualizá la página

Vas a ver un cartel verde que dice: **"Your site is live at https://TU_USUARIO.github.io/cartera-1738/"**

🎉 **¡Ya podés abrir esa URL desde cualquier dispositivo!**

---

## PASO 5 — Habilitar los precios automáticos (1 min)

Para que GitHub actualice los precios solo, necesitás darle permiso:

1. En tu repositorio, hacé clic en **Settings**
2. En el menú izquierdo, andá a **Actions → General**
3. Bajá hasta "Workflow permissions"
4. Seleccioná **"Read and write permissions"**
5. Hacé clic en **Save**

Ahora podés probar que funciona:
1. Hacé clic en la pestaña **Actions** (en el menú de tu repo)
2. En la lista izquierda, buscá **"📈 Actualizar Precios"**
3. Hacé clic en **"Run workflow"** → **"Run workflow"** (botón verde)
4. Esperá ~30 segundos y actualizá la página
5. Deberías ver un tick verde ✅ indicando que funcionó

Después de esto, **los precios se van a actualizar automáticamente cada día hábil a las 18hs Argentina** sin que hagas nada.

---

## ¿Cómo actualizar la cartera cuando cambian las posiciones?

Cuando tu broker te mande un nuevo archivo HTM:

1. Subí el archivo HTM a la carpeta **Bolsa** en tu computadora
2. Abrí esta app (Claude / Cowork) y decime: **"Actualizá la cartera 1738 con el nuevo HTM"**
3. Yo voy a leer el archivo, actualizar `data/prices.json` y `index.html`, y te voy a dar los archivos para reemplazar en GitHub

Para reemplazar archivos en GitHub:
1. Entrá a tu repo en github.com
2. Hacé clic en el archivo que querés actualizar
3. Hacé clic en el ícono del lápiz ✏️ (arriba a la derecha)
4. Reemplazá el contenido y hacé clic en **"Commit changes"**

---

## Estructura del proyecto

```
cartera-1738/
│
├── index.html                          ← La app web (abrís esta URL)
│
├── data/
│   └── prices.json                     ← Precios actualizados automáticamente
│
├── scripts/
│   └── fetch_prices.py                 ← Script que descarga los precios
│
└── .github/
    └── workflows/
        └── update-prices.yml           ← Cron job: corre el script diariamente
```

---

## URL de tu app

Una vez publicada, la URL va a ser:
```
https://TU_USUARIO_DE_GITHUB.github.io/cartera-1738/
```

Guardá esa URL como favorito en tu teléfono 📱 — podés abrirla desde cualquier lugar.

---

*Generado por Claude · Cowork · Cartera 1738 – Accrogliano Gabriela*
