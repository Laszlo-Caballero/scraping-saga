from dataclasses import dataclass, asdict, field

value_error = tuple[str | None, str | None]

@dataclass
class Product:

    name: str = ""
    price: list[float] = field(default_factory=list)
    buy_by: str = ""
    brand: str = ""
    url: str = ""
    images: list[str] = field(default_factory=list)
    caracteristics: list[str] = field(default_factory=list)
    spects: list[str] = field(default_factory=list)
    category: str = ""
    sub_category: str = ""
    
    error: str = ""
    especific_error: dict[str, str] = field(default_factory=dict)
    
    def to_dict(self):
        return asdict(self)
    
    def set_error(self, error: str):
        self.error = error
    
    def append_especific_error(self, key: str, value: str):
        self.especific_error[key] = value
    
    def set_name(self, name: value_error):
        error, value = name
        if error:
            self.append_especific_error("name", error)
        else:
            self.name = value or ""
    
    def set_brand(self, brand: value_error):
        error, value = brand
        if error:
            self.append_especific_error("brand", error)
        else:
            self.brand = value or ""
    
    def set_url(self, url: value_error):
        error, value = url
        if error:
            self.append_especific_error("url", error)
        else:
            self.url = value or ""
    
    def set_price(self, price: list[value_error]):
        for error, value in price:
            if error:
                self.append_especific_error("price", error)
            else:
                try:
                    price_value = float(value.replace("S/", "").replace(",", "").strip())
                    self.price.append(price_value)
                except Exception as e:
                    self.append_especific_error("price", f"Error al convertir precio: {e}")
    
    