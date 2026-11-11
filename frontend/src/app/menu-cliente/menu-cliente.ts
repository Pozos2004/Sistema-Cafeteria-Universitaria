import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';
import { ProductoService } from '../services/producto';
import { CarritoService } from '../services/carrito';
import { AuthService } from '../services/auth';

@Component({
  selector: 'app-menu-cliente',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './menu-cliente.html',
  styleUrl: './menu-cliente.css'
})
export class MenuClienteComponent implements OnInit {
  productos = signal<any[]>([]);
  variantesSeleccionadas: { [key: number]: any } = {};
  personalizacionesSeleccionadas: { [key: number]: any[] } = {};

  constructor(
    private productoService: ProductoService,
    public carritoService: CarritoService,
    private http: HttpClient,
    private router: Router,
    public authService: AuthService
  ) {}

  ngOnInit() {
    this.productoService.getProductos().subscribe(data => this.productos.set(data));
  }

  togglePersonalizacion(prodId: number, personalizacion: any, event: any) {
    if (!this.personalizacionesSeleccionadas[prodId]) this.personalizacionesSeleccionadas[prodId] = [];
    if (event.target.checked) this.personalizacionesSeleccionadas[prodId].push(personalizacion);
    else this.personalizacionesSeleccionadas[prodId] = this.personalizacionesSeleccionadas[prodId].filter(p => p.id !== personalizacion.id);
  }

  agregarAlCarrito(producto: any) {
    const varianteId = this.variantesSeleccionadas[producto.id];
    let variante = null;
    if (varianteId) variante = producto.variantes.find((v: any) => v.id === parseInt(varianteId));
    const pers = this.personalizacionesSeleccionadas[producto.id] || [];
    this.carritoService.agregarProducto(producto, variante, pers);
  }

  obtenerNombresPersonalizaciones(item: any): string {
    if (!item.personalizaciones || item.personalizaciones.length === 0) return '';
    return item.personalizaciones.map((p: any) => p.nombre).join(', ');
  }

  logout() {
    this.authService.logout();
  }

  confirmarPedido() {
    const token = this.authService.getToken();
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);

    const pedidoData = {
      total: this.carritoService.total(),
      detalles: this.carritoService.items().map(item => ({
        producto: item.producto.id,
        variante: item.variante ? item.variante.id : null,
        cantidad: item.cantidad,
        precio_unitario: item.precioUnitario
      }))
    };

    this.http.post('http://127.0.0.1:8000/api/pedidos/', pedidoData, { headers }).subscribe({
      next: (respuesta: any) => {
        this.carritoService.vaciarCarrito();
        this.router.navigate(['/seguimiento', respuesta.folio]);
      },
      error: (err) => {
        console.error('Error:', err);
        alert('Hubo un error al procesar tu pedido.');
      }
    });
  }
}