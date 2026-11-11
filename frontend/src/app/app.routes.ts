import { Routes } from '@angular/router';
import { inject } from '@angular/core';
import { AuthService } from './services/auth';
import { Router } from '@angular/router';

const authGuard = () => {
  const authService = inject(AuthService);
  const router = inject(Router);
  if (authService.isLoggedIn()) return true;
  router.navigate(['/login']);
  return false;
};

export const routes: Routes = [
  { 
    path: '', 
    loadComponent: () => import('./menu-cliente/menu-cliente').then(m => m.MenuClienteComponent),
    canActivate: [authGuard] 
  },
  { path: 'login', loadComponent: () => import('./login/login').then(m => m.LoginComponent) },
  { 
    path: 'cocina', 
    loadComponent: () => import('./cocina/cocina').then(m => m.CocinaComponent) 
    // <-- QUITAMOS EL canActivate de aquí para que el cocinero pueda entrar directo
  },
  { path: 'seguimiento', loadComponent: () => import('./seguimiento/seguimiento').then(m => m.SeguimientoComponent) },
  { path: 'seguimiento/:folio', loadComponent: () => import('./seguimiento/seguimiento').then(m => m.SeguimientoComponent) },
  { path: '**', redirectTo: '' }
];