class Venta:
    def __init__(
        self,
        identificador: str,
        usuario_identificacion: str,
        producto_codigo: str,
        fecha: str,
    ) -> None:
        self.identificador = identificador
        self.usuario_identificacion = usuario_identificacion
        self.producto_codigo = producto_codigo
        self.fecha = fecha

    @property
    def identificador(self) -> str:
        return self._identificador

    @identificador.setter
    def identificador(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El identificador de la venta no puede estar vacio.")
        self._identificador = valor.strip()

    @property
    def usuario_identificacion(self) -> str:
        return self._usuario_identificacion

    @usuario_identificacion.setter
    def usuario_identificacion(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("La venta debe indicar el usuario que la realiza.")
        self._usuario_identificacion = valor.strip()

    @property
    def producto_codigo(self) -> str:
        return self._producto_codigo

    @producto_codigo.setter
    def producto_codigo(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("La venta debe indicar el producto del menu.")
        self._producto_codigo = valor.strip()

    @property
    def fecha(self) -> str:
        return self._fecha

    @fecha.setter
    def fecha(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("La fecha de la venta no puede estar vacia.")
        self._fecha = valor.strip()

    def convertir_a_diccionario(self) -> dict:
        return {
            "identificador": self.identificador,
            "usuario_identificacion": self.usuario_identificacion,
            "producto_codigo": self.producto_codigo,
            "fecha": self.fecha,
        }

    def __str__(self) -> str:
        return (
            f"Venta: {self.identificador} | Usuario: {self.usuario_identificacion} | "
            f"Producto: {self.producto_codigo} | Fecha: {self.fecha}"
        )
