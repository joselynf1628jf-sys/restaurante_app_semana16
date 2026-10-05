# Restaurante App — Semana 16

| Campo | Detalle |
|---|---|
| **Estudiante** | Joselyn Yomaira Fuentes Rosero |
| **Asignatura** | Programación Orientada a Objetos |
| **Universidad** | Universidad Estatal Amazónica |
| **Tema** | Interacción con eventos en Tkinter |

---

## Sobre esta entrega

Esta versión evoluciona `restaurante_app` (Restaurante Casero) a partir de la Semana 15, sin reconstruirla. Se conservan íntegramente el inicio de sesión, la navegación, la gestión completa del menú y la sección Ventas construida con `command=`.

El objetivo central de esta semana es avanzar hacia el **manejo real de eventos de Tkinter mediante `bind()`**: responder a la selección en una tabla, a teclas del teclado y al cambio de valor en un `Combobox`, sin concentrar lógica de negocio en la interfaz.

Como caso práctico, la sección **Usuarios** —que hasta la Semana 15 solo permitía consultar en modo lectura— se convierte en una gestión completa (CRUD) con **roles** (`Administrador`, `Empleado`, `Cliente`) y control de acceso básico: solo el rol `Administrador` puede ver y usar esta sección.

---

## Organización de archivos

```
restaurante_app/
├── assets/
│   ├── icons/
│   └── logo/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
├── main.py
└── README.md
```

La organización no cambió respecto a la Semana 15. La evolución ocurre en `modelos/usuario.py` (atributo `rol`), `restaurante_servicio.py` (CRUD de usuarios) y `ui/main_view.py` (sección Usuarios con formulario, tabla y eventos).

---

## Responsabilidad de cada capa

| Capa | Responsabilidad |
|---|---|
| `modelos/` | `Producto` (con descripción), `Venta` (relaciona `usuario_identificacion`, `producto_codigo` y `fecha`) y `Usuario`, ahora con el atributo `rol`, validado mediante `property` contra `ROLES_PERMITIDOS = (Administrador, Empleado, Cliente)`. |
| `servicios/archivo_servicio.py` | Lee y escribe los archivos JSON de `datos/`. |
| `servicios/restaurante_servicio.py` | Convierte los datos en objetos, valida el acceso y expone el CRUD completo de productos y ventas, además del **CRUD completo de usuarios** (nuevo): `registrar_usuario`, `actualizar_usuario`, `eliminar_usuario`, `buscar_usuario_por_login`. Toda la validación y persistencia vive aquí, nunca en la interfaz. |
| `ui/` | `LoginView` y `MainView`, construidas con Tkinter. Los callbacks solo recolectan datos del formulario o del evento recibido y delegan la operación a `RestauranteServicio`. |
| `main.py` | Crea la única ventana principal, configura el ícono del sistema desde `assets/` y controla el cambio entre vistas. No se modificó esta semana. |

---

## Manejo de eventos con `bind()` (nuevo — Semana 16)

La sección **Usuarios** es el ejemplo principal de esta entrega para el manejo de eventos reales de Tkinter, más allá de `command=`:

```
Interaccion del usuario -> evento -> bind() -> callback(event) -> RestauranteServicio -> usuarios.json -> tabla actualizada
```

| Evento | Widget | Callback | Efecto |
|---|---|---|---|
| `<<TreeviewSelect>>` | Tabla de usuarios | `al_seleccionar_usuario` | Carga el usuario seleccionado en el formulario |
| `<Return>` | Contraseña / Rol | `al_presionar_enter_usuario` | Registra el usuario desde el formulario |
| `<Escape>` | Todos los campos y la tabla | `al_presionar_escape_usuario` | Limpia el formulario y cancela la selección |
| `<<ComboboxSelected>>` | Combobox de rol | `al_seleccionar_rol` | Actualiza la etiqueta "Rol seleccionado" |

Ningún callback contiene lógica de negocio: todos obtienen datos de la interfaz o del `event` recibido y delegan la validación y la persistencia a `RestauranteServicio`, reutilizando el mismo patrón que ya usaba la sección Ventas con `command=`.

---

## Sección Ventas: flujo de eventos aplicado (Semana 15)

```
Cliente elige un Cliente y un Producto en los Combobox
                ↓
Clic en "Registrar venta"  (command=self.registrar_venta)
                ↓
Callback registrar_venta() en MainView:
    - obtiene el texto seleccionado en cada Combobox
    - lo traduce a la identificacion / codigo real
    - llama a restaurante_servicio.registrar_venta(...)
                ↓
RestauranteServicio.registrar_venta():
    - valida que ambos campos vengan seleccionados
    - valida que el cliente exista
    - valida que el producto exista
    - crea un objeto Venta (el modelo valida sus propios datos)
    - agrega la venta en memoria y llama a guardar_ventas()
                ↓
ArchivoServicio.escribir_json() persiste en ventas.json
                ↓
MainView.refrescar_ventas() actualiza la tabla (Treeview)
y la barra de estado inferior
```

Esta sección se conserva sin cambios; convive con la sección Usuarios como ejemplo de la diferencia entre `command=` (acción explícita de un botón) y `bind()` (respuesta a un evento generado por el usuario).

### Componentes usados en Ventas

- `ttk.Combobox` (solo lectura) para elegir un cliente y un producto existentes.
- `ttk.Button` con `command=self.registrar_venta`.
- `ttk.Treeview` + `ttk.Scrollbar` para las ventas registradas.
- `tk.LabelFrame` para separar el formulario del listado, igual que en Productos y Usuarios.

---

## Gestión de usuarios y roles (nuevo — Semana 16)

La pestaña **Usuarios** del menú superior solo aparece cuando la sesión activa pertenece al rol `Administrador`; ese es el control de acceso básico que pide la actividad. Desde allí se puede:

- Registrar un nuevo usuario indicando identificación, nombre, teléfono, usuario, contraseña y rol.
- Consultar los usuarios registrados en una tabla (`Treeview`), incluyendo su rol.
- Seleccionar un usuario de la tabla (evento `<<TreeviewSelect>>`) para cargar automáticamente sus datos en el formulario.
- Actualizar los datos del usuario seleccionado.
- Eliminar el usuario seleccionado, con confirmación previa.
- Limpiar el formulario y cancelar la selección actual (botón o tecla `Escape`).

`RestauranteServicio` impide eliminar el usuario con el que se inició sesión y cambiar el rol del administrador actualmente conectado, para que la aplicación nunca quede sin una cuenta administrativa activa.

## Operaciones implementadas sobre usuarios, productos y ventas

| Operación | Acción en la interfaz | Método en `RestauranteServicio` |
|---|---|---|
| Registrar producto | Botón **Registrar** | `registrar_producto(...)` |
| Actualizar producto | Botón **Actualizar** | `actualizar_producto(...)` |
| Eliminar producto | Botón **Eliminar** | `eliminar_producto(codigo)` |
| Registrar venta | Botón **Registrar venta** | `registrar_venta(usuario_identificacion, producto_codigo)` |
| Registrar usuario | Botón **Registrar** / tecla `Enter` | `registrar_usuario(identificacion, nombre, telefono, usuario, contrasena, rol)` |
| Consultar usuario | Selección en la tabla (`<<TreeviewSelect>>`) | `buscar_usuario_por_identificacion(identificacion)` |
| Actualizar usuario | Botón **Actualizar** | `actualizar_usuario(identificacion, nombre, telefono, usuario, contrasena, rol, identificacion_actual)` |
| Eliminar usuario | Botón **Eliminar** | `eliminar_usuario(identificacion, identificacion_actual)` |

---

## Recursos gráficos (`assets/`)

- `assets/logo/logo.png`: logotipo mostrado en la pantalla de inicio de sesión.
- `assets/logo/icono.png`: versión simplificada usada como ícono de la ventana principal y junto al título en el encabezado.
- `assets/icons/`: íconos para cada botón de navegación (Inicio, Productos, Usuarios, Reservas, Ventas, Cerrar sesión) y para las acciones de los formularios, reutilizados también en el nuevo formulario de usuarios (`add.png`, `edit.png`, `delete.png`, `clean.png`).

---

## Persistencia

Los productos se guardan en `datos/productos.json`. Las ventas se guardan en `datos/ventas.json`. Los usuarios se guardan en `datos/usuarios.json` mediante `guardar_usuarios()` (nuevo), incluyendo ahora el campo `rol`. Las tres operaciones delegan en `ArchivoServicio`. Al reabrir la aplicación, los productos, las ventas y los usuarios registrados se recuperan correctamente.

Ejemplo de usuario persistido:

```json
{
    "identificacion": "0911112222",
    "nombre": "Cocinera Principal",
    "telefono": "0987654321",
    "usuario": "cocina1",
    "contrasena": "casero2026",
    "rol": "Empleado"
}
```

---

## Control de acceso

| Rol | Acceso a la pestaña Usuarios |
|---|---|
| `Administrador` | Sí |
| `Empleado` | No |
| `Cliente` | No |

No se implementa un sistema avanzado de permisos; el objetivo es demostrar un control de acceso básico a partir del rol del usuario que inició sesión.

---

## Flujo de la aplicación

```
Inicio -> LoginView -> RestauranteServicio valida el acceso -> MainView
MainView -> Inicio (resumen) | Productos | Usuarios* (solo Administrador) | Ventas | Reservas
Usuarios -> seleccionar fila -> <<TreeviewSelect>> -> formulario cargado
Registrar / Actualizar / Eliminar -> command= -> RestauranteServicio valida y persiste
Enter registra, Escape limpia, <<ComboboxSelected>> actualiza el rol mostrado
MainView -> Cerrar sesion -> LoginView
```

---

## Credenciales de acceso (demostración)

| Usuario | Contraseña | Rol |
|---|---|---|
| `jfuentes` | `caseroapp` | Cliente |
| `admin` | `admin321` | Administrador |
| `cocina1` | `casero2026` | Empleado |

---

## Cómo ejecutar

```bash
cd restaurante_app
python main.py
```

---

## Pruebas realizadas

- Se ejecutó `main.py` y la aplicación inició sin errores, con el ícono del sistema visible en la ventana.
- El inicio de sesión con `admin` / `admin321` continúa funcionando y muestra el logotipo.
- La navegación y la gestión completa de Productos siguen funcionando igual que en la Semana 15.
- Con la sesión de `admin`, aparece la pestaña **Usuarios**; con `jfuentes` (Cliente), la pestaña no aparece en el menú superior.
- Se registró un nuevo usuario con rol `Empleado` desde el formulario; apareció de inmediato en la tabla.
- Al seleccionar una fila de la tabla (`<<TreeviewSelect>>`), los datos se cargaron correctamente en el formulario.
- Se actualizaron el nombre, la contraseña y el rol de un usuario seleccionado; el cambio se reflejó en la tabla y en `usuarios.json`.
- Se intentó cambiar el rol del administrador con el que se inició sesión: la operación fue rechazada con un mensaje claro.
- Se intentó eliminar el usuario con el que se inició sesión: la operación fue rechazada.
- Se usó la tecla `Enter` desde el campo Contraseña para registrar un usuario, y `Escape` para limpiar el formulario y cancelar la selección.
- El Combobox de rol actualizó la etiqueta "Rol seleccionado" al cambiar de valor (`<<ComboboxSelected>>`).
- La sección Ventas se probó sin cambios y continúa registrando pedidos mediante `command=`.
- Al cerrar y volver a ejecutar la aplicación, los usuarios, productos y ventas registrados se recuperan correctamente.

---

## Nota sobre la autenticación

El acceso de esta etapa es una simulación pedagógica. Las contraseñas se guardan en JSON en texto plano solo con fines didácticos; no representa una práctica segura para un sistema real. La gestión de roles tampoco implementa un sistema de permisos avanzado: su propósito es mostrar, de forma clara, el uso de eventos de Tkinter aplicados a una operación CRUD real.
