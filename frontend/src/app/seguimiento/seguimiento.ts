import { Component, OnInit, OnDestroy, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-seguimiento',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './seguimiento.html',
  styleUrl: './seguimiento.css'
})
export class SeguimientoComponent implements OnInit, OnDestroy {
  folio: string = '';
  pedido: any = null;
  intervalo: any;

  constructor(private http: HttpClient, private route: ActivatedRoute, private cdr: ChangeDetectorRef) {}

  ngOnInit() {
    this.route.paramMap.subscribe(params => {
      const folioUrl = params.get('folio');
      if (folioUrl) {
        this.folio = folioUrl;
        this.buscarPedido();
      }
    });
    
    this.intervalo = setInterval(() => {
      if (this.folio) this.buscarPedido();
    }, 5000);
  }

  ngOnDestroy() {
    if (this.intervalo) clearInterval(this.intervalo);
  }

  buscarPedido() {
    this.http.get<any[]>('http://127.0.0.1:8000/api/pedidos/').subscribe(data => {
      const encontrado = data.find(p => p.folio === this.folio);
      if (encontrado) {
        this.pedido = encontrado;
      } else {
        this.pedido = null;
      }
      this.cdr.detectChanges();
    });
  }
}