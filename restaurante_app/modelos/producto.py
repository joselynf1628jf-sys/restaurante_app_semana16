class Producto:
    CATEGORIAS_VALIDAS: tuple[str, ...] = (
        "DESAYUNO",
        "ALMUERZO",
        "CENA",
        "BEBIDA",
        "ADICIONAL",
    )

    def __init__(
        self,
        codigo: str,
        nombre: str,
        precio: float,
        categoria: str,
        descripcion: str = "",
        stock: int = 0,
    ) -> None:
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
        self.descripcion = descripcion
        self.stock = stock

    @staticmethod
    def formatear_codigo(valor: str) -> str:
        return valor.strip().upper()

    @property
    def codigo(self) -> str:
        return self._codigo

    @codigo.setter
    def codigo(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El codigo no puede estar vacio.")
        self._codigo = Producto.formatear_codigo(valor)

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El nombre del producto no puede estar vacio.")
        self._nombre = valor.strip()

    @property
    def precio(self) -> float:
        return self._precio

    @precio.setter
    def precio(self, valor: float) -> None:
        try:
            precio = float(valor)
        except (TypeError, ValueError):
            raise ValueError("El precio debe ser un numero valido.")
        if precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        self._precio = round(precio, 2)

    @property
    def categoria(self) -> str:
        return self._categoria

    @categoria.setter
    def categoria(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("La categoria no puede estar vacia.")
        cat = valor.strip().upper()
        if cat not in self.CATEGORIAS_VALIDAS:
            raise ValueError(f"Categoria invalida. Use: {', '.join(self.CATEGORIAS_VALIDAS)}")
        self._categoria = cat

    @property
    def descripcion(self) -> str:
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor: str) -> None:
        self._descripcion = valor.strip() if valor else ""

    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, valor: int) -> None:
        try:
            stock = int(valor)
        except (TypeError, ValueError):
            raise ValueError("El stock debe ser un numero entero.")
        if stock < 0:
            raise ValueError("El stock no puede ser negativo.")
        self._stock = stock

    def vender(self, cantidad: int) -> bool:
        if cantidad <= 0 or self._stock < cantidad:
            return False
        self._stock -= cantidad
        return True

    def hay_disponibilidad(self) -> bool:
        return self._stock > 0

    def convertir_a_diccionario(self) -> dict:
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "precio": self.precio,
            "categoria": self.categoria,
            "descripcion": self.descripcion,
            "stock": self.stock,
        }

    def __str__(self) -> str:
        return (
            f"Codigo: {self.codigo} | Nombre: {self.nombre} | "
            f"Precio: ${self.precio:.2f} | Categoria: {self.categoria} | "
            f"Descripcion: {self.descripcion or 'Sin descripcion'} | Stock: {self.stock}"
        )
