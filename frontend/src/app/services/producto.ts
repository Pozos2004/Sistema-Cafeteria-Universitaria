import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ProductoService {
  // La URL de tu API en Django
  private apiUrl = 'http://127.0.0.1:8000/api/productos/';

  constructor(private http: HttpClient) { }

  // Método para obtener todos los productos
  getProductos(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl);
  }
}