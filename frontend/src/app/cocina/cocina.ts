import { Component, OnInit, OnDestroy, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { AuthService } from '../services/auth';
import { Router } from '@angular/router';

@Component({
  selector: 'app-cocina',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './cocina.html',
  styleUrl: './cocina.css'
})
export class CocinaComponent implements OnInit, OnDestroy {
  pedidos = signal<any[]>([]);
  intervalo: any;

  constructor(private http: HttpClient, private authService: AuthService, private router: Router) {}

  ngOnInit() {
    this.cargarPedidos();
    this.intervalo = setInterval(() => this.cargarPedidos(), 5000);
  }

  ngOnDestroy() {
    if (this.intervalo) clearInterval(this.intervalo);
  }

  cargarPedidos() {
    this.http.get<any[]>('http://127.0.0.1:8000/api/pedidos/').subscribe({
      next: (data) => {
        const activos = data.filter(p => p.estado !== 'ENTREGADO' && p.estado !== 'CANCELADO');
        this.pedidos.set(activos);
      }
    });
  }

  cambiarEstado(pedido: any, nuevoEstado: string) {
    // Obtenemos el token del usuario logueado
    const token = this.authService.getToken();
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);

    this.http.patch(`http://127.0.0.1:8000/api/pedidos/${pedido.id}/`, { estado: nuevoEstado }, { headers }).subscribe({
      next: () => this.cargarPedidos(),
      error: (err) => {
        console.error('Error al cambiar estado:', err);
        alert('Error al cambiar el estado. Revisa la consola.');
      }
    });
  }

  logout() {
    this.authService.logout();
  }
}