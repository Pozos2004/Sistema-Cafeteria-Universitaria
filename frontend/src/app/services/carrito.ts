import { Injectable, signal } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class CarritoService {
  items = signal<any[]>([]);

  agregarProducto(producto: any, variante: any = null, personalizaciones: any[] = []) {
    const itemsActuales = this.items();
    
    let precioFinal = parseFloat(producto.precio_base);
    if (variante) precioFinal += parseFloat(variante.precio_extra);
    personalizaciones.forEach(p => precioFinal += parseFloat(p.precio_extra));

    const index = itemsActuales.findIndex(item => 
      item.producto.id === producto.id && 
      item.variante?.id === variante?.id &&
      JSON.stringify(item.personalizaciones.map((p:any) => p.id).sort()) === JSON.stringify(personalizaciones.map(p => p.id).sort())
    );

    if (index !== -1) {
      const nuevosItems = [...itemsActuales];
      nuevosItems[index].cantidad += 1;
      this.items.set(nuevosItems);
    } else {
      this.items.set([...itemsActuales, {
        producto,
        variante,
        personalizaciones,
        cantidad: 1,
        precioUnitario: precioFinal
      }]);
    }
  }

  eliminarProducto(index: number) {
    const nuevosItems = [...this.items()];
    nuevosItems.splice(index, 1);
    this.items.set(nuevosItems);
  }

  total = () => {
    return this.items().reduce((acc, item) => acc + (item.precioUnitario * item.cantidad), 0);
  }

  vaciarCarrito() {
    this.items.set([]);
  }
}